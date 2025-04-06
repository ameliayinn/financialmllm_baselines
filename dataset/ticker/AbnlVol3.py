import pandas as pd
import numpy as np
import pymc as pm
from scipy.stats import norm
import matplotlib.pyplot as plt
import warnings

# 忽略一些警告
warnings.filterwarnings("ignore", category=RuntimeWarning)

# ==================== 1. 数据准备 ====================
inputfile = '../ticker_pricedata_2017/AAPL.csv'
df = pd.read_csv(inputfile, usecols=['YYYYMMDD', 'DlyVol'])
window = 60

# ==================== 2. 改进的贝叶斯波动率估计 ====================
def bayesian_volatility_estimation(data):
    """更稳健的贝叶斯方法估计波动率参数"""
    # 数据预处理：确保至少有3个数据点且标准差不为0
    if len(data) < 3:
        return np.mean(data), np.std(data) if len(data) > 0 else (data[0], 1.0)
    
    data_std = np.std(data)
    if data_std == 0:
        data_std = 1.0  # 避免除零
    
    with pm.Model() as model:
        # 更稳健的先验分布设置
        mu = pm.StudentT('mu', nu=4, 
                        mu=np.median(data),  # 使用中位数更稳健
                        sigma=data_std*5)    # 更宽松的标准差
        
        # 对sigma使用更稳健的先验
        sigma = pm.HalfNormal('sigma', sigma=data_std*5)
        
        # 似然函数
        likelihood = pm.Normal('returns', mu=mu, sigma=sigma, observed=data)
        
        # 更稳健的MCMC采样设置
        try:
            trace = pm.sample(
                1000, tune=1000, 
                chains=2, 
                progressbar=False,
                init='adapt_diag',  # 更稳健的初始化方法
                target_accept=0.9    # 更高的接受率
            )
        except:
            # 如果采样失败，返回简单统计量
            return np.mean(data), data_std
    
    return np.mean(trace.posterior['mu']), np.mean(trace.posterior['sigma'])

# ==================== 3. 蒙特卡洛模拟测试 ====================
def monte_carlo_simulation(true_anomalies, n_simulations=1000):
    """评估Z-score方法的检测性能"""
    detection_rates = []
    false_positives = []
    
    for _ in range(n_simulations):
        # 生成符合真实数据统计特性的模拟序列
        sim_data = np.random.normal(df['DlyVol'].mean(), df['DlyVol'].std(), len(df))
        
        # 添加已知异常点（位置与真实数据相同）
        anomaly_indices = df[df['Is_Abnormal']].index
        sim_data[anomaly_indices] *= np.random.uniform(2, 5, len(anomaly_indices))
        
        # 应用Z-score检测
        rolling_mean = pd.Series(sim_data).rolling(window).mean()
        rolling_std = pd.Series(sim_data).rolling(window).std()
        z_scores = (sim_data - rolling_mean) / rolling_std
        detected = np.abs(z_scores) > 3
        
        # 计算指标
        detection_rates.append(np.sum(detected[anomaly_indices])/len(anomaly_indices))
        false_positives.append(np.sum(detected) - np.sum(detected[anomaly_indices]))
    
    return np.mean(detection_rates), np.mean(false_positives)

# ==================== 4. 混合检测策略 ====================
df['Z_Score'] = np.nan
df['Is_Abnormal'] = False
df['Reference_Mean'] = np.nan
df['Days_Used'] = 0  # 记录用于计算参考值的天数

# 初始贝叶斯估计（使用前3个数据点作为最小样本）
initial_data = df['DlyVol'].iloc[:3].values
mu_bayes, sigma_bayes = bayesian_volatility_estimation(initial_data)

for i in range(len(df)):
    if i < window:
        # 前60日使用贝叶斯估计（动态更新）
        if i >= 3:  # 至少使用3个数据点
            current_data = df['DlyVol'].iloc[:i+1].values
            mu_bayes, sigma_bayes = bayesian_volatility_estimation(current_data)
        
        current_vol = df['DlyVol'].iloc[i]
        z = (current_vol - mu_bayes) / max(sigma_bayes, 1e-6)  # 避免除零
        df.loc[df.index[i], 'Z_Score'] = z
        df.loc[df.index[i], 'Is_Abnormal'] = np.abs(z) > 3
        df.loc[df.index[i], 'Reference_Mean'] = mu_bayes
        df.loc[df.index[i], 'Days_Used'] = i+1
    else:
        # 60日后使用常规Z-score
        window_data = df['DlyVol'].iloc[i-window:i]
        current_vol = df['DlyVol'].iloc[i]
        window_std = window_data.std()
        if window_std == 0:
            window_std = 1e-6  # 避免除零
        z = (current_vol - window_data.mean()) / window_std
        df.loc[df.index[i], 'Z_Score'] = z
        df.loc[df.index[i], 'Is_Abnormal'] = np.abs(z) > 3
        df.loc[df.index[i], 'Reference_Mean'] = window_data.mean()
        df.loc[df.index[i], 'Days_Used'] = window

# ==================== 5. 结果分析 ====================
abnormal_dates = df[df['Is_Abnormal']].copy()
abnormal_dates['AbnlVol'] = abnormal_dates['DlyVol']

# 计算变化百分比
abnormal_dates['VolChangePct'] = np.where(
    abnormal_dates['Reference_Mean'] > 0,
    (abnormal_dates['DlyVol'] / abnormal_dates['Reference_Mean'] - 1) * 100,
    np.nan
)

abnormal_dates['Direction'] = np.where(abnormal_dates['VolChangePct'] > 0, '增高', '减少')

# 生成描述（使用实际使用的天数）
abnormal_dates['Description'] = abnormal_dates.apply(
    lambda row: (
        f"{row['YYYYMMDD']}日的成交量({row['AbnlVol']:,}股)较过去{row['Days_Used']}个交易日的平均成交量"
        f"({row['Reference_Mean']:,.1f}股){row['Direction']}了"
        f"{abs(row['VolChangePct']):.1f}%"
        if not pd.isna(row['Reference_Mean']) 
        else f"{row['YYYYMMDD']}日数据不足无法计算参考均值"
    ), 
    axis=1
)

# ==================== 6. 性能评估 ====================
try:
    detection_rate, false_positives = monte_carlo_simulation(abnormal_dates.index)
    print(f"\n蒙特卡洛测试结果：")
    print(f"异常检测率：{detection_rate:.1%}")
    print(f"平均误报数：{false_positives:.1f}")
except:
    print("\n蒙特卡洛测试跳过（可能需要更多数据）")

# ==================== 7. 结果保存 ====================
output_cols = ['YYYYMMDD', 'AbnlVol', 'Reference_Mean', 'VolChangePct', 'Direction', 'Description', 'Days_Used']
outputfile = f'../ticker_pricedata_2017_Abnl/{inputfile[24:-4]}_AbnlVol.csv'
abnormal_dates[output_cols].to_csv(outputfile, index=False)

print(f"\n结果已保存至 {outputfile}")
print(abnormal_dates[output_cols].head())