import pandas as pd

# 读取CSV文件
data = pd.read_csv('/hpc2hdd/home/jliu043/ywj/financialmm/dataset/ticker/data.csv')

# 选取前100行
first_100_rows = data.head(100)

# 将前100行保存到新的CSV文件
first_100_rows.to_csv('/hpc2hdd/home/jliu043/ywj/financialmm/dataset/ticker/data_100.csv', index=False)

print("前100行已保存到 'first_100_rows.csv' 文件中。")