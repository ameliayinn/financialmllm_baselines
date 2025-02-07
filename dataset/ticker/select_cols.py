import pandas as pd

# 读取原始CSV文件
data = pd.read_csv('/hpc2hdd/home/jliu043/ywj/financialmm/dataset/ticker/data_original.csv')

# 选择需要的列（A、C、D）
selected_columns = data[['ticker', 'title', 'body', 'past_50', 'future_10']]

# 将选中的列保存到新的CSV文件
selected_columns.to_csv('/hpc2hdd/home/jliu043/ywj/financialmm/dataset/ticker/data.csv', index=False)

print("data.csv")