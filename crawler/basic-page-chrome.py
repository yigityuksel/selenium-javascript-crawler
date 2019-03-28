# -*- coding: utf-8 -*-
"""
Created on Tue Dec 25 13:36:16 2018

@author: baa
"""

from browsermobproxy import Server
import os, sys
import datetime
import psutil
import time
import json

for proc in psutil.process_iter():
    # check whether the process name matches
    if proc.name() == "browsermob-proxy":
        proc.kill()

def writeToFile(filename,content):
    _dir = os.path.dirname('__file__') 
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M')
    relative = "har/" + filename + " - "+ timestamp + ".json"
    path = os.path.join(_dir, relative)    
    f= open(path,"w+")
    f.write(content)


dict = {'port': 8090}
server = Server(path="D:\\Programs\\Browsermob\\bin\\browsermob-proxy", options=dict)
server.start()
time.sleep(1)
proxy = server.create_proxy()
time.sleep(1)

from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--proxy-server={0}".format(proxy.proxy))
chrome_options.add_argument("--user-data-dir={0}".format('C:\\Users\\yyu\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 1'))
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(executable_path="D:\\Programs\\WebDrivers\\chromedriver.exe",chrome_options=chrome_options)

full_log = []
warning_log = []
severe_log = []
javascript_log = []

with open('page-list.txt') as f:
    pages = f.readlines()
    pages = [x.strip() for x in pages]

proxy.new_har("pmi", options={'captureHeaders': True, 'captureCookies': True})
total_pages = len(pages)
for i, page in enumerate(pages):
    print('Crawling ' + str(i) + '/' + str(total_pages) + ' URL: ' + page)
    try:
        driver.get(page)

        # SCROLL_PAUSE_TIME = 5.5
        # index = 0

        # bodyHeight = driver.execute_script("return document.body.clientHeight")
        # clientHeight = driver.execute_script("return document.documentElement.clientHeight")
        
        # page_height = int(bodyHeight)
        # client_height = int(clientHeight)
        # max_bound = int(page_height / client_height)
      
        # while max_bound >= index:

        #     driver.save_screenshot("D:\\Emakina-Projects\\crawler\\crawler\\screenshots\\{0}.png".format(index))         
        #     time.sleep(SCROLL_PAUSE_TIME)
        #     driver.execute_script("window.scrollTo(0,window.scrollY+window.innerHeight*.9)")
        #     index += 1

        browser_log = driver.get_log('browser')
        for i in browser_log:        
            log = {
                "Url" : page,
                "Error" : i["level"],
                "Source" : i["source"],
                "Message" : i["message"]
            }
            
            if(i["level"] == "WARNING"):
                warning_log.append(log)
            elif(i["level"] == "SEVERE" and i["source"] == "javascript"):
                javascript_log.append(log)
            else:
                severe_log.append(log)

        full_log.append({
            "Url" : page,
            "Error" : browser_log
        })

    except:
        print("\t\tCrawling failed for page: " + page)

#writeToFile(json.dumps(proxy.har))
writeToFile("FULL",json.dumps(full_log))
writeToFile("WARNING",json.dumps(warning_log))
writeToFile("SEVERE",json.dumps(severe_log))
writeToFile("SEVERE_JAVASCRIPT",json.dumps(javascript_log))


server.stop()
driver.quit()