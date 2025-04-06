import pandas as pd

# Read the CSV data (assuming it's in a file named 'input.csv')
df = pd.read_csv('BA_price.csv')

# Extract the DlyPrc column values
dlyprc_values = df['DlyPrc'].tolist()

# Split into chunks of 10 and 2 alternately
seq_len = []
pred_len = []
i = 0

while i + 24 <= len(dlyprc_values):  # 确保有完整的 10 + 2 数据
    # 取10个作为 seq_len
    seq_len.append(dlyprc_values[i:i+20])
    i += 20
    
    # 取2个作为 pred_len
    pred_len.append(dlyprc_values[i:i+4])
    i += 4

# 创建DataFrame
result = pd.DataFrame({
    'seq_len': seq_len,
    'pred_len': pred_len
})

# Save to a new CSV file
result.to_csv('BA_20_4_price.csv', index=False)

print("Processing complete. Results saved to output.csv")