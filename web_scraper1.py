import time

from selenium import webdriver

from selenium.webdriver.common.keys import Keys

search_string = input("Search for a specialist in which field?").lower()

if search_string == "cardiology":
    url = "https://findavet.rcvs.org.uk/find-a-vet-surgeon/?filter-keyword=&filter-searchtype=surgeon&specialist5=true"

elif search_string == "diagnostic imaging":
        url = """
        https://findavet.rcvs.org.uk/find-a-vet-surgeon/?filter-keyword=&filter-searchtype=surgeon&specialist13=true"""

#Allows Selenium to take control of Firefox
driver = webdriver.Firefox(executable_path=r"geckodriver.exe")

driver.get(url)

# print(url)

try:
    name = driver.find_element_by_xpath("//div[@id='results']//h3[@class='item-title']")
    print(name.text)

except Exception:
    print("An error has occurred.")

#Closes Firefox
driver.quit()