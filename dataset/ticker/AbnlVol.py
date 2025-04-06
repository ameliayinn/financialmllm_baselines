import pandas as pd
import numpy as np

# 1. 读取数据
inputfile = '../ticker_pricedata_2017/BA.csv'
df = pd.read_csv(inputfile, usecols=['YYYYMMDD', 'DlyVol'])

# 2. 计算滚动统计量（窗口60日）
window = 60
df['Rolling_Mean'] = df['DlyVol'].rolling(window).mean()
df['Rolling_Std'] = df['DlyVol'].rolling(window).std()
df['Z_Score'] = (df['DlyVol'] - df['Rolling_Mean']) / df['Rolling_Std']

# 3. 检测异常（Z > 3）
df['Is_Abnormal'] = np.abs(df['Z_Score']) > 3
abnormal_dates = df[df['Is_Abnormal']].copy()

# 4. 计算变动百分比和方向
abnormal_dates['AbnlVol'] = abnormal_dates['DlyVol']
abnormal_dates['Rolling_Mean'] = abnormal_dates['Rolling_Mean'].apply(lambda x: f"{x:.1f}")
abnormal_dates['Rolling_Mean'] = abnormal_dates['Rolling_Mean'].astype(float)
abnormal_dates['VolChangePct'] = (abnormal_dates['DlyVol'] / abnormal_dates['Rolling_Mean'] - 1) * 100
abnormal_dates['Direction'] = np.where(abnormal_dates['VolChangePct'] > 0, '增高', '减少')

# 增加说明列
abnormal_dates['Description'] = abnormal_dates.apply(
    lambda row: f"{row['YYYYMMDD']}日的成交量({row['AbnlVol']:,}股)较过去{window}个交易日的平均成交量（{row['Rolling_Mean']:,}股）{row['Direction']}了{abs(row['VolChangePct']):.1f}%。", 
    axis=1
)

# 5. 保存结果（日期、异常值、变动百分比）
result = abnormal_dates[['YYYYMMDD', 'AbnlVol', 'Rolling_Mean', 'VolChangePct', 'Direction', 'Description']]
outputfile = f'../ticker_pricedata_2017_Abnl/{inputfile[24:-4]}_AbnlVol_1.csv'
result.to_csv(outputfile, index=False)

print(f"异常交易量日期及提升比已保存至 {outputfile}.csv")
print(result)