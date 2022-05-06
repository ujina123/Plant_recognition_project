# JngMkk
import urllib.request as req
import urllib
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time
import os

driver = webdriver.Firefox(executable_path="../geckodriver")

def scroll() :
    last_page_height = driver.execute_script("return document.documentElement.scrollHeight")
    while True:
        driver.execute_script('window.scrollTo(0, document.documentElement.scrollHeight)')
        time.sleep(7)
        new_page_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_page_height == last_page_height:
            break
        last_page_height = new_page_height

name = []           # 한글검색
eng_name = []       # 영어검색
dir_name = []       # 폴더이름
quote_name = []     # 한글 url quote

for n, dir in zip(name, dir_name):
    os.system(f"mkdir -p ./image/{dir}")
    quote_name.append(urllib.parse.quote(n))

for x, y, z in zip(eng_name, quote_name, dir_name):
    srcs = []
    # 구글 영어검색
    url = f"https://www.google.com/search?q={x}"
    driver.get(url)
    time.sleep(7)
    driver.find_element_by_css_selector("div.hdtb-mitem:nth-child(2) > a:nth-child(1)").click()
    time.sleep(7)
    while True:
        scroll()
        try:
            driver.find_element_by_class_name("mye4qd").click()
        except Exception as e:
            print(e)
            break
    html = driver.page_source
    soup = bs(html, 'html.parser')
    items = soup.select(".isv-r.PNCib.MSM1fd.BUooTd")
    for item in items:
        if "src" in item.select_one("img").attrs:
            srcs.append(item.select_one("img")['src'])
        elif "data-src" in item.select_one("img").attrs:
            srcs.append(item.select_one("img")['data-src'])
        else:
            continue
    
    # 구글 한국어검색
    url = f"https://www.google.com/search?q={y}"
    driver.get(url)
    time.sleep(7)
    driver.find_element_by_css_selector("div.hdtb-mitem:nth-child(2) > a:nth-child(1)").click()
    time.sleep(7)
    while True:
        scroll()
        try:
            driver.find_element_by_class_name("mye4qd").click()
        except Exception as e:
            print(e)
            break
    html = driver.page_source
    soup = bs(html, 'html.parser')
    items = soup.select(".isv-r.PNCib.MSM1fd.BUooTd")
    for item in items:
        if "src" in item.select_one("img").attrs:
            src = item.select_one("img")["src"]
            if src in srcs:
                continue
            else:
                srcs.append(src)                
        elif "data-src" in item.select_one("img").attrs:
            src = item.select_one("img")['data-src']
            if src in srcs:
                continue
            else:
                srcs.append(src)
        else:
            continue
    
    url = f"https://www.bing.com/images/search?q={x}"
    driver.get(url)
    time.sleep(7)
    while True:
        scroll()
        try:
            driver.find_element_by_class_name("btn_seemore").click()
        except Exception as e:
            print(e)
            break
    html = driver.page_source
    soup = bs(html, "html.parser")
    items = soup.select("div.img_cont.hoff")
    for item in items:
        src = item.select_one("img")["src"]
        if src in srcs:
            continue
        else:
            srcs.append(src)
    
    url = f"https://www.bing.com/images/search?q={y}"
    driver.get(url)
    time.sleep(7)
    while True:
        scroll()
        try:
            driver.find_element_by_class_name("btn_seemore").click()
        except Exception as e:
            print(e)
            break
    html = driver.page_source
    soup = bs(html, "html.parser")
    items = soup.select("div.img_cont.hoff")
    for item in items:
        src = item.select_one("img")["src"]
        if src in srcs:
            continue
        else:
            srcs.append(src)
    
    # 네이버 한글 검색
    url = f"https://search.naver.com/search.naver?where=nexearch&ie=utf8&query={y}"
    driver.get(url)
    time.sleep(7)
    if driver.find_element_by_css_selector("ul.base > li:nth-child(2) > a").text == "이미지":
        driver.find_element_by_css_selector("ul.base > li:nth-child(2)").click()
    else:
        driver.find_element_by_css_selector("ul.base > li:nth-child(3)").click()
    time.sleep(7)
    scroll()
    html = driver.page_source
    soup = bs(html, "html.parser")
    items = soup.select(".tile_item._item")
    for item in items:
        if item.select_one("img"):
            if item.select_one("img")["src"] in srcs:
                continue
            else:
                srcs.append(item.select_one("img")["src"])
        else:
            continue
    cnt = 1
    for s in srcs:
        try:
            req.urlretrieve(s, f"./image/{z}/{z}{cnt}.png")
            cnt += 1
        except Exception as e:
            print(e)
            continue
