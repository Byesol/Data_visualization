import csv
import torch
from transformers import TextClassificationPipeline, BertForSequenceClassification, AutoTokenizer

# Load the sentiment analysis model and tokenizer
model_name = 'smilegate-ai/kor_unsmile'
device = 0 if torch.cuda.is_available() else -1

model = BertForSequenceClassification.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

pipe = TextClassificationPipeline(
    model=model,
    tokenizer=tokenizer,
    device=device,
    top_k=None,  # Use top_k=None to get all scores
    function_to_apply='sigmoid'
)

def truncate_text(text, tokenizer, max_length):
    # Tokenize and truncate the text to the max length
    tokens = tokenizer(text, truncation=True, max_length=max_length, padding=False, return_tensors='pt')
    return tokenizer.decode(tokens['input_ids'][0], skip_special_tokens=True)

def analyze_comments(input_csv, output_csv, max_length=300):
    # Read the input CSV file
    with open(input_csv, mode='r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        comments = [row for row in reader]
    
   
    analyzed_comments = []
    for comment in comments:
        truncated_comment = truncate_text(comment['comment'], tokenizer, max_length)
        analysis = pipe(truncated_comment)
        result = {'date': comment['date'], 'comment': comment['comment']}
        for score in analysis[0]:
            result[score['label']] = score['score']
        analyzed_comments.append(result)
    
   
    fieldnames = ['date', 'comment', '여성/가족', '남성', '성소수자', '인종/국적', '연령', '지역', '종교', '기타 혐오', '악플/욕설', 'clean']
    
    # Write the analyzed data to the output CSV file
    with open(output_csv, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for analyzed_comment in analyzed_comments:
            writer.writerow(analyzed_comment)
    
    print(f'Analysis results have been written to {output_csv}')

# Example usage
input_csv = 'weekly_best_comments_2006_1_to_2024_1.csv'

output_csv = '2006-2023_analyzed_comments2.csv'
analyze_comments(input_csv, output_csv)
