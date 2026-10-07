import os, requests, csv, time
from bs4 import BeautifulSoup as soup

from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

driver = webdriver.Chrome(executable_path="chromedriver.exe")
driver.set_window_size(100, 100)
driver.set_window_position(1300, 900)

def get_url_list():
    a = open("url_list.txt", "r+")
    b = [c for c in a]
    return b

def page_request(page_url):
    a = driver.get(page_url)
    time.sleep(0.5)
    b = driver.page_source
    return b

def soupify(page_content):
    a = soup(page_content)
    return a

def get_pagination(soup_content):
    a = soup_content.find("a", {"class": "gt999"})
    b = int(a.text)
    return b

def get_forum_title(soup_content):
    a = soup_content.find("h1")
    a = "_" + str(a.text).lower().replace(" ", "_")
    return a

def create_write_csv(forum_title):
    a = open(str(forum_title)+".csv", "a+")
    b = csv.writer(a)
    b.writerow(["replies","views","post_title","post_url","original_poster","original_date","last_poster","last_date"])
    return b

def one_time_per_url(url):
    a = page_request(str(url))
    b = soupify(a)
    c = get_pagination(b)
    d = create_write_csv(get_forum_title(b))
    return [c, d]

def get_page_list_items(soup_content):
    a = soup_content.findAll("li", {"class": "discussionListItem"})
    return a

def split_list_items(list_items, csv_writer):
    a = []
    for b in list_items:
        print(b)
        c = b.find("a", {"class": "PreviewTooltip"})
        print(c)
        try:
            d = "https://www.blackhatworld.com/" + str(c["href"])
            e = c.text
            f = b.find("span", {"class": "DateTime"}).text
            g = b.find("a", {"class": "username"}).text
            h = b.find("dl", {"class": "major"}).find("dd").text
            i = b.find("dl", {"class": "minor"}).find("dd").text
            j = b.find("dl", {"class": "lastPostInfo"})
            k = j.find("span", {"class": "DateTime"}).text
            l = j.find("a", {"class": "username"}).text
            print([h,i,e,d,g,f,k,l])
            csv_writer.writerow([h,i,e,d,g,f,k,l])
        except:
            pass

def loop_pages(num_pages, csv_writer, url):
    a = 2
    print(num_pages)
    while a < num_pages:
        print(a)
        b = page_request(url + "page-" + str(a))
        c = soupify(b)
        d = get_page_list_items(c)
        e = split_list_items(d, csv_writer)
        a+=1

def url_cycler():
    a = get_url_list()
    for b in a:
        print(b)
        c = one_time_per_url(str(b))
        loop_pages(c[0], c[1], str(b))

def init():
    url_cycler()

init()
