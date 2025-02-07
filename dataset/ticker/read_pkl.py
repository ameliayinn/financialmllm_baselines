import pandas as pd

# 读取 .pkl 文件中的 DataFrame
pkl_file_path = "/hpc2hdd/home/jliu043/ywj/financialmm/dataset/ticker/news_2017.pkl"  # 替换为你的 pkl 文件路径
df = pd.read_pickle(pkl_file_path)

# 将 DataFrame 转换为 .csv 文件
csv_file_path = "news_2017.csv"  # 替换为你想保存的 CSV 文件路径
df.to_csv(csv_file_path, index=False)  # index=False 是不保存行索引

print("pkl 文件已成功转换为 csv 文件！")
