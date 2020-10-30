from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium import webdriver
import chromedriver_autoinstaller
import pandas as pd
import numpy as np
import re
import time
import requests as rq
import bs4 as bs4
import tqdm
import glob
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

""" Coleta de Dadoos """

df = pd.read_json('parsed_videos_full.json', lines=True)
df.head()

lista_de_links = df['link'].unique()
len(lista_de_links)

url = "https://www.youtube.com{link}"

for link in lista_de_links:
    urll = url.format(link=link)
    print(urll)
    driver.get(urll)
    time.sleep(2)
    response = driver.page_source

    link_name = re.search("v=(.*)", link).group(1)

    with open("./dados_brutos/video_{}.html".format(link_name), 'w+', encoding="utf-8") as output:
        output.write(response)

with open("parsed_video_info.json", 'w+', encoding="utf-8") as output:
    for video_file in sorted(glob.glob("./dados_brutos/video*")):
        with open(video_file, 'r+', encoding="utf-8") as inp:
            page_html = inp.read()
            parsed = bs4.BeautifulSoup(page_html, 'html.parser')

            class_watch = parsed.find_all(
                attrs={"class": re.compile(r"watch")})
            id_watch = parsed.find_all(attrs={"id": re.compile(r"watch")})
            channel = parsed.find_all(
                "a", attrs={"href": re.compile(r"channel")})
            meta = parsed.find_all("meta")

            data = dict()

            for e in class_watch:
                colname = "_".join(e['class'])
                if "clearfix" in colname:
                    continue
                data[colname] = e.text.strip()

            for e in id_watch:
                colname = e['id']
                # if colname in output:
                #    print(colname)
                data[colname] = e.text.strip()

            for e in meta:
                colname = e.get('property')
                if colname is not None:
                    data[colname] = e['content']

            for link_num, e in enumerate(channel):
                data["channel_link_{}".format(link_num)] = e['href']

            output.write("{}\n".format(json.dumps(data)))

df = pd.read_json("parsed_video_info.json", lines=True)
print(df.shape)

pd.set_option("display.max_columns", 166)
print(df.head(1))

colunas_selecionadas = ['watch-title', 'watch-view-count', 'watch-time-text', 'content_watch-info-tag-list', 'watch7-headline',
                        'watch7-user-header', 'watch8-sentiment-actions', "og:image", 'og:image:width', 'og:image:height',
                        "og:description", "og:video:width", 'og:video:height', "og:video:tag", 'channel_link_0']

df[colunas_selecionadas].head()
df[colunas_selecionadas].to_feather("raw_data.feather")
df[colunas_selecionadas].to_csv("raw_data_sem_labels.csv")
