import random
import time
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from colorama import init
from termcolor import colored


class SetWebDriver:

    def __init__(self, service, options):
        self.driver = webdriver.Chrome(service=service, options=options)

    def launch_browser(self, url):
        driver = self.driver
        driver.get(url)
        print(colored("Start", "red"))

    def close_browser(self):
        self.driver.close()
        self.driver.quit()


class Bot(SetWebDriver):

    def fill_search_form(self):
        driver = self.driver
        time.sleep(random.randrange(5, 7))
        driver.find_element(By.CLASS_NAME, "cmp-intro_acceptAll").click()
        select_element = driver.find_element(By.ID, 'make')
        select_object = Select(select_element)
        select_object.select_by_value('9')
        time.sleep(random.randrange(3, 5))
        select_element = driver.find_element(By.ID, 'model')
        select_object = Select(select_element)
        select_object.select_by_value('53')
        time.sleep(random.randrange(5, 7))
        driver.find_element(By.CLASS_NAME, "mb-sm-0").click()
        print("Searching...")
        time.sleep(random.randrange(5, 7))

    def write_csv(self):
        with open(f'data.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(
                [
                    "Model",
                    "Year",
                    "Mileage",
                    "Horsepower",
                    "Fuel",
                    "Transmission",
                    "Price",
                    "Old Price",
                    "Links"
                ]
            )
        print(colored("CSV file created", "yellow"))

    def cars_for_sale(self):
        global model, year, mileage, horsepower, fuel, transmission, price, old_price, links
        print("...in action")
        driver = self.driver
        html = driver.page_source
        soup = BeautifulSoup(html, "lxml")
        vehicle_cards = soup.find_all("article", class_="vehicle-card")
        for card in vehicle_cards:
            model = card.find("div", class_="mr-auto").get_text()
            try:
                tech = card.find("div", class_="mt-xl-4")
                list = []
                for item in tech:
                    i = item.get_text(strip=True)
                    list.append(i)
                year, mileage, horsepower, fuel, transmission = [list[i] for i in (0, 1, 2, 3, 4)]
            except:
                pass
            prices = card.find("div", class_="vehicle-prices")
            price = prices.find("span", class_="d-inline-block").get_text()
            old_price = prices.find("span", class_="old-price").get_text()
            links = "https://www.autoscout24.ch" + card.find("a", class_="stretched-link").get("href")

            with open(f'data.csv', 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow(
                    [
                        model,
                        year,
                        mileage,
                        horsepower,
                        fuel,
                        transmission,
                        price,
                        old_price,
                        links
                    ]
                )
        time.sleep(random.randrange(7, 10))

    def check_pagination_exists(self, num):
        driver = self.driver
        try:
            driver.find_element(By.CSS_SELECTOR, f"div > main > section > div > div > div > div > div:nth-child(5) > div.col.col-sm-8.col-md > nav > ul > li:nth-child({num}) > button")
        except NoSuchElementException:
            print("Pagination button not exists")
            return False
        return True

    def next_page(self, num):
        driver = self.driver
        driver.find_element(By.CSS_SELECTOR, f"div > main > section > div > div > div > div > div:nth-child(5) > div.col.col-sm-8.col-md > nav > ul > li:nth-child({num}) > button").click()
        time.sleep(random.randrange(7, 10))

    """
    _______________________________________________________________________
    _______________________Main Method Here________________________________
    _______________________________________________________________________
    """


def main():
    init()  # colorama init
    service = Service(executable_path="/Users/antonr/Documents/Python/autoscout24/chromedriver")
    lang = "en-US"
    window_size = "1200,800"
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36"

    options = Options()
    options.headless = True  # Headless Mode. Driving Headless Browser
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument(f"--lang={lang}")
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument(f"--window-size={window_size}")

    """
    _______________________________________________________________________
    ____________________Creating an instance of a class____________________
    _______________________________________________________________________
    """

    bot = Bot(service, options)
    bot.launch_browser("https://www.autoscout24.ch/de/")
    bot.fill_search_form()
    bot.write_csv()

    iterator = 2
    page_button_num = 2
    running = True
    while running:
        bot.cars_for_sale()
        print(bot.check_pagination_exists(page_button_num))
        try:
            if not bot.check_pagination_exists(page_button_num):
                running = False
            else:
                bot.next_page(page_button_num)
                print(colored(f"Next page: {iterator}", "yellow"))
        except:
            pass

        if page_button_num < 5:
            page_button_num += 1
        else:
            page_button_num = 5

        iterator += 1

    print("Out of the Loop")
    time.sleep(random.randrange(7, 10))
    print(colored("Finish", "red"))
    time.sleep(random.randrange(7, 10))
    bot.close_browser()


if __name__ == "__main__":
    main()
