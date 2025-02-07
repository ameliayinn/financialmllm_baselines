import os
import glob

# 设置文件夹路径
folder_path = '/hpc2hdd/home/jliu043/ywj/financialmm/dataset/ticker_pricedata_2017'  # 替换为你的文件夹路径

# 查找所有以 '_2017.csv' 结尾的文件
csv_files = glob.glob(os.path.join(folder_path, '*_2017.csv'))

# 遍历所有找到的文件，进行重命名
for file_path in csv_files:
    # 构造新的文件名（去掉 '_2017'）
    new_file_path = file_path.replace('_2017.csv', '.csv')
    
    # 重命名文件
    os.rename(file_path, new_file_path)

    print(f"文件已重命名: {file_path} -> {new_file_path}")

print("所有文件重命名完成！")
