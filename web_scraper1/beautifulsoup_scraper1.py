from requests import get
from bs4 import BeautifulSoup
import pandas as pd
from IPython.core.display import clear_output

# This block introduces a wait to crawl through multiple search result pages to reduce risk of having IP blocked!
from random import randint
from time import sleep
from time import time

results = []
names = []
qualifications = []
specialist_areas = []

start_time = time()
request_count = 1

for i in range(1,6):

    if i == 1:
    
        url = 'https://findavet.rcvs.org.uk/find-a-vet-surgeon/?filter-choice=&filter-keyword=&filter-searchtype=surgeon&specialist5=true&%p='

        response = get(url)

        sleep(randint(1, 3))

        elapsed_time = time() - start_time
        print('Request: {}; Frequency: {} Requests/s;'.format(request_count, request_count / elapsed_time))
        clear_output(wait=True)    
        
        html_soup = BeautifulSoup(response.text, "lxml")

        result_containers = html_soup.find_all('div', class_='item item--fav item--surgeon')
        specialism = html_soup.find_all('div', class_='item-additional')

        for container in result_containers:
            name = container.div.h3.a.text
            names.append(name)

            qualification = container.div.span.text
            qualifications.append(qualification)

        for container in specialism:
            speciality = container.li.text
            specialist_areas.append(speciality)    
        
        from pandas import ExcelWriter
        test_df = pd.DataFrame({'Name': names,
        'Qualifications': qualifications,
        'Specialist in:': specialist_areas})
        print(test_df.info())

    else:

        url = 'https://findavet.rcvs.org.uk/find-a-vet-surgeon/?filter-choice=&filter-keyword=&filter-searchtype=surgeon&specialist5=true&%p=' + str(i)

        response = get(url)

        sleep(randint(1, 3))

        elapsed_time = time() - start_time
        print('Request: {}; Frequency: {} Requests/s;'.format(request_count, request_count / elapsed_time))
        clear_output(wait=True)    
        
        html_soup = BeautifulSoup(response.text, 'lxml')

        result_containers = html_soup.find_all('div', class_='item item--fav item--surgeon')
        specialism = html_soup.find_all('div', class_='item-additional')

        for container in result_containers:
            name = container.div.h3.a.text
            names.append(name)

            qualification = container.div.span.text
            qualifications.append(qualification)

        for container in specialism:
            speciality = container.li.text
            specialist_areas.append(speciality)    
        
        from pandas import ExcelWriter
        test_df = pd.DataFrame({'Name': names,
        'Qualifications': qualifications,
        'Specialist in:': specialist_areas})
        print(test_df.info())
    
writer = pd.ExcelWriter('beautiful_soup_output.xlsx')
test_df.to_excel(writer, 'Cardiologists')
writer.save()