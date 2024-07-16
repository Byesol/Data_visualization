import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime, timedelta

def get_weekly_best_comments(date):
    targeted_url = f'https://news.nate.com/comment?type=best&mid=n1501&sect_id=&p=week&ymd={date}'
    requested = requests.get(targeted_url)
    soup = BeautifulSoup(requested.text, 'html.parser')
    
    iframe = soup.find('iframe', id='ifr_reple')
    if iframe:
        iframe_url = 'https:' + iframe['src']
        iframe_response = requests.get(iframe_url)
        iframe_soup = BeautifulSoup(iframe_response.text, 'html.parser')
        
        jreplyList = iframe_soup.find('div', class_='jreplyList jreplyLast')
        comments = []
        
        if jreplyList:
            jreply_wraps = jreplyList.find_all('div', class_='jreplyWrap')
            for jreply_wrap in jreply_wraps:
                usertxt_elements = jreply_wrap.find_all('dd', class_='usertxt')
                for usertxt in usertxt_elements:
                    comment = usertxt.text.strip()
                    comments.append({'date': date[:7], 'comment': comment})  # YYYY-MM 형식
        return comments
    else:
        print("Iframe not found")
        return []

def generate_weekly_comments_csv(start_year, start_month, end_year, end_month):
    start_date = datetime(start_year, start_month, 1)
    end_date = datetime(end_year, end_month, 1)
    delta = timedelta(days=7)
    
    filename = f'weekly_best_comments_{start_year}_{start_month}_to_{end_year}_{end_month}.csv'
    fieldnames = ['date', 'comment']
    
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        
        current_date = start_date
        while current_date <= end_date:
            date_str = current_date.strftime('%Y-%m-%d')
            comments = get_weekly_best_comments(date_str)
            for comment in comments:
                writer.writerow(comment)
            current_date += delta

    print(f'Weekly best comments from {start_year}-{start_month} to {end_year}-{end_month} have been written to {filename}')

# 2023년 5월부터 2024년 5월까지의 주간 베스트 댓글을 CSV 파일로 생성
generate_weekly_comments_csv(2013, 1, 2023, 12)


