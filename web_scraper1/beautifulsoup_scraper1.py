from requests import get
from bs4 import BeautifulSoup
import pandas as pd
from IPython.core.display import clear_output

# This block introduces a wait to crawl through multiple search result pages to reduce risk of having IP blocked!
from random import randint
from time import sleep
from time import time

start_time = time()
requests = 0

for _ in range(4):
    requests += 1
    sleep(randint(1, 3))
    elapsed_time = time() - start_time
    print('Request: {}; Frequency: {} requests/s;'.format(requests, requests / elapsed_time))
    clear_output(wait=True)

url = 'https://findavet.rcvs.org.uk/find-a-vet-surgeon/?filter-keyword=&filter-searchtype=surgeon&specialist5=true'

response = get(url)

# print(response.text)

html_soup = BeautifulSoup(response.text, 'lxml')
type(html_soup)

result_containers = html_soup.find_all('div', class_='item item--fav item--surgeon')
specialism = html_soup.find_all('div', class_='item-additional')

print(type(specialism))
print(len(specialism))

print(type(result_containers))
print(len(result_containers))

results = []
names = []
qualifications = []
specialist_areas = []

pages = [str(i) for i in range(1, 5)]

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
test_df.to_excel(writer, 'Sheet1')
writer.save()