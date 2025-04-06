import pandas as pd
import os
from datetime import datetime

def process_price_file(price_file):
    # Read price file
    price_df = pd.read_csv(price_file)
    dates = price_df['YYYYMMDD'].tolist()
    dlyprc = price_df['DlyPrc'].tolist()
    return dates, dlyprc

def process_abnlvol_file(abnlvol_file, dates, dlyprc):
    abnlvol_df = pd.read_csv(abnlvol_file)
    dates_1 = abnlvol_df['YYYYMMDD'].tolist()
    descriptions = abnlvol_df['Description'].tolist()
    
    # Create a dictionary for faster lookup of dates in dates_1
    dates_1_dict = {date: idx for idx, date in enumerate(dates_1)}
    
    # 使用字典来按event_date聚合结果
    results_dict = {}
    
    find_t = [
        [59, 49, 'past_50', 'future_10', 50, 10],
        [47, 39, 'past_40', 'future_8', 40, 8],
        [35, 29, 'past_30', 'future_6', 30, 6],
        [23, 19, 'past_20', 'future_4', 20, 4],
        [11, 9, 'past_10', 'future_2', 10, 2]
    ]
    
    for t in range(len(dates)):
        for params in find_t:
            delta1, delta2, past_name, future_name, past_len, future_len = params
            if t + delta1 < len(dates):
                # Check if dates[t+delta2] exists in dates_1
                target_date = dates[t + delta2]
                if target_date in dates_1_dict:
                    # Get the index in dates_1
                    idx_1 = dates_1_dict[target_date]
                    event_date = dates_1[idx_1]
                    
                    # 如果这个event_date还没有记录，创建新记录
                    if event_date not in results_dict:
                        results_dict[event_date] = {
                            'event_date': event_date,
                            'past_50': None,
                            'future_10': None,
                            'past_40': None,
                            'future_8': None,
                            'past_30': None,
                            'future_6': None,
                            'past_20': None,
                            'future_4': None,
                            'past_10': None,
                            'future_2': None,
                            'text': descriptions[idx_1]
                        }
                    
                    # 更新对应的时间窗口数据
                    results_dict[event_date][past_name] = dlyprc[t:t+past_len]
                    results_dict[event_date][future_name] = dlyprc[t+past_len:t+past_len+future_len]
    
    # 将字典转换为列表
    return list(results_dict.values())

def process_news_file(news_file, dates, dlyprc):
    # Read news file
    with open(news_file, 'r') as f:
        lines = f.readlines()
    
    if not lines:
        return []
    
    # First line is the date in "YYYY-MM-DD" format
    date_news_str = lines[0].strip()
    
    try:
        # Parse news date into datetime object
        news_date = datetime.strptime(date_news_str, '%Y-%m-%d').date()
    except ValueError:
        print(f"无法解析新闻文件中的日期: {date_news_str}")
        return []
    
    # The rest is the news content
    news = '\\n'.join(line.strip() for line in lines[1:]).strip()  # 保留换行符
    print(news)
    
    results_dict = {}
    
    # Convert all trading dates to datetime objects
    trading_dates = []
    for date_val in dates:
        try:
            if isinstance(date_val, int):
                date_str = str(date_val)
            else:
                date_str = date_val
            trading_dates.append(datetime.strptime(date_str, '%Y-%m-%d').date())
        except (ValueError, TypeError):
            print(f"跳过无法解析的交易日期: {date_val}")
            continue
    
    find_t = [
        [59, 49, 'past_50', 'future_10', 50, 10],
        [47, 39, 'past_40', 'future_8', 40, 8],
        [35, 29, 'past_30', 'future_6', 30, 6],
        [23, 19, 'past_20', 'future_4', 20, 4],
        [11, 9, 'past_10', 'future_2', 10, 2]
    ]
    
    for t in range(len(trading_dates)):
        for params in find_t:
            delta1, delta2, past_name, future_name, past_len, future_len = params
            
            # Check if we have enough trading dates for this window
            if t + delta1 >= len(trading_dates):
                continue
            
            # Get the event window boundaries
            window_start_pos = t + delta2
            window_end_pos = t + delta2 + 1  # next trading day
            
            if window_end_pos >= len(trading_dates):
                continue
            
            window_start = trading_dates[window_start_pos]
            window_end = trading_dates[window_end_pos]
            
            # Debug print to check the intervals
            # print(f"检查区间: {window_start} 到 {window_end} (新闻日期: {news_date})")
            
            # Check if news date falls within this trading date interval
            if window_start <= news_date < window_end:
                print(f"匹配成功: 新闻日期 {news_date} 落在区间 [{window_start}, {window_end})")
                
                # Use original YYYY-MM-DD format for output
                event_date = date_news_str
                
                if event_date not in results_dict:
                    results_dict[event_date] = {
                        'event_date': event_date,
                        'past_50': None,
                        'future_10': None,
                        'past_40': None,
                        'future_8': None,
                        'past_30': None,
                        'future_6': None,
                        'past_20': None,
                        'future_4': None,
                        'past_10': None,
                        'future_2': None,
                        'text': news
                    }
                
                # Add the price data
                results_dict[event_date][past_name] = dlyprc[t:t+past_len]
                results_dict[event_date][future_name] = dlyprc[t+past_len:t+past_len+future_len]
    
    return list(results_dict.values())

def main():
    # Process price file
    price_file = 'BA_price.csv'
    dates, dlyprc = process_price_file(price_file)
    
    all_results = []
    
    # Process AbnlVol files
    abnlvol_files = [f for f in os.listdir() if 'AbnlVol' in f and f.endswith('.csv')]
    for abnlvol_file in abnlvol_files:
        results = process_abnlvol_file(abnlvol_file, dates, dlyprc)
        all_results.extend(results)
    
    # Process news files
    news_files = [f for f in os.listdir() if 'news' in f and 'prompt' not in f and f.endswith('.txt')]
    for news_file in news_files:
        results = process_news_file(news_file, dates, dlyprc)
        all_results.extend(results)
    
    # Convert to DataFrame
    if all_results:
        df = pd.DataFrame(all_results)
        
        # Reorder columns as specified
        columns_order = [
            'event_date',
            'past_50', 'future_10',
            'past_40', 'future_8',
            'past_30', 'future_6',
            'past_20', 'future_4',
            'past_10', 'future_2',
            'text'
        ]
        df = df[columns_order]
        
        # Save to CSV
        df.to_csv('BA_mllm.csv', index=False)
        print("Successfully created BA_mllm.csv")
    else:
        print("No matching data found to create the output file.")

if __name__ == '__main__':
    main()