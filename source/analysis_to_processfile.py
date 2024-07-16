import csv

def process_analyzed_comments(input_csv, output_csv):
    # Read the input CSV file
    with open(input_csv, mode='r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        comments = [row for row in reader]
    
    processed_comments = []
    for comment in comments:
        result = {'date': comment['date'], 'comment': comment['comment']}
        
        # Extract relevant scores and convert them to 0-100 scale
        scores = {
            '여성/가족': float(comment.get('여성/가족', 0)) * 100,
            '남성': float(comment.get('남성', 0)) * 100,
            '성소수자': float(comment.get('성소수자', 0)) * 100,
            '인종/국적': float(comment.get('인종/국적', 0)) * 100,
            '연령': float(comment.get('연령', 0)) * 100,
            '지역': float(comment.get('지역', 0)) * 100,
            '종교': float(comment.get('종교', 0)) * 100,
            '기타 혐오': float(comment.get('기타 혐오', 0)) * 100,
            '악플/욕설': float(comment.get('악플/욕설', 0)) * 100,
            'clean': float(comment.get('clean', 0)) * 100
        }
        
        # Find the label with the maximum score
        max_label = max(scores, key=scores.get)
        max_value = round(scores[max_label])
        
        result.update({
            'maxname': max_label,
            'maxvalue': max_value
        })
        
        processed_comments.append(result)
    
    # Define the fieldnames for the output CSV
    fieldnames = ['date', 'comment', 'maxname', 'maxvalue']
    
    # Write the processed data to the output CSV file
    with open(output_csv, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for processed_comment in processed_comments:
            writer.writerow(processed_comment)
    
    print(f'Processed analysis results have been written to {output_csv}')

# Example usage
input_csv = '2006-2023_analyzed_comments2.csv'
output_csv = '2006-2023_processed_comments.csv'
process_analyzed_comments(input_csv, output_csv)
