import pandas as pd
import ast
import os

# 读取 CSV 文件
file_path = "/hpc2hdd/home/jliu043/ywj/financialmm/dataset/ticker/selected_rows.csv"  # 替换为你的文件路径
df = pd.read_csv(file_path)

# 创建输出文件夹
output_dir = "/hpc2hdd/home/jliu043/ywj/financialmm/dataset/ticker_new"
os.makedirs(output_dir, exist_ok=True)

ticker_names = ['ETN', 'BIO', 'CNP', 'NKE', 'MDLZ', 'HSIC', 'DLR', 'SBAC', 'O', 'WYNN', 'MA', 'KEY', 'CB', 'AAPL', 'HOLX', 'KR', 'BIIB', 'LYB', 'INTC', 'AEP', 'WEC', 'CSCO', 'AME', 'MNST', 'ICE', 'BX', 'EXC', 'INVH', 'WAT', 'LUV', 'SJM', 'PEP', 'CCL', 'MSCI', 'ES', 'STT', 'ELV', 'NCLH', 'XOM', 'K', 'ROK', 'CMI', 'ULTA', 'IFF', 'F', 'SHW', 'MTB', 'HCA', 'EBAY', 'CMS', 'AON', 'EQT', 'CTSH', 'GS', 'MGM', 'URI', 'WST', 'TSLA', 'ISRG', 'NVR', 'EPAM', 'EIX', 'UAL', 'PODD', 'MOS', 'AOS', 'NI', 'PANW', 'GLW', 'LRCX', 'XYL', 'LDOS', 'AJG', 'UNP', 'HPQ', 'SWK', 'HLT', 'POOL', 'MCK', 'BWA', 'SLB', 'ADM', 'QCOM', 'CRL', 'CFG', 'BA', 'RTX', 'MLM', 'DFS', 'D', 'WMB', 'CTRA', 'PCG', 'LKQ', 'ESS', 'KMI', 'SPG', 'BBY', 'RJF', 'JNJ', 'HWM', 'CCI', 'RSG', 'TDY', 'ANET', 'CBRE', 'GDDY', 'HAS', 'MCD', 'ANSS', 'ETSY', 'MO', 'ALGN', 'ACN', 'PFE', 'FAST', 'FITB', 'ALL', 'DHI', 'COF', 'VTR', 'FTV', 'RF', 'PARA', 'EA', 'YUM', 'GRMN', 'JKHY', 'LULU', 'DPZ', 'FE', 'ITW', 'EXPE', 'GOOG', 'IP', 'ATO', 'TMUS', 'UNH', 'LLY', 'GPN', 'AVGO', 'IT', 'MPWR', 'VRSK', 'DE', 'PRU', 'XEL', 'WM', 'TGT', 'TECH', 'NXPI', 'ABT', 'NFLX', 'CF', 'KLAC', 'DGX', 'AMZN', 'AMT', 'LYV', 'CTLT', 'CNC', 'PYPL', 'META', 'HUBB', 'HON', 'EVRG', 'WAB', 'FCX', 'APH', 'TXN', 'NEE', 'BXP', 'PKG', 'DOV', 'KHC', 'PNW', 'MHK', 'HII', 'BAC', 'PEG', 'CTAS', 'GM', 'DHR', 'CL', 'KEYS', 'AXP', 'ORCL', 'MTD', 'SYF', 'CSGP', 'ADSK', 'CI', 'TEL', 'EXPD', 'BAX', 'NWSA', 'AIG', 'TYL', 'LMT', 'BKNG', 'FRT', 'NTRS', 'ALLE', 'EL', 'DG', 'TSCO', 'CE', 'GIS', 'MAS', 'AFL', 'HPE', 'TRMB', 'BRO', 'NEM', 'CINF', 'TAP', 'JBHT', 'COO', 'BLDR', 'VLO', 'NWS', 'DIS', 'DTE', 'AEE', 'FFIV', 'VMC', 'BG', 'GL', 'MMM', 'AAL', 'AES', 'AMAT', 'BBWI', 'DLTR', 'ROST', 'PH', 'NDAQ', 'BEN', 'CPT', 'MRK', 'UHS', 'ROP', 'DD', 'ZBRA', 'DXCM', 'JPM', 'MCO', 'VRTX', 'EOG', 'PPG', 'MOH', 'PNR', 'NUE', 'NVDA', 'TPR', 'IQV', 'TRGP', 'GWW', 'APD', 'HES', 'SMCI', 'PFG', 'CVX', 'IVZ', 'WTW', 'VST', 'JBL', 'LHX', 'MET', 'TTWO', 'BLK', 'MMC', 'KO', 'SNPS', 'EMN', 'IR', 'RL', 'UPS', 'COST', 'LH', 'MS', 'GOOGL', 'CHD', 'AVB', 'AMGN', 'ORLY', 'SWKS', 'CMCSA', 'ADP', 'ARE', 'REGN', 'LW', 'FDX', 'ECL', 'DAL', 'HIG', 'SCHW', 'WDC', 'MU', 'AMP', 'IDXX', 'TDG', 'PLD', 'WY', 'NOC', 'HSY', 'QRVO', 'GE', 'EXR', 'OKE', 'CHTR', 'A', 'ADBE', 'C', 'SYY', 'ZTS', 'LNT', 'AXON', 'CMG', 'DECK', 'LVS', 'TMO', 'COR', 'AKAM', 'HBAN', 'CBOE', 'MCHP', 'FANG', 'STE', 'JCI', 'HRL', 'TT', 'EQR', 'KIM', 'PSA', 'DVN', 'RCL', 'AVY', 'FSLR', 'TER', 'BK', 'SO', 'BKR', 'MTCH', 'CRM', 'TXT', 'MKTX', 'TSN', 'LOW', 'INTU', 'COP', 'PNC', 'IEX', 'OMC', 'BDX', 'CVS', 'CAT', 'WMT', 'BR', 'DUK', 'TJX', 'STZ', 'LEN', 'TRV', 'CSX', 'SYK', 'PTC', 'PCAR', 'TFC', 'ADI', 'CHRW', 'KMB', 'MAA', 'ON', 'AIZ', 'SPGI', 'ZBH', 'GPC', 'NRG', 'AMD', 'CAH', 'VZ', 'WBA', 'CLX', 'APA', 'WRB', 'ETR', 'FMC', 'CME', 'CAG', 'J', 'CZR', 'IBM', 'PAYC', 'NOW', 'ED', 'SNA', 'ODFL', 'PSX', 'TROW', 'MRO', 'KMX', 'GNRC', 'SRE', 'FIS', 'GILD', 'STX', 'APTV', 'EQIX', 'PAYX', 'GD', 'STLD', 'MAR', 'DOW', 'USB', 'DRI', 'NSC', 'FTNT', 'EW', 'WFC', 'GEN', 'L', 'HUM', 'MSFT', 'CPB', 'T', 'NTAP', 'V', 'BMY', 'UDR', 'IRM', 'MPC', 'FDS', 'CDW', 'ABBV', 'PGR', 'ACGL', 'AZO', 'VRSN', 'BALL', 'JNPR', 'BSX', 'PWR', 'EFX', 'DVA', 'HST', 'AWK', 'NDSN', 'IPG', 'MSI', 'PPL', 'ALB', 'MDT', 'HD', 'OXY', 'HAL', 'ROL', 'PHM', 'PG', 'KKR', 'CDNS', 'ENPH', 'TFX', 'FICO', 'CPRT', 'EMR', 'PM', 'INCY', 'REG', 'SBUX', 'MKC', 'DOC', 'RMD']

# 遍历每个 ticker
for _, row in df.iterrows():
    if row['ticker'] in ticker_names:
        ticker = row['ticker']
        body = row['body']
        past_50 = ast.literal_eval(row['past_50'])  # 转换为列表
        future_10 = ast.literal_eval(row['future_10'])  # 转换为列表
        
        # 保存 body 到 txt 文件
        txt_file = os.path.join('/hpc2hdd/home/jliu043/ywj/financialmm/dataset/prompt_bank', f"{ticker}.txt")
        with open(txt_file, "w", encoding="utf-8") as f:
            f.write(body)
        
        # 组合 past_50 和 future_10
        combined_data = past_50 + future_10
        csv_file = os.path.join(output_dir, f"{ticker}.csv")
        
        # 保存为 60 行 1 列的 CSV
        pd.DataFrame({"data": combined_data}).to_csv(csv_file, index=False)

print("文件处理完成！")
