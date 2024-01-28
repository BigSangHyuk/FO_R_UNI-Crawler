import requests
from bs4 import BeautifulSoup
from datetime import datetime

def getHtml(url):
    res = requests.get(url)
    
    html = res.text
    
    soup = BeautifulSoup(html, 'html.parser')
    
    return soup

def CrawlNotice(code, number):
    data = []
    
    list_url = f'https://inu.ac.kr/bbs/{code}/{number}/artclList.do'

    soup = getHtml(list_url)

    notice_list = soup.select('body table tbody > tr:not(.notice)')
    today = datetime.now().strftime("%Y.%m.%d")
    today = '2024.01.22'
    
    for notice in notice_list:
        posted_at = notice.select_one('.td-date').text.strip()
        if today == posted_at:
            
            notice_url = 'https://inu.ac.kr' + notice.select_one('.td-subject > a').get('href')

            title = notice.select_one('.td-subject strong').text
            
            writer = notice.select_one('.td-write').text.strip()
            
            soup = getHtml(notice_url)
            
            content = soup.select_one('.view-con').text
            
            data.append({'category_id':number, 'title':title, 'content':content, 'img_url':'', 'posted_at':posted_at, 'deadline':''})
            
    return data