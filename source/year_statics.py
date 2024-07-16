import csv
from collections import defaultdict

def calculate_statistics(input_csv, output_csv):
    # Read the input CSV file
    with open(input_csv, mode='r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        comments = [row for row in reader]
    
    # Initialize a nested dictionary to count maxname occurrences per year
    stats = defaultdict(lambda: defaultdict(int))
    total_counts = defaultdict(int)
    
    for comment in comments:
        year = comment['date'][:4]
        maxname = comment['maxname']
        stats[year][maxname] += 1
        total_counts[year] += 1
    
    # Prepare data for output CSV
    output_data = []
    categories = ['여성/가족', '남성', '성소수자', '인종/국적', '연령', '지역', '종교', '기타 혐오', '악플/욕설', 'clean']
    
    for year, counts in stats.items():
        year_data = {'year': year}
        for category in categories:
            count = counts[category]
            total = total_counts[year]
            percentage = (count / total) * 100 if total > 0 else 0
            year_data[f'{category}_count'] = count
            year_data[f'{category}_percentage'] = round(percentage, 2)
        output_data.append(year_data)
    
    # Define the fieldnames for the output CSV
    fieldnames = ['year'] + [f'{category}_count' for category in categories] + [f'{category}_percentage' for category in categories]
    
    # Write the processed data to the output CSV file
    with open(output_csv, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for data in output_data:
            writer.writerow(data)
    
    print(f'Statistics have been written to {output_csv}')

# Example usage
input_csv = '2006-2023_processed_comments.csv'
output_csv = '2006-2023_yearly_statistics.csv'
calculate_statistics(input_csv, output_csv)
