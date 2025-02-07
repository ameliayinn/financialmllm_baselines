from data_provider.data_loader import Dataset_ETT_hour, Dataset_ETT_minute, Dataset_Custom, Dataset_M4, Dataset_A, Dataset_Ticker
from torch.utils.data import DataLoader

data_dict = {
    'A': Dataset_Ticker,
    'ETTh1': Dataset_ETT_hour,
    'ETTh2': Dataset_ETT_hour,
    'ETTm1': Dataset_ETT_minute,
    'ETTm2': Dataset_ETT_minute,
    'ECL': Dataset_Custom,
    'Traffic': Dataset_Custom,
    'Weather': Dataset_Custom,
    'm4': Dataset_M4,
}

ticker_names = ['ETN', 'BIO', 'CNP', 'NKE', 'MDLZ', 'HSIC', 'DLR', 'SBAC', 'O', 'WYNN', 'MA', 'KEY', 'CB', 'AAPL', 'HOLX', 'KR', 'BIIB', 'LYB', 'INTC', 'AEP', 'WEC', 'CSCO', 'AME', 'MNST', 'ICE', 'BX', 'EXC', 'INVH', 'WAT', 'LUV', 'SJM', 'PEP', 'CCL', 'MSCI', 'ES', 'STT', 'ELV', 'NCLH', 'XOM', 'K', 'ROK', 'CMI', 'ULTA', 'IFF', 'F', 'SHW', 'MTB', 'HCA', 'EBAY', 'CMS', 'AON', 'EQT', 'CTSH', 'GS', 'MGM', 'URI', 'WST', 'TSLA', 'ISRG', 'NVR', 'EPAM', 'EIX', 'UAL', 'PODD', 'MOS', 'AOS', 'NI', 'PANW', 'GLW', 'LRCX', 'XYL', 'LDOS', 'AJG', 'UNP', 'HPQ', 'SWK', 'HLT', 'POOL', 'MCK', 'BWA', 'SLB', 'ADM', 'QCOM', 'CRL', 'CFG', 'BA', 'RTX', 'MLM', 'DFS', 'D', 'WMB', 'CTRA', 'PCG', 'LKQ', 'ESS', 'KMI', 'SPG', 'BBY', 'RJF', 'JNJ', 'HWM', 'CCI', 'RSG', 'TDY', 'ANET', 'CBRE', 'GDDY', 'HAS', 'MCD', 'ANSS', 'ETSY', 'MO', 'ALGN', 'ACN', 'PFE', 'FAST', 'FITB', 'ALL', 'DHI', 'COF', 'VTR', 'FTV', 'RF', 'PARA', 'EA', 'YUM', 'GRMN', 'JKHY', 'LULU', 'DPZ', 'FE', 'ITW', 'EXPE', 'GOOG', 'IP', 'ATO', 'TMUS', 'UNH', 'LLY', 'GPN', 'AVGO', 'IT', 'MPWR', 'VRSK', 'DE', 'PRU', 'XEL', 'WM', 'TGT', 'TECH', 'NXPI', 'ABT', 'NFLX', 'CF', 'KLAC', 'DGX', 'AMZN', 'AMT', 'LYV', 'CTLT', 'CNC', 'PYPL', 'META', 'HUBB', 'HON', 'EVRG', 'WAB', 'FCX', 'APH', 'TXN', 'NEE', 'BXP', 'PKG', 'DOV', 'KHC', 'PNW', 'MHK', 'HII', 'BAC', 'PEG', 'CTAS', 'GM', 'DHR', 'CL', 'KEYS', 'AXP', 'ORCL', 'MTD', 'SYF', 'CSGP', 'ADSK', 'CI', 'TEL', 'EXPD', 'BAX', 'NWSA', 'AIG', 'TYL', 'LMT', 'BKNG', 'FRT', 'NTRS', 'ALLE', 'EL', 'DG', 'TSCO', 'CE', 'GIS', 'MAS', 'AFL', 'HPE', 'TRMB', 'BRO', 'NEM', 'CINF', 'TAP', 'JBHT', 'COO', 'BLDR', 'VLO', 'NWS', 'DIS', 'DTE', 'AEE', 'FFIV', 'VMC', 'BG', 'GL', 'MMM', 'AAL', 'AES', 'AMAT', 'BBWI', 'DLTR', 'ROST', 'PH', 'NDAQ', 'BEN', 'CPT', 'MRK', 'UHS', 'ROP', 'DD', 'ZBRA', 'DXCM', 'JPM', 'MCO', 'VRTX', 'EOG', 'PPG', 'MOH', 'PNR', 'NUE', 'NVDA', 'TPR', 'IQV', 'TRGP', 'GWW', 'APD', 'HES', 'SMCI', 'PFG', 'CVX', 'IVZ', 'WTW', 'VST', 'JBL', 'LHX', 'MET', 'TTWO', 'BLK', 'MMC', 'KO', 'SNPS', 'EMN', 'IR', 'RL', 'UPS', 'COST', 'LH', 'MS', 'GOOGL', 'CHD', 'AVB', 'AMGN', 'ORLY', 'SWKS', 'CMCSA', 'ADP', 'ARE', 'REGN', 'LW', 'FDX', 'ECL', 'DAL', 'HIG', 'SCHW', 'WDC', 'MU', 'AMP', 'IDXX', 'TDG', 'PLD', 'WY', 'NOC', 'HSY', 'QRVO', 'GE', 'EXR', 'OKE', 'CHTR', 'A', 'ADBE', 'C', 'SYY', 'ZTS', 'LNT', 'AXON', 'CMG', 'DECK', 'LVS', 'TMO', 'COR', 'AKAM', 'HBAN', 'CBOE', 'MCHP', 'FANG', 'STE', 'JCI', 'HRL', 'TT', 'EQR', 'KIM', 'PSA', 'DVN', 'RCL', 'AVY', 'FSLR', 'TER', 'BK', 'SO', 'BKR', 'MTCH', 'CRM', 'TXT', 'MKTX', 'TSN', 'LOW', 'INTU', 'COP', 'PNC', 'IEX', 'OMC', 'BDX', 'CVS', 'CAT', 'WMT', 'BR', 'DUK', 'TJX', 'STZ', 'LEN', 'TRV', 'CSX', 'SYK', 'PTC', 'PCAR', 'TFC', 'ADI', 'CHRW', 'KMB', 'MAA', 'ON', 'AIZ', 'SPGI', 'ZBH', 'GPC', 'NRG', 'AMD', 'CAH', 'VZ', 'WBA', 'CLX', 'APA', 'WRB', 'ETR', 'FMC', 'CME', 'CAG', 'J', 'CZR', 'IBM', 'PAYC', 'NOW', 'ED', 'SNA', 'ODFL', 'PSX', 'TROW', 'MRO', 'KMX', 'GNRC', 'SRE', 'FIS', 'GILD', 'STX', 'APTV', 'EQIX', 'PAYX', 'GD', 'STLD', 'MAR', 'DOW', 'USB', 'DRI', 'NSC', 'FTNT', 'EW', 'WFC', 'GEN', 'L', 'HUM', 'MSFT', 'CPB', 'T', 'NTAP', 'V', 'BMY', 'UDR', 'IRM', 'MPC', 'FDS', 'CDW', 'ABBV', 'PGR', 'ACGL', 'AZO', 'VRSN', 'BALL', 'JNPR', 'BSX', 'PWR', 'EFX', 'DVA', 'HST', 'AWK', 'NDSN', 'IPG', 'MSI', 'PPL', 'ALB', 'MDT', 'HD', 'OXY', 'HAL', 'ROL', 'PHM', 'PG', 'KKR', 'CDNS', 'ENPH', 'TFX', 'FICO', 'CPRT', 'EMR', 'PM', 'INCY', 'REG', 'SBUX', 'MKC', 'DOC', 'RMD']

# 遍历 ticker_names 并为每个 ticker 添加新的条目
for ticker in ticker_names:
    data_dict[ticker] = Dataset_Ticker  # 为每个 ticker 添加 Dataset_Ticker

def data_provider(args, flag):
    Data = data_dict[args.data]
    timeenc = 0 if args.embed != 'timeF' else 1
    percent = args.percent

    if flag == 'test':
        shuffle_flag = False
        drop_last = True
        batch_size = args.batch_size
        freq = args.freq
    else:
        shuffle_flag = True
        drop_last = True
        batch_size = args.batch_size
        freq = args.freq

    if args.data == 'm4':
        drop_last = False
        data_set = Data(
            root_path=args.root_path,
            data_path=args.data_path,
            flag=flag,
            size=[args.seq_len, args.label_len, args.pred_len],
            features=args.features,
            target=args.target,
            timeenc=timeenc,
            freq=freq,
            seasonal_patterns=args.seasonal_patterns
        )
    else:
        data_set = Data(
            root_path=args.root_path,
            data_path=args.data_path,
            flag=flag,
            size=[args.seq_len, args.label_len, args.pred_len],
            features=args.features,
            target=args.target,
            timeenc=timeenc,
            freq=freq,
            percent=percent,
            seasonal_patterns=args.seasonal_patterns
        )
    data_loader = DataLoader(
        data_set,
        batch_size=batch_size,
        shuffle=shuffle_flag,
        num_workers=args.num_workers,
        drop_last=drop_last)
    return data_set, data_loader
