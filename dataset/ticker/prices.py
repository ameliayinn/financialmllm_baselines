import os
import json
import pandas as pd

def process_stock_data_to_jsonl(input_dir='../ticker_pricedata_2017', output_file='prices.jsonl'):
    """将股票数据存储为 JSON Lines (JSONL) 格式，每行一个 {ticker: prices_list}"""
    
    # 确保输出文件名以 .jsonl 结尾
    if not output_file.endswith('.jsonl'):
        output_file += '.jsonl'
    
    with open(output_file, 'w') as f_out:
        for filename in os.listdir(input_dir):
            if filename.endswith('.csv'):
                ticker = filename[:-4]  # 去掉 .csv 后缀
                try:
                    filepath = os.path.join(input_dir, filename)
                    df = pd.read_csv(filepath)
                    
                    if 'DlyPrc' in df.columns:
                        prices = df['DlyPrc'].tolist()
                        record = {ticker: prices}
                        json_line = json.dumps(record, separators=(',', ':'))
                        f_out.write(json_line + '\n')  # 写入一行 JSONL

                    else:
                        print(f"警告: {filename} 中没有 DlyPrc 列")
                except Exception as e:
                    print(f"处理 {filename} 时出错: {e}")
    
    print(f"处理完成，结果已保存到 {output_file}")

# 使用示例
process_stock_data_to_jsonl() 