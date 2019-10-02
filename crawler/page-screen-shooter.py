# -*- coding: utf-8 -*-
"""
Created on Tue Dec 25 13:36:16 2018

@author: yyu
"""
from tqdm import tqdm
from browsermobproxy import Server
import os, sys
import datetime
import psutil
import time
import json
import requests
import pandas as pd

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

browser_mob_location = "D:\\Programs\\Browsermob\\bin\\browsermob-proxy"
chrome_driver_location = "D:\\Programs\\WebDrivers\\chromedriver.exe"
sitemap_location = "D:\\Emakina-Projects\\crawler\\crawler\\sitemaps\\prod3.txt"

screen_shot_save_location = "D:\\Emakina-Projects\\crawler\\crawler\\screenshots\\"
error_page_location = "D:\\Emakina-Projects\\crawler\\crawler\\404\\"

startingIndex = 0
errorPages = []

for proc in psutil.process_iter():
    # check whether the process name matches
    if proc.name() == "browsermob-proxy":
        proc.kill()

dict = {'port': 8090}
server = Server(path=browser_mob_location, options=dict)
server.start()
time.sleep(1)
proxy = server.create_proxy()
time.sleep(1)

proxy.new_har("pmi", options={'captureHeaders': True, 'captureCookies': True})

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--proxy-server={0}".format(proxy.proxy))
#chrome_options.add_argument("--user-data-dir={0}".format('C:\\Users\\yyu\\AppData\\Local\\Google\\Chrome\\User Data\\'))
#chrome_options.add_argument("--profile-directory={0}".format('Profile 5'))
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--log-level=3")

driver = webdriver.Chrome(executable_path=chrome_driver_location,chrome_options=chrome_options)

with open(sitemap_location, encoding="utf-8") as f:
    pages = f.readlines()
    pages = [x.strip() for x in pages]

with tqdm(total=len(pages)) as pbar:
    for i, page in enumerate(pages):
        
        pbar.update(1)
        pbar.set_description("Processing")

        if(i >= startingIndex ):
            #print('Crawling ' + str(i) + '/' + str(total_pages) + ' URL: ' + page)

            driver.get(page)

            page_result = requests.get(page)
            
            if(page_result.status_code != 200):
                errorPages.append(page)    

            total_width = 1920
            total_height = driver.execute_script("return document.body.scrollHeight") + 200

            # current_position = 0
            
            # while(current_position <= total_height):
            #     current_position += 100
            #     driver.execute_script("window.scrollTo(0, " + str(current_position) + ");")

            try:
                driver.execute_script('document.getElementsByClassName("optanon-alert-box-wrapper")[0].style.visibility = "hidden"')
            except:
                pass

            driver.set_window_size(total_width, total_height)

            time.sleep(5)

            driver.save_screenshot(screen_shot_save_location + "{0}.png".format(i+1))

with open(error_page_location + '404.txt', 'w') as file:
    for item in errorPages:
        file.write("%s\n" % item)

server.stop()
driver.quit()