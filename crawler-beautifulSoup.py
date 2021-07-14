from enum import EnumMeta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import json

url = "https://www.fda.gov/news-events/fda-meetings-conferences-and-workshops/fda-meetings-conferences-and-workshops-past-events"

def crawler(url):
    driver = webdriver.Chrome()
    driver.get(url)
    driver.implicitly_wait(7)

    total_entries = driver.find_element_by_id('DataTables_Table_0_info').text
    total_entries = total_entries[18:-7]
    total_entries = int(total_entries)

    dates = []
    urls = []
    headings = []
    list_of_dict = []

    i = 0
    l = 0

    soup = BeautifulSoup(driver.page_source, 'lxml')
        
    table = soup.find('table', attrs={'id': 'DataTables_Table_0'})

    table_headers = table.find('thead')
    headers = table_headers.find_all('tr')

    for tr in headers:
        all_headers = tr.find_all('th')

        for header in all_headers:
            headings.append(header.text.strip())


    while len(dates) < (total_entries*2):

        driver.execute_script("window.scrollBy(0,1000)", "")

        
        soup = BeautifulSoup(driver.page_source, 'lxml')
        table = soup.find('table', attrs={'id': 'DataTables_Table_0'})

        
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')

        for row in rows:
            cols = row.find_all('td')

            for element in cols:
                if (element.a is not None):
                    urls.append(element.a['href'])
                else:
                    dates.append(element.text.strip())

       
        driver.find_element_by_link_text('Next').click()
    
    dictionary = {}

    while (l < len(urls)):
        dictionary[headings[0]] = dates[i]
        dictionary[headings[1]] = dates[i + 1]
        dictionary[headings[2]] = 'www.fda.gov' + urls[l]
        dictionary[headings[3]] = 'www.fda.gov' + urls[l + 1]
        dictionary[headings[4]] = 'www.fda.gov' + urls[l + 2]

        list_of_dict.append(dictionary)

        dictionary = {}


        i = i + 2
        l = l + 3   
    
    result_file = open('resultfile', 'w', encoding='utf-8')
    for dic in list_of_dict:
        json.dump(dic, result_file) 
        result_file.write("\n")


crawler(url)