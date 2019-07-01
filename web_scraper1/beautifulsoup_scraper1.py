from requests import get
from bs4 import BeautifulSoup
import pandas as pd
from IPython.core.display import clear_output
from pandas import ExcelWriter

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

# moved the logic to get the data into a function. Since the only variable here is URL, we'll pass that in.
# Function returns a dataframe with the salient data
def getVets(url):

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


    pageOfData = pd.DataFrame({'Name': names,
    'Qualifications': qualifications,
    'Specialist in:': specialist_areas})
    print(pageOfData.info())

    return pageOfData

# URL without page
firstUrl = 'https://findavet.rcvs.org.uk/find-a-vet-surgeon/?filter-keyword=&filter-searchtype=surgeon&advanced16=true#primary-navigation'

# set the allPages dataframe == the response from the first call to the GetVets function, which will return page 1
allPages = getVets(firstUrl)

# Loop the remaining pages, adding to the allPages dataframe
#for i in range(2,6):
    #pagedUrl = 'https://findavet.rcvs.org.uk/find-a-vet-surgeon/?filter-choice=&filter-keyword=&filter-searchtype=surgeon&specialist5=true&p=' + str(i)
    #allPages = getVets(pagedUrl)

# Print to Excel - used a 'with' statement so that the onject is disposed of cleanly after it's scope is complete.... good memory hygene!  Nobody likes a dirty heap!
with pd.ExcelWriter('uk_sa_cardiology_avps.xlsx') as writer:
    allPages.to_excel(writer, 'Cardiologists')
    writer.save()