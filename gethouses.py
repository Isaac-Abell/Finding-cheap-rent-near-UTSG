from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import math

def get_houses(max: int, total = None):

    browser = webdriver.Chrome()

    browser.get("https://rentals.ca/toronto")

    link = []
    prices = []
    locations = []
    if total is None:
        total = browser.find_element(By.XPATH, "/html[1]/body[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/p[1]/strong[1]").text
        total = int(total[0:total.index(" ")])
        total = math.ceil(total / 10)

    for i in range(1, total):
        for j in browser.find_elements(By.CLASS_NAME, "listing-card__details-link"):
            link.append(j.get_attribute("href"))

        for j in browser.find_elements(By.CLASS_NAME, "listing-card__price"):
            price = j.text

            price = price[price.index("$")+1:].strip()
            if "-" in price:
                price = price[0:price.index("-") - 1]

            prices.append(int(price))

        for j in browser.find_elements(By.CLASS_NAME, "listing-card__title"):
            locations.append(j.text)

        for k in prices:
            if k > max:
                p = prices.index(k)
                prices.pop(p)
                locations.pop(p)
                link.pop(p)
        
        if i == 2:
            browser.get("https://rentals.ca/toronto" + "?p=" + str(i+1))
            time.sleep(30)

        else:
            browser.get("https://rentals.ca/toronto" + "?p=" + str(i+1))

    info = []

    for i in range(0, len(prices)):
        info.append([locations[i], prices[i], link[i]])

    info.sort(key = lambda x: x[1])

    return info
