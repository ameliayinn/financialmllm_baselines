import pandas as pd
import numpy as np
import pymc as pm
from scipy.stats import norm
import matplotlib.pyplot as plt

# ==================== 1. 数据准备 ====================
inputfile = '../ticker_pricedata_2017/BA.csv'
df = pd.read_csv(inputfile, usecols=['YYYYMMDD', 'DlyVol'])
window = 60

# ==================== 2. 贝叶斯波动率估计（用于前60日） ====================
def bayesian_volatility_estimation(data):
    """贝叶斯方法估计波动率参数"""
    with pm.Model() as model:
        # 先验分布（假设收益率服从正态分布）
        #mu = pm.Normal('mu', mu=np.mean(data), sigma=np.std(data)*3)  # 宽松的均值先验
        #sigma = pm.HalfNormal('sigma', sigma=np.std(data)*3)  # 必须为正的波动率
        
        mu = pm.StudentT('mu', nu=4, mu=data.mean(), sigma=data.std()*2)  # 厚尾分布
        sigma = pm.InverseGamma('sigma', alpha=3, beta=data.std()*2)  # 更灵活的先验
        
        # 似然函数
        likelihood = pm.Normal('returns', mu=mu, sigma=sigma, observed=data)
        
        # MCMC采样
        trace = pm.sample(1000, tune=1000, chains=2, progressbar=False)
    
    return trace.posterior['mu'].mean(), trace.posterior['sigma'].mean()

# 对前60日数据应用贝叶斯估计
early_data = df['DlyVol'].iloc[:window].values
mu_bayes, sigma_bayes = bayesian_volatility_estimation(early_data)

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

for i in range(len(df)):
    if i < window:
        # 前60日使用贝叶斯估计
        current_vol = df['DlyVol'].iloc[i]
        z = (current_vol - mu_bayes) / sigma_bayes
        df.loc[df.index[i], 'Z_Score'] = z
        df.loc[df.index[i], 'Is_Abnormal'] = np.abs(z) > 3
    else:
        # 60日后使用常规Z-score
        window_data = df['DlyVol'].iloc[i-window:i]
        current_vol = df['DlyVol'].iloc[i]
        z = (current_vol - window_data.mean()) / window_data.std()
        df.loc[df.index[i], 'Z_Score'] = z
        df.loc[df.index[i], 'Is_Abnormal'] = np.abs(z) > 3

# ==================== 5. 结果分析 ====================
abnormal_dates = df[df['Is_Abnormal']].copy()
abnormal_dates['AbnlVol'] = abnormal_dates['DlyVol']

# 计算参考均值（前60日用贝叶斯估计，之后用滚动均值）
abnormal_dates['Reference_Mean'] = np.where(
    abnormal_dates.index < window,
    mu_bayes,
    df['DlyVol'].rolling(window).mean().loc[abnormal_dates.index]  # 直接使用原始数据的滚动均值
)

abnormal_dates['VolChangePct'] = np.where(
    abnormal_dates['Reference_Mean'] > 0,
    (abnormal_dates['DlyVol'] / abnormal_dates['Reference_Mean'] - 1) * 100,
    np.nan
)

abnormal_dates['Direction'] = np.where(abnormal_dates['VolChangePct'] > 0, '增高', '减少')

# 生成描述（添加了NaN值处理）
abnormal_dates['Description'] = abnormal_dates.apply(
    lambda row: (
        f"{row['YYYYMMDD']}日的成交量({row['AbnlVol']:,}股)较过去60个交易日的平均成交量"
        f"({row['Reference_Mean']:,.1f}股){row['Direction']}了"
        f"{abs(row['VolChangePct']):.1f}%"
        if not pd.isna(row['Reference_Mean']) 
        else f"{row['YYYYMMDD']}日数据不足无法计算参考均值"
    ), 
    axis=1
)

# ==================== 6. 性能评估 ====================
detection_rate, false_positives = monte_carlo_simulation(abnormal_dates.index)
print(f"\n蒙特卡洛测试结果：")
print(f"异常检测率：{detection_rate:.1%}")
print(f"平均误报数：{false_positives:.1f}")

# ==================== 7. 结果保存 ====================
output_cols = ['YYYYMMDD', 'AbnlVol', 'Reference_Mean', 'VolChangePct', 'Direction', 'Description']
outputfile = f'../ticker_pricedata_2017_Abnl/{inputfile[24:-4]}_AbnlVol_2.csv'
abnormal_dates[output_cols].to_csv(outputfile, index=False)

print(f"\n结果已保存至 {outputfile}")
print(abnormal_dates[output_cols].head())