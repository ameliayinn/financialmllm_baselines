import os
import re

# 目标文件夹路径
folder_path = '/hpc2hdd/home/jliu043/ywj/financialmm/dataset/ticker_pricedata_2017'

# 存储提取结果的列表
result_list = []

# 遍历文件夹中的所有文件
for file_name in os.listdir(folder_path):
    # 匹配 *_2017.csv 的文件名格式
    match = re.match(r'(.*)_2017\.csv', file_name)
    if match:
        result_list.append(match.group(1))  # 提取 * 部分

with open('ticker_names.txt', 'w') as f:
    f.write(str(result_list))
print(len(result_list))
# print("提取结果：", result_list)