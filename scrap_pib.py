""" Created on 4 August 2023
    Author: Lavinia Nongbri

    this code is to extract the links of the PIB articles
    Language - Hindi and Manipuri
               Manipuri and English"""


# importing packages

from selenium.webdriver.common.by import By
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.select import Select
import sys
import os

source_lang = 'mni'

# Take the preferred language of the article as an input from the user. Option is either hindi or manipuri
lang = input("Enter your preferred target language (Eng/Hin):")

str1 = "english"
str2 = "hindi"

if (lang.lower() != str1) and (lang.lower() != str2):
    print("Not valid")
    sys.exit(0)

region_value = '30'
lang_value = '14'
partial_link_text = 'খরগা হেন্না +'


# else:
#     if (lang.lower() == str1):
#         region_value = '30'
#         lang_value = '14'
#         partial_link_text = 'খরগা হেন্না +'
#         print(lang)
#
#     elif (lang.lower() == str2):
#         region_value = '3'
#         lang_value = '2'
#         partial_link_text = 'और देखें +'
#         print(lang)

# ministries of same domain clubbed together in a list
# list contains the ministry_id according to pib

#admin = '1', '2', '3', '4', '10', '12', '35', '68']
admin = {'President Secretariat': '1', 'Vice President Secretariat': '2', 'Prime Minister Office': '3',
         'Cabinet Secretariat': '68', 'Election Commission': '35', 'Ministry of Panchayati Raj': '10',
         'Ministry of Parliamentary Affairs': '12', 'Ministry of External Affairs': '4' }

#law = ['7', '33', '5']
law = {'Ministry of Defence': '33', 'Ministry of Law and Justice': '7', 'Ministry of Home Affairs': '5'}

#edu = ['8', '77']
edu = {'Ministry of Education': '8', 'Ministry of Skill Development and Enterprenuership': '77'}

#tech = ['13', '1323']
tech = {'Ministry of Electronics & IT': '1323', 'Ministry of Science & Technology': '13'}

#health = ['31', '80']
health = {'AYUSH': '80', 'Ministry of Health & Family Welfare' : '31'}

#agri = ['27']
agri = {'Ministry of Agriculture & Farmers Welfare': '27'}

#climate = ['30', '38']
climate = {'Ministry of Environment, Forest and Climate Change': '30',
           'Ministry of Water Resources, River Development, Ganga Rejuvenation': '38'}

#tourism = ['36']
tourism = {'Ministry of Tourism': '36'}


domain_list = {'administration': '1', 'law': '2','education': '3','technical': '4',
               'healthcare': '5','agriculture': '6','climate': '7','tourism': '8'}

print("Domain inputs to be given\n"
      "Administration\n"
      "Law \n"
      "Education\n"
      "Technical\n"
      "Healthcare\n"
      "Agriculture\n"
      "Climate\n"
      "Tourism\n")

# take domain choice as input from user

domain = input("Articles of which domain would like to collect?").lower()

if domain not in domain_list:
    print("Invalid domain")
    sys.exit(0)

domain_value = domain_list.get(domain)

ministry_list = {}

if domain_value == '1':
    ministry_list = admin
elif domain_value == '2':
    ministry_list = law
elif domain_value == '3':
    ministry_list = edu
elif domain_value == '4':
    ministry_list = tech
elif domain_value == '5':
    ministry_list = health
elif domain_value == '6':
    ministry_list = agri
elif domain_value == '7':
    ministry_list = climate
elif domain_value == '8':
    ministry_list = tourism
else:
    print('Not match')

print(ministry_list)
print("You can choose date, month and year of the articles you want\n"
      "For date, you can give any number between 0-31. 0 means all the days of the particular month ")
date = input('Enter the date:')

date_int = int(date)

if date_int < 0 or date_int >31:
    print("Invalid Date")
    sys.exit(0)

month_list = {'january': '1', 'february': '2','march': '3','april': '4','may': '5','june': '6','july': '7','august': '8','september': '9','october': '10','november': '11','december': '12'}

month = input("enter month:").lower()

if month not in month_list:
    print("Invalid month")
    sys.exit(0)

month_value = month_list.get(month)

year = input("Enter year (2017-2023):")


if 2023 < int(year) < 2017:
    print("Invalid year")
    sys.exit(0)

# execute the chrome driver

driver = webdriver.Chrome(executable_path=r"C:\Users\IIIT\.wdm\drivers\chromedriver-win64-119\chromedriver.exe")

# load the website
driver.get('https://pib.gov.in/indexd.aspx')

# identify dropdown ------> PIB Imphal
select_region = driver.find_element(By.NAME, 'ctl00$Bar1$ddlregion')

select = Select(select_region)
select.select_by_value(region_value)

# wait for the page to load
driver.implicitly_wait(15)

# select the language

select_lang = driver.find_element(By.NAME, 'ctl00$Bar1$ddlLang')
select = Select(select_lang)
select.select_by_value(lang_value)

driver.implicitly_wait(15)

# click on more release in the web page
all_release = driver.find_element(By.CLASS_NAME, 'more-release')
more_release = driver.find_element_by_partial_link_text(partial_link_text)
more_release.click()

driver.implicitly_wait(30)

path = r"Z:\lavinia"
folder_path = os.path.join(path, domain)

file_name = domain+'-'+date+'-'+month+'-'+year+'-'+source_lang+'-links.txt'

file_path = os.path.join(folder_path, file_name)

text = open(file_path, 'w', encoding="utf-8")

for ministry in ministry_list.values():

    # Select all from date dropdown menu
    select_date = driver.find_element(By.NAME, 'ctl00$ContentPlaceHolder1$ddlMinistry')
    select = Select(select_date)
    select.select_by_value(ministry)

    # Select all from date dropdown menu
    select_date = driver.find_element(By.NAME, 'ctl00$ContentPlaceHolder1$ddlday')
    select = Select(select_date)
    select.select_by_value(date)

    driver.implicitly_wait(20)

    # Select month dropdown menu
    select_month = driver.find_element(By.NAME, 'ctl00$ContentPlaceHolder1$ddlMonth')
    select = Select(select_month)
    select.select_by_value(month_value)  # january index is 0

    driver.implicitly_wait(10)

    # Select year dropdown menu
    select_year = driver.find_element(By.NAME, 'ctl00$ContentPlaceHolder1$ddlYear')
    select = Select(select_year)
    select.select_by_value(year)  # january index is 0

    content_area = driver.find_element(By.CLASS_NAME, 'content-area')
    collect_a = content_area.find_elements(By.TAG_NAME, 'a')

    for a in collect_a:
        href = a.get_attribute('href')
        print(href)
        text.write(href + '\n')
        if href is not None:
            print(href)

text.close()

driver.close()

import subprocess

# Run the other script
subprocess.run(["python", "scrap_pib_contents.py", domain, date, month, year, lang, file_path])

print("end of program")