""" Created on 24 November 2023
    Author: Lavinia Nongbri

    this code is to perform data cleaning of the PIB articles
    Language - Manipuri and Hindi
               Manipuri and English

    1. Break the paragraph into sentences
    2. Remove ***, html links, bullet points, etc."""

import re
import os
from langdetect import detect
import nltk

new_text = []

# detect the language of the article


def detect_lang(line):
    l = detect(line)
    return l

def data_clean(line):

    line = re.sub('^[1-9]-', '', line)  # removing bullet points viz 1. 2. 3. upto 2 digits
    line = re.sub('.*News', '', line)
    line = re.sub('((www.[^s]+)|(https?://[^s]+))', '', line)
    line = re.sub('@[^s]+', '', line)
    line = re.sub(r'#([^s]+)', r'', line)
    line = re.sub(r'[''")(]', r'', line)
    line = re.sub(r'\**\*$', r'', line)
    line = re.sub(r'\u200d', r' ', line)
    line = re.sub(r'\xa0', r' ', line)
    line = re.sub(r'\t', r'', line)
    line = re.sub(r'^[*•]', r'', line)
    line = line.strip()
    return line


# set the path of the folder

path = input("Path of the folder:")                 # path = 'Z:\lavinia\law'

# read each text file of the articles from the folder
# iterate through all file

for file in os.listdir(path):

    article_path = f"{path}\{file}"
    article_text = open(article_path,'r', encoding = 'utf-8')

    file_name = os.path.splitext(article_path)
    print(file_name[0])

    # read the first line of the text to determine the language of the article

    first_line = article_text.readline()
    lang = detect_lang(first_line)

    read_article = article_text.read()

    # Text is the paragraph input
    # perform sentence segmentation according to the language
    if lang == 'en':
        sent_text = nltk.sent_tokenize(read_article)
    elif lang == 'hi':
        sent_text = re.split("।|\n", read_article)
    elif lang == 'bn':
        sent_text = re.split("।|\n", read_article)
    else:
        print("Language detected is not English, Hindi or Manipuri")

    fname = file_name[0]+"-clean.txt"

    clean_article_text = open(fname, 'w+', encoding='utf-8')

    for sent in sent_text:
        result = data_clean(sent)
        new_text.append(result)

    while "" in new_text:
        new_text.remove("")

    for s in new_text:
        clean_article_text.write(s + "\n")

    clean_article_text.close()

    new_text.clear()

    sent_text.close()

    article_text.close()

    # clubbing the parallel sentences in a text file

    from itertools import izip

    with open("textfile1") as textfile1, open("textfile2") as textfile2:
        for x, y in izip(textfile1, textfile2):
            x = x.strip()
            y = y.strip()
            print("{0}\t{1}".format(x, y))