import requests
from bs4 import BeautifulSoup
from datetime import datetime
from .gpt import get_ai_response
import re
import aiohttp
import asyncio


async def fetch_html(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.text()
    except (aiohttp.ClientError, asyncio.TimeoutError) as e:
        print(f"Error fetching HTML from {url}: {e}")
        return None


async def CrawlDepartment(dm):
    data = []
    code = dm[0]
    number = dm[1]

    list_url = f"https://inu.ac.kr/bbs/{code}/{number}/artclList.do"
    html = await fetch_html(list_url)

    soup = BeautifulSoup(html, "html.parser")

    notice_list = soup.select("body table tbody > tr:not(.notice)")
    today = datetime.now().strftime("%Y.%m.%d")
    today = "2024.04.30"

    for notice in notice_list:
        posted_at = (
            notice.select_one(".td-date").text.strip()
            if notice.select_one(".td-date")
            else ""
        )
        if today == posted_at:
            notice_url = "https://inu.ac.kr" + notice.select_one(".td-subject > a").get("href")
            title = notice.select_one(".td-subject strong").text

            html = await fetch_html(notice_url)
            content = BeautifulSoup(html, "html.parser").select_one(".view-con")
            
            if content:
                content_text = re.sub(r"(\n)+", "\n", re.sub(r"\t|\xa0", "", content.text))

                if img := content.select("p img"):
                    img_url = [i.get("src") for i in img]
                else:
                    img_url = []

                ai_text = re.sub(r'\n', '', BeautifulSoup(html, "html.parser").select_one("._fnctWrap").text)
                
                deadline = await get_ai_response(ai_text, img_url)
                
                if deadline == "":
                    is_classified = False
                else:
                    is_classified = True

                data.append(
                    {
                        "category_id": number,
                        "title": title,
                        "content": content_text,
                        "img_url": img_url,
                        "posted_at": posted_at,
                        "deadline": deadline,
                        "isclassified": is_classified,
                        "notice_url": notice_url,
                    }
                )
                
    return data


async def CrawlNotice(department):
    tasks = [CrawlDepartment(dm) for dm in department]
    results = await asyncio.gather(*tasks)
    return sum(results, [])
