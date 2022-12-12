from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import datetime as dt

chrome_options = Options()
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument("--headless")
chromedriver_autoinstaller.install()

driver = webdriver.Chrome(options=chrome_options)


class Trading:

    def __init__(self, ticker):
        self.ticker = ticker

    def summary(self):
        try:
            driver.get(self.ticker)
            time.sleep(2)

            driver.find_element(by=By.XPATH, value='//button[@id="5m"]').click()
            time.sleep(1)

            now = dt.datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

            summary = driver.find_element(by=By.XPATH, value='//span[contains(.,"Summary")]/following::span[10]').text
            price = driver.find_element(by=By.XPATH,
                                        value='//div[@class="tv-symbol-price-quote__value js-symbol-last"]').text
            print('Summary Status:', summary, "At", dt_string)
            print('Price:', price, "At", dt_string)

            if price is None:
                price = 0

            return summary, float(price)
        except Exception as e:
            print(f"Trading view fail: {e}")
