from requests import get
from bs4 import BeautifulSoup
import pandas as pd
from IPython.core.display import clear_output
from random import randint
from time import sleep
from time import time

def scrape():
    
    results = []
    names = []
    qualifications = []
    specialist_areas = []

    start_time = time()
    request_count = 1

    pages = [str(i) for i in range(1,5)]

    for i in pages():

            url = ('https://findavet.rcvs.org.uk/find-a-vet-surgeon/?filter-'
            'choice=&filter-keyword=&filter-searchtype=surgeon&specialist5='
            'true&p=') + i

            response = get(url)

            sleep(randint(1,3))

            html_soup = BeautifulSoup(response.text, 'lxml')

            result_containers = html_soup.find_all('div', class_='item item--'
            'fav item--surgeon')
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