import pandas as pd
from transformers import AutoModelForCausalLM, AutoTokenizer
from tqdm import tqdm

# Initialize model and tokenizer
model_name = "DeepSeek-R1-Distill-Qwen-1.5B"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto")

# Configuration
MAX_TOKENS = 2048
PROMPT_RESERVE = 300
CHUNK_SIZE = MAX_TOKENS - PROMPT_RESERVE
TARGET_LENGTH = (100, 150)  # Character length range

def count_tokens(text):
    return len(tokenizer.encode(text, add_special_tokens=False))

def refine_summary(initial_summary, max_attempts=3):
    """Iteratively refine summary to reach target length"""
    current_summary = initial_summary
    attempts = 0
    
    while attempts < max_attempts:
        current_len = len(current_summary)
        
        if TARGET_LENGTH[0] <= current_len <= TARGET_LENGTH[1]:
            return current_summary
        
        # Determine refinement prompt based on length
        if current_len > TARGET_LENGTH[1]:
            instruction = f"Condense this summary to {TARGET_LENGTH[1]} characters max while preserving key information:"
        else:
            instruction = f"Expand this summary to at least {TARGET_LENGTH[0]} characters while adding key details:"
        
        prompt = f"{instruction}\n\nSummary: {current_summary}\n\nRevised Summary:"
        
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=MAX_TOKENS).to("cuda")
        outputs = model.generate(
            **inputs,
            max_new_tokens=150,
            temperature=0.7,
            do_sample=True
        )
        
        new_summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
        new_summary = new_summary.replace(prompt, "").strip()
        
        # Prevent infinite loops
        if new_summary == current_summary:
            break
            
        current_summary = new_summary
        attempts += 1
    
    # Final length adjustment if still not in range
    if len(current_summary) > TARGET_LENGTH[1]:
        return current_summary[:TARGET_LENGTH[1]]
    return current_summary

def generate_summary(title, snippet, body):
    prompt_template = """You are an expert financial analyst with deep knowledge of stock markets, economic indicators, and corporate finance. Generate a professional news summary for financial professionals with these requirements:

1. Length: 100-150 words
2. Focus on financial implications: Highlight market impacts, stock reactions, and economic significance
3. Key elements must include:
   - Affected companies/stocks (with tickers if available)
   - Relevant market indices
   - Financial figures (percentages, valuations, etc.)
   - Policy/regulatory implications
4. Maintain analytical tone while being concise
5. Flag any potential market-moving information

### Input:
Title: {title}
Snippet: {snippet}
Body: {body}

### Output (Financial Summary):
[For important market-moving news, begin with "MARKET-SENSITIVE:"]
"""
    # Split body if too long
    body_chunks = []
    if count_tokens(body) > CHUNK_SIZE:
        body_words = body.split()
        current_chunk = []
        current_length = 0
        
        for word in body_words:
            word_length = count_tokens(word)
            if current_length + word_length <= CHUNK_SIZE:
                current_chunk.append(word)
                current_length += word_length
            else:
                body_chunks.append(" ".join(current_chunk))
                current_chunk = [word]
                current_length = word_length
        if current_chunk:
            body_chunks.append(" ".join(current_chunk))
    else:
        body_chunks = [body]

    # Generate initial summary
    summaries = []
    for chunk in body_chunks:
        prompt = prompt_template.format(title=title, snippet=snippet, body=chunk)
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=MAX_TOKENS).to("cuda")
        
        outputs = model.generate(
            **inputs,
            max_new_tokens=150,
            temperature=0.7,
            do_sample=True
        )
        
        summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
        summary = summary.replace(prompt, "").strip()
        summaries.append(summary)
    
    full_summary = " ".join(summaries)
    
    # Apply iterative refinement
    return refine_summary(full_summary)

# Process all 200 news articles
df = pd.read_csv("dataset/ticker/news_2017.csv")
results = []

for _, row in tqdm(df.iterrows(), total=len(df)):
    title = str(row['title']) if pd.notna(row['title']) else ""
    snippet = str(row['snippet']) if pd.notna(row['snippet']) else ""
    body = str(row['body']) if pd.notna(row['body']) else ""
    
    summary = generate_summary(title, snippet, body)
    results.append({
        'original_title': title,
        'original_body_length': len(body),
        'summary': summary,
        'summary_length': len(summary),
        'meets_length': TARGET_LENGTH[0] <= len(summary) <= TARGET_LENGTH[1]
    })

# Save results with verification
results_df = pd.DataFrame(results)
results_df.to_csv("refined_news_summaries.csv", index=False)

# Print quality report
success_rate = results_df['meets_length'].mean() * 100
print(f"Summarization completed. Success rate: {success_rate:.1f}% within target length")
print(f"Average summary length: {results_df['summary_length'].mean():.1f} characters")
print("Results saved to refined_news_summaries.csv")