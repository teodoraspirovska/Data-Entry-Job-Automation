import time
from bs4 import BeautifulSoup
import requests
import re
from selenium import webdriver
import os

CHROME_DRIVER_PATH = os.environ.get("MY_CHROME_DRIVER_PATH")
ZILLOW_URL = "https://www.zillow.com/san-francisco-ca/rentals/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22north%22%3A37.85489581746635%2C%22east%22%3A-122.29840365771484%2C%22south%22%3A37.69560228625891%2C%22west%22%3A-122.56825534228516%7D%2C%22mapZoom%22%3A12%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A20330%2C%22regionType%22%3A6%7D%5D%7D"
GOOGLE_FORM = "https://docs.google.com/forms/d/e/1FAIpQLSeK5i2OGdC0g1AjHlZHysS0FTwhmNq8AnIr7XkMW1O7PLH0QA/viewform?usp=pp_url"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/58.0.3029.110 Safari/537.3"
}
response = requests.get(ZILLOW_URL, headers=headers)

website_html = response.text
soup = BeautifulSoup(website_html, "html.parser")

addresses = soup.find_all(name="address")
apartment_addresses = []
for address in addresses:
    full_address = address.getText()
    apartment_addresses.append(full_address)
print(apartment_addresses)

prices = soup.find_all(name="span", class_='PropertyCardWrapper__StyledPriceLine-srp__sc-16e8gqd-1 iMKTKr')
apartment_prices = []
for price in prices:
    text = price.getText()
    match = re.search(r"\$[\d,]+", text)
    if match:
        apartment_prices.append(match.group())
print(apartment_prices)

links = soup.find_all(name="a", class_="StyledPropertyCardDataArea-c11n-8-84-0__sc-yipmu-0")
apartment_links = []
for link in links:
    href = link.get("href")
    apartment_links.append(href)
print(apartment_links)

driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
driver.get(GOOGLE_FORM)
time.sleep(5)

for i in range(len(apartment_addresses)):
    address_input = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_input = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_input = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')

    address_input.send_keys(apartment_addresses[i])
    price_input.send_keys(apartment_prices[i])
    link_input.send_keys(apartment_links[i])

    submit_button = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    submit_button.click()

    time.sleep(2)
    submit_another_response_link = driver.find_element_by_link_text("Submit another response")
    submit_another_response_link.click()
    time.sleep(5)
