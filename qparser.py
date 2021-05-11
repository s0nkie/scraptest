from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import csv, json
import os


url = 'https://finance.yahoo.com/'

csvFilePath = './PINS.csv'
jsonFilePath = './PINS.json'

options = webdriver.ChromeOptions()
options.add_argument("--headless")

driver = webdriver.Chrome(options=options)

def save(csvFilePath, jsonFilePath):
    if csvFilePath in csvFilePath:
        data = {}
        with open(csvFilePath) as csvFile:
            csvReader = csv.DictReader(csvFile)
            for rows in csvReader:
                Date = rows['Date']
                data[Date] = rows
        with open(jsonFilePath, 'w') as jsonFile:
            jsonFile.write(json.dumps(data, indent=4))
    return data


def main():
    driver.get(url)
    serch = driver.find_element(By.ID, 'yfin-usr-qry').send_keys("PINS" + Keys.ENTER)
    driver.implicitly_wait(5)
    historical_data = driver.find_element(By.LINK_TEXT, 'Historical Data').click()
    driver.implicitly_wait(5)
    date = driver.find_element(By.XPATH, '//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/div[1]/div/div/div/span').click()
    date_max = driver.find_element( By.XPATH, '//*[@id="dropdown-menu"]/div/ul[2]/li[4]/button').click()
    apply_btn = driver.find_element(By.XPATH,'//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/button/span').click()
    download = driver.find_element(By.XPATH, '//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[2]/span[2]/a/span')
    download.click()

    while True:
        if os.path.exists(csvFilePath):
            save(csvFilePath, jsonFilePath)
            driver.close()
            break
        else:
            continue

if __name__ == "__main__":
    main()