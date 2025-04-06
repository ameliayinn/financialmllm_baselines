import pandas as pd

# 读取 Stata 文件
# df = pd.read_stata('stock_price_2017.dta')

# 读取Pkl文件
# df = pd.read_pickle('news_ticker_all.pkl')

# 读取csv文件
df = pd.read_csv('news_2017.csv', usecols=["body"])

# 获取 ticker 列中不同值的数量
# unique_tickers = df['Ticker'].nunique()

# 获取 ticker 列中不同值的列表
# unique_ticker_list = df['Ticker'].unique()

max_length = df["body"].str.len().max()

#print(f"不同的 ticker 值数量: {unique_tickers}")
#print("不同的 ticker 值列表:")
#print(unique_ticker_list)
print(df.columns)
print(max_length)