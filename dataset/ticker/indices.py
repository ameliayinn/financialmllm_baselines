import json

# 读取原始JSON文件
with open('/hpc2hdd/home/jliu043/ywj/financialmm/dataset/ticker/indices_original.json', 'r') as file:
    data = json.load(file)

# 定义过滤函数
def filter_numbers(arr, threshold=126520):
    return [num for num in arr if num <= threshold]

# 过滤 train、val、test 数组
filtered_data = {
    "train": filter_numbers(data["train"]),
    "val": filter_numbers(data["val"]),
    "test": filter_numbers(data["test"])
}

# 将过滤后的数据保存到新的JSON文件
with open('/hpc2hdd/home/jliu043/ywj/financialmm/dataset/ticker/indices.json', 'w') as file:
    json.dump(filtered_data, file, indent=4)

# 统计新旧数组的长度
original_lengths = {
    "train": len(data["train"]),
    "val": len(data["val"]),
    "test": len(data["test"])
}

filtered_lengths = {
    "train": len(filtered_data["train"]),
    "val": len(filtered_data["val"]),
    "test": len(filtered_data["test"])
}

# 输出统计结果
print("原始数组长度：", original_lengths)
print("过滤后数组长度：", filtered_lengths)
print("过滤后的数据已保存到 'indices.json' 文件中。")

'''
原始数组长度： {'train': 88564, 'val': 12653, 'test': 25304}
过滤后数组长度： {'train': 4109, 'val': 589, 'test': 1136}
过滤后的数据已保存到 'indices.json' 文件中。
'''