""" Created on 4 August 2023
    Author: Lavinia Nongbri

    this code is to extract the articles from PIB
    Language - Hindi and Manipuri
               Manipuri and English"""


# importing packages
from bs4 import BeautifulSoup as bs
import requests
import os
import re
import sys

source_lang = 'mni'

# storing the arguments by slicing out the 0 index which holds the file name.
arguments = sys.argv[1:]
domain = arguments[0]
date = arguments[1]
month = arguments[2]
year = arguments[3]
lang = arguments[4]
file_path = arguments[5]

# importing file containing links
file = open(file_path,'r').read()

# converting to list
links = file.split("\n")

# using remove() to
# perform removal
while "" in links:
    links.remove("")

path = r"Z:\lavinia"

folder_path = os.path.join(path, domain)
file_name = domain+'-'+date+'-'+month+'-'+year

# split_file_name = os.path.splitext(file_path)[0]

# save_eng_links_file = split_file_name+'eng.txt'

target_links_text = file_name+'-'+lang+'-links.txt'

target = open(os.path.join(folder_path,target_links_text), 'w', encoding='utf-8')

count_articles = 0  # count the links


# function to check if the same article is published in english, if yes then get the link

def search_lang(link, target_lang):
    r = requests.get(link)
    soup = bs(r.content, 'html5lib')  # If this line causes an error, run 'pip install html5lib' or install html5lib
    # print(soup.prettify())
    content = soup.find("div", class_="innner-page-main-about-us-content-right-part")

    release_lang = content.find("div", class_="ReleaseLang")

    # lang = []

    for a in release_lang.find_all('a'):
        # l = a.get_text().strip()
        # lang.append(l)

        if target_lang in a.get_text().lower():
            status = True
            t_link = a.get('href')
            target.write(t_link + '\n')

    return status, t_link

# function to scrap the contents of the articles


def scrap_articles(link, language, count):

    text_file_name = file_name+'-'+str(count)+'-'+language+'-'+'.txt'

    article_file_path = os.path.join(folder_path, text_file_name)

    article = open(article_file_path, 'w', encoding="utf-8")

    r = requests.get(link)
    soup = bs(r.content, 'html5lib')  # If this line causes an error, run 'pip install html5lib' or install html5lib
    # print(soup.prettify())

    content = soup.find("div", class_="innner-page-main-about-us-content-right-part")

    for tags in content.find_all(re.compile('^h[1-6]')):
        print(tags.text.strip())
        t = tags.text.strip()
        article.write(t + "\n")

    # extracting the main contents
    # getting all the paragraphs
    for para in content.find_all("p"):
        print(para.get_text())
        para_text = para.get_text()
        article.write(para_text + "\n")

    article.close()


for each_link in links:

    count_articles += 1
    result = search_lang(each_link, lang)
    if result[0] is True:
        scrap_articles(each_link, source_lang, count_articles)
        scrap_articles(result[1], lang, count_articles)

target.close()