# JngMkk
import pandas as pd
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time
import requests

driver = webdriver.Firefox(executable_path="")

# 오늘의 집
url = "https://ohou.se/productions/feed?query=%EC%8B%A4%EB%82%B4%20%EC%8B%9D%EB%AC%BC&order=buy&category_id=11060004"
driver.get(url)
time.sleep(10)

html = driver.page_source
soup = bs(html, 'html.parser')
items = soup.select(".production-feed__item-wrap.col-6.col-md-4.col-lg-3")
today_href = []
today_title = []
for item in items:
    today_href.append("https://ohou.se" + item.select_one(".production-item__overlay")['href'])
    today_title.append(item.select_one(".production-item__header__name").text)
driver.execute_script('window.scrollTo(0, 2000)')
time.sleep(10)
html = driver.page_source
soup = bs(html, 'html.parser')
items = soup.select(".production-feed__item-wrap.col-6.col-md-4.col-lg-3")
for item in items:
    if "https://ohou.se" + item.select_one(".production-item__overlay")['href'] in today_href:
        continue
    else:
        today_href.append("https://ohou.se" + item.select_one(".production-item__overlay")['href'])
        today_title.append(item.select_one(".production-item__header__name").text)
if len(today_href) < 30:
    driver.execute_script("window.scrollTo(2000, 3000)")
    time.sleep(10)
    html = driver.page_source
    soup = bs(html, 'html.parser')
    items = soup.select(".production-feed__item-wrap.col-6.col-md-4.col-lg-3")
    for item in items:
        if "https://ohou.se" + item.select_one(".production-item__overlay")['href'] in today_href:
            continue
        else:
            today_href.append("https://ohou.se" + item.select_one(".production-item__overlay")['href'])
            today_title.append(item.select_one(".production-item__header__name").text)

# coupang
url = "https://www.coupang.com/np/search?rocketAll=false&q=%EC%8B%A4%EB%82%B4+%EC%8B%9D%EB%AC%BC&brand=&offerCondition=&filter=1%23attr_11379%2429216%2C29217%2C3870%2C29218%2C31529%2C29220%2C31530%40DEFAULT&availableDeliveryFilter=&filterType=&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=user&backgroundColor=&searchProductCount=1829&component=&rating=0&sorter=saleCountDesc&listSize=30"
html = requests.get(url).text
soup = bs(html, 'html.parser')
items = soup.select(".search-product ")
coupang_href = []
coupang_title = []
for item in items:
    coupang_href.append("coupang.com" + item.find("a")['href'])
    coupang_title.append(item.find("img")['alt'])

# 11번가
url = "https://search.11st.co.kr/Search.tmall?kwd=%25EC%258B%25A4%25EB%2582%25B4%25EC%258B%259D%25EB%25AC%25BC#chkCtgrNo%%1003050%%%EA%BD%83/%EC%8B%9D%EB%AC%BC%%13$$pageNum%%1%%page%%14$$sortCd%%A%%%EB%88%84%EC%A0%81%20%ED%8C%90%EB%A7%A4%EC%88%9C%%29"
driver.get(url)
time.sleep(10)
html = driver.page_source
soup = bs(html, 'html.parser')
items = soup.select("section.search_section > ul > li")
href_11st = []
title_11st = []
for i in range(30):
    href_11st.append(items[i].select_one("a")['href'])
    title_11st.append(items[i].select_one("strong").text)

# 옥션
url = "http://browse.auction.co.kr/search?keyword=%ec%8b%a4%eb%82%b4%ec%8b%9d%eb%ac%bc&itemno=&nickname=&frm=hometab&dom=auction&isSuggestion=No&retry=&Fwk=%ec%8b%a4%eb%82%b4%ec%8b%9d%eb%ac%bc&acode=SRP_SU_0100&arraycategory=&encKeyword=%ec%8b%a4%eb%82%b4%ec%8b%9d%eb%ac%bc&s=8"
requests.get(url)
html = requests.get(url).text
soup = bs(html, 'html.parser')
items = soup.select("div.section--itemcard")
auction_href = []
auction_title = []
for i in range(30):
    auction_href.append(items[i].select_one('a')['href'])
    auction_title.append(items[i].select_one('span.text--title').text)

df = pd.DataFrame([today_href[:30], today_title[:30],
                    coupang_href, coupang_title,
                    href_11st, title_11st,
                    auction_href, auction_title]).T
df.columns = ['오늘의집상품URL', '오늘의집상품이름',
                '쿠팡상품URL', '쿠팡상품이름',
                '11번가상품URL', '11번가상품이름',
                '옥션상품URL', '옥션상품이름']

df.to_csv("./data/shop_top30.csv", encoding="utf-8")
