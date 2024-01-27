import requests
from bs4 import BeautifulSoup
from datetime import datetime

def CrawlNotice(code, number):
    list_url = f'https://inu.ac.kr/bbs/{code}/{number}/artclList.do'
    res = requests.get(list_url)

    html = res.text
    soup = BeautifulSoup(html, 'html.parser')

    notice_list = soup.select('body table tbody > tr:not(.notice)')
    today = datetime.now().strftime("%Y.%m.%d")
    today = '2024.01.22'
    
    for notice in notice_list:
        if today == notice.select_one('.td-date').text.strip():
            
            notice_url = 'https://inu.ac.kr' + notice.select_one('.td-subject > a').get('href')

            title = notice.select_one('.td-subject strong').text
            
            writer = notice.select_one('.td-write').text.strip()
            
            res = requests.get(notice_url)

            html = res.text
            
            soup = BeautifulSoup(html, 'html.parser')
            
            detail = soup.select_one('.view-con').text
            print(detail)
            
CrawlNotice('isis', 376)