from logging import disable
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import json

url = "https://www.fda.gov/news-events/fda-meetings-conferences-and-workshops/fda-meetings-conferences-and-workshops-past-events"

def crawler(url):
    driver = webdriver.Chrome()
    driver.get(url)
    driver.implicitly_wait(7)

    all_td_entries = []
    all_link_entries = []

    total_entries = driver.find_element_by_id('DataTables_Table_0_info').text
    total_entries = total_entries[18:-7]
    total_entries = int(total_entries)

    start_dates = []
    end_dates = []
    events = []
    events_type = []
    centers = []

    headings = []

    list_of_dict = []


    table_headings = driver.find_elements_by_xpath('//table[@id="DataTables_Table_0"]/thead//th')

    for heading in table_headings:
        headings.append(heading.text)

    i = 0
    l = 0
    m = 0

    while (len(start_dates) < total_entries):

        driver.execute_script("window.scrollBy(0,925)", "")

        non_link_entries = driver.find_elements_by_xpath('//table[@id="DataTables_Table_0"]/tbody/tr/td')
        linked_entries = driver.find_elements_by_xpath('//table[@id="DataTables_Table_0"]/tbody/tr/td/a')

        for entry in non_link_entries:
            all_td_entries.append(entry)

        for entry in linked_entries:
            all_link_entries.append(entry)
        
        while l < len(all_link_entries):
            events.append(all_link_entries[l].get_attribute('href'))
            events_type.append(all_link_entries[l + 1].get_attribute('href'))
            centers.append(all_link_entries[l + 2].get_attribute('href'))

            l = l + 3      
        
        while i < len(all_td_entries):
            start_dates.append(all_td_entries[i].text)
            end_dates.append(all_td_entries[i + 1].text)

            i = i + 5
        
        dictionary = {}

        while m < len(start_dates):
            dictionary[headings[0]] = start_dates[m]
            dictionary[headings[1]] = end_dates[m]
            dictionary[headings[2]] = events[m]
            dictionary[headings[3]] = events_type[m]
            dictionary[headings[4]] = centers[m]

            list_of_dict.append(dictionary)

            dictionary = {}

            m = m + 1

                   
        driver.find_element_by_link_text('Next').click()
        
        output_file = open('outputfile', 'w', encoding='utf-8')

        for dic in list_of_dict:
            json.dump(dic, output_file) 
            output_file.write("\n")


instance = crawler(url)