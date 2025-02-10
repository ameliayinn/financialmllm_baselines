#!/bin/bash
model_name=TimeLLM
train_epochs=20
learning_rate=0.01
llama_layers=32

#master_port=00097
master_port=8080
num_process=1
batch_size=12
d_model=16
d_ff=32

# 定义数组
seq_lens=(10 20 30 40 50)
label_lens=(5 10 15 20 25)
pred_lens=(2 4 6 8 10)
# tickers=("BA" "MCO" "KKR" "AZO" "UAL" "EQT" "EA" "HII" "PSX" "VMC" "CAT" "EBAY" "BMY" "SPG" "MTB" "KEY" "XOM" "TGT" "PFE" "HUM" "KR" "TXT" "DOV" "CL" "CPB" "GS" "ACN" "GDDY" "HD" "MET" "WM" "UPS" "BX" "JNJ" "CCI" "CB" "HUBB" "BBY" "WMT" "DD" "DG" "EMR" "ORCL" "COST" "PPG" "COO" "KHC" "AAPL" "JBHT" "GM" "PM" "BDX" "GIS" "GILD" "MS" "IEX" "HPQ" "USB" "F" "MRK" "BR" "DE" "ECL" "DTE" "TAP" "STT" "ES" "FE" "NRG" "WEC" "GOOG" "GOOGL" "JNPR" "HSY" "K" "CRM" "PNC" "LNT" "C" "REG" "DVA" "PG" "MSFT" "DAL" "NEM" "CMCSA" "CAH" "ABT" "YUM" "MCD" "CNP" "AMT" "IT" "LW" "TSN" "FDX" "WRB" "PSA" "NKE" "PPL" "SYY" "EXC" "CI" "AEP" "NEE" "EW" "KO" "PEP" "MSI" "IBM" "AMZN" "AES" "NWS" "NWSA" "WTW" "PNR" "APA" "FCX" "PKG" "HAL" "SLB" "CSCO" "LUV" "SHW" "AFL" "GLW" "PCG" "KIM" "VTR" "INTC" "CMG" "CPT" "MGM" "CFG" "GEN" "VZ" "BAC" "MSCI" "APD" "MKC" "EQR" "JPM" "CF" "LH" "CBOE" "BIO" "COP" "IRM" "CAG" "HLT" "INVH" "CSX" "RL" "TROW" "WYNN" "NTRS" "NOC" "ZTS" "ROST" "ETSY" "BIIB" "NDAQ" "TXN" "TMUS" "PGR" "DPZ" "AVGO" "BG" "JCI" "MNST" "SCHW" "PNW" "TRGP" "MTD" "AVY" "CDW" "AIG" "GE" "T" "WFC" "INTU" "AAL" "PYPL" "MPC" "AOS" "NSC" "DFS" "LVS" "BK" "CZR" "BSX" "MA" "CHTR" "ABBV" "STE" "AIZ" "MKTX" "SO" "RF" "COF" "TYL" "PANW" "V" "CCL" "DHR" "GPC" "JBL" "CDNS" "TER" "MDLZ" "HON" "ALGN" "CVX" "EMN" "CRL" "MHK" "DUK" "AJG" "TMO" "HCA" "STZ" "MCK" "WAB" "QCOM" "CMI" "TRV" "IPG" "VRTX" "ICE" "LYB" "DLR" "AON" "ADP" "ITW" "WBA" "SRE" "ZBH" "IP" "AMP" "FTV" "RCL" "MMM" "MOH" "CLX" "HPE" "HIG" "TDG" "EXR" "AXON" "LMT" "PHM" "HRL" "OKE" "XYL" "ARE" "AVB" "AXP" "MRO" "ROL" "ZBRA" "NCLH" "BLK" "REGN" "A" "ADI" "ROP" "NVDA" "WST" "SBAC" "DIS" "BEN" "AME" "DECK" "DHI" "TFX" "EFX" "BAX" "EPAM" "NXPI" "ALL" "CME" "MOS" "MTCH" "UHS" "KEYS" "TJX" "BWA" "PFG" "LKQ" "IFF" "EL" "BXP" "NUE" "MU" "O" "TPR" "D" "RSG" "ADSK" "DGX" "ANSS" "DLTR")
# tickers=("BA" "MCO" "KKR" "AZO")
tickers=("UAL" "EQT" "EA" "HII" "PSX" "VMC" "CAT" "EBAY" "BMY" "SPG" "MTB" "KEY" "XOM" "TGT" "PFE" "HUM" "KR" "TXT" "DOV" "CL" "CPB" "GS" "ACN" "GDDY" "HD" "MET" "WM" "UPS" "BX" "JNJ" "CCI" "CB" "HUBB" "BBY" "WMT" "DD" "DG" "EMR" "ORCL" "COST" "PPG" "COO" "KHC" "AAPL" "JBHT" "GM" "PM" "BDX" "GIS" "GILD" "MS" "IEX" "HPQ" "USB" "F" "MRK" "BR" "DE" "ECL" "DTE" "TAP" "STT" "ES" "FE" "NRG" "WEC" "GOOG" "GOOGL" "JNPR" "HSY" "K" "CRM" "PNC" "LNT" "C" "REG" "DVA" "PG" "MSFT" "DAL" "NEM" "CMCSA" "CAH" "ABT" "YUM" "MCD" "CNP" "AMT" "IT" "LW" "TSN" "FDX" "WRB" "PSA" "NKE" "PPL" "SYY" "EXC" "CI" "AEP" "NEE" "EW" "KO" "PEP" "MSI" "IBM" "AMZN" "AES" "NWS" "NWSA" "WTW" "PNR" "APA" "FCX" "PKG" "HAL" "SLB" "CSCO" "LUV" "SHW" "AFL" "GLW" "PCG" "KIM" "VTR" "INTC" "CMG" "CPT" "MGM" "CFG" "GEN" "VZ" "BAC" "MSCI" "APD" "MKC" "EQR" "JPM" "CF" "LH" "CBOE" "BIO" "COP" "IRM" "CAG" "HLT" "INVH" "CSX" "RL" "TROW" "WYNN" "NTRS" "NOC" "ZTS" "ROST" "ETSY" "BIIB" "NDAQ" "TXN" "TMUS" "PGR" "DPZ" "AVGO" "BG" "JCI" "MNST" "SCHW" "PNW" "TRGP" "MTD" "AVY" "CDW" "AIG" "GE" "T" "WFC" "INTU" "AAL" "PYPL" "MPC" "AOS" "NSC" "DFS" "LVS" "BK" "CZR" "BSX" "MA" "CHTR" "ABBV" "STE" "AIZ" "MKTX" "SO" "RF" "COF" "TYL" "PANW" "V" "CCL" "DHR" "GPC" "JBL" "CDNS" "TER" "MDLZ" "HON" "ALGN" "CVX" "EMN" "CRL" "MHK" "DUK" "AJG" "TMO" "HCA" "STZ" "MCK" "WAB" "QCOM" "CMI" "TRV" "IPG" "VRTX" "ICE" "LYB" "DLR" "AON" "ADP" "ITW" "WBA" "SRE" "ZBH" "IP" "AMP" "FTV" "RCL" "MMM" "MOH" "CLX" "HPE" "HIG" "TDG" "EXR" "AXON" "LMT" "PHM" "HRL" "OKE" "XYL" "ARE" "AVB" "AXP" "MRO" "ROL" "ZBRA" "NCLH" "BLK" "REGN" "A" "ADI" "ROP" "NVDA" "WST" "SBAC" "DIS" "BEN" "AME" "DECK" "DHI" "TFX" "EFX" "BAX" "EPAM" "NXPI" "ALL" "CME" "MOS" "MTCH" "UHS" "KEYS" "TJX" "BWA" "PFG" "LKQ" "IFF" "EL" "BXP" "NUE" "MU" "O" "TPR" "D" "RSG" "ADSK" "DGX" "ANSS" "DLTR")

# 循环运行任务
for ticker in "${tickers[@]}"; do
  echo "Running with ticker=$ticker"
  
  for i in "${!seq_lens[@]}"; do
    seq_len=${seq_lens[$i]}
    label_len=${label_lens[$i]}
    pred_len=${pred_lens[$i]}
    
    comment="TimeLLM-${ticker}"

    echo "Running ticker=$ticker with seq_len=$seq_len, label_len=$label_len, pred_len=$pred_len"

    accelerate launch --num_machines 1 --dynamo_backend 'no' --mixed_precision bf16 \
    --num_processes $num_process --main_process_port $master_port run_main.py \
      --task_name long_term_forecast \
      --is_training 1 \
      --root_path dataset/ticker_pricedata_2017/ \
      --data_path "${ticker}.csv" \
      --model_id "${ticker}_${seq_len}_${pred_len}" \
      --model "$model_name" \
      --data "$ticker" \
      --features S \
      --target DlyPrc \
      --seq_len "$seq_len" \
      --label_len "$label_len" \
      --pred_len "$pred_len" \
      --e_layers 2 \
      --d_layers 1 \
      --factor 3 \
      --enc_in 6 \
      --dec_in 6 \
      --c_out 6 \
      --batch_size "$batch_size" \
      --learning_rate "$learning_rate" \
      --llm_layers "$llama_layers" \
      --train_epochs "$train_epochs" \
      --model_comment "$comment"
  done
done