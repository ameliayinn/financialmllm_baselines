import pandas as pd

# 读取CSV文件
data = pd.read_csv('/hpc2hdd/home/jliu043/ywj/financialmm/dataset/data.csv')

# 统计行数
num_rows = len(data)

print(f"CSV文件中共有 {num_rows} 行数据。")
# CSV文件中共有 126521 行数据。