from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from bs4 import BeautifulSoup
import os
import chromedriver_autoinstaller
import pandas as pd
import numpy as np
import re
import time
import requests as rq
import json

chromedriver_autoinstaller.install()

queries = ["machine+learning", "datascience", "kaggle"]
url = "https://www.youtube.com/results?search_query={query}&p={page}"

options = webdriver.ChromeOptions()
prefs = {''
         "download.default_directory": r"%s" % ('C:\\'),
         "download.prompt_for_download": False,
         "download.directory_upgrade": True
         }

options.add_experimental_option('prefs', prefs)
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--allow-running-insecure-content")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-extensions")
options.add_argument("--proxy-server='direct://'")
options.add_argument("--proxy-bypass-list=*")
options.add_argument("--start-maximized")
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--ignore-certificate-errors')
driver = webdriver.Chrome(chrome_options=options)
# exibir o google chrome [descomentar a de baixo e comentar a de cima]
# driver = webdriver.Chrome("chromedriver.exe",chrome_options=options)

for query in queries:
    for page in range(1, 101):
        urll = url.format(query=query, page=page)
        print(urll)
        driver.get(urll)
        response = driver.page_source

        with open("./dados_brutos/{}_{}.html".format(query, page), "w+", encoding="utf-8") as output:
            output.write(response)

for query in queries:
    for page in range(1, 101):
        with open("./dados_brutos/{}_{}.html".format(query, page), "r+", encoding="utf-8") as inp:
            page_html = inp.read()
            parsed = BeautifulSoup(page_html)
            tags = parsed.findAll("a", {"id": "video-title"})

            for e in tags:
                if e.has_attr("aria-label"):
                    link = e['href']
                    title = e['title']
                    with open("parsed_videos_full.json", "a+") as output:
                        data = {"link": link, "title": title, "query": query}
                        output.write("{}\n".format(json.dumps(data)))
