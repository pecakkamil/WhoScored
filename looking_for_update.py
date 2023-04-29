from selenium.webdriver.common.by import By
import time
from datetime import datetime
import json

new_match_list = []
# dictionary of main pages of each league

with open("data/leagues.txt") as file:
    league_sites = json.loads(file.read())



class Update:
    def __init__(self, league_country, driver, waiting_time, starting_time):
        self.league_country = league_country
        self.driver = driver
        self.waiting_time = waiting_time
        self.starting_time = starting_time
        self.id_numbers = []
        self.links = []

    def get_update(self):
        # opening the league website
        self.driver.get(league_sites[self.league_country])
        time.sleep(self.waiting_time)
        # clicking the agree button before opening site
        agree_button = self.driver.find_element(By.XPATH, '//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]')
        agree_button.click()
        # getting date value
        date = self.driver.find_element(By.XPATH, '//*[@id="date-config-toggle-button"]/span[1]')
        decoded_dates = date_decoder(date.text)

        user_start_date = datetime(self.starting_time[0], self.starting_time[1], self.starting_time[2])

        print(decoded_dates[0])
        print(user_start_date)

        # clicking previous week until we get date before user start
        while decoded_dates[0] > user_start_date:
            print("cofnij strone")
            back = self.driver.find_element(By.XPATH, '//*[@id="date-controller"]/a[1]/span')
            back.click()
            date = self.driver.find_element(By.XPATH, '//*[@id="date-config-toggle-button"]/span[1]')
            decoded_dates = date_decoder(date.text)
            time.sleep(2 * self.waiting_time)
            # selection of all matches links
            matches = self.driver.find_elements(By.CSS_SELECTOR, 'a.result-1.rc')
            for match in matches:
                self.links.append(match.get_attribute("href"))

        # creating matches id of links
        for link in self.links:
            print(link)
            short_link = link.replace('https://www.whoscored.com/Matches/', "")
            print(short_link)
            self.id_numbers.append(short_link[0:7])


# function changing date scraped from whoscored to start and end date of each week
def date_decoder(date):
    elements = date.split(" ")
    print(elements)
    date_list = [0, 0, 0, 0, 0, 0]
    # start day, start month,year, end day, end month, year

    if elements[1] == "-":
        date_list[0] = elements[0]
        date_list[1] = elements[3]
        date_list[2] = elements[4]
        date_list[3] = elements[2]
        date_list[4] = elements[3]
        date_list[5] = elements[4]

    else:
        date_list[0] = elements[0]
        date_list[1] = elements[1]
        date_list[2] = elements[5]
        date_list[3] = elements[3]
        date_list[4] = elements[4]
        date_list[5] = elements[5]
        if date_list[1] == "Dec" and date_list[4] == "Jan":
            date_list[2] = int(date_list[5]) - 1

    months = {"Jan": 1,
              "Feb": 2,
              "Mar": 3,
              "Apr": 4,
              "May": 5,
              "Jun": 6,
              "Jul": 7,
              "Aug": 8,
              "Sep": 9,
              "Oct": 10,
              "Nov": 11,
              "Dec": 12}
    print(date_list)
    # changing year if week is between two years
    for month, number in months.items():
        if date_list[1] == month:
            date_list[1] = str(number)
        if date_list[4] == month:
            date_list[4] = str(number)
    print(date_list)
    # changing all str values to int values
    for i in range(len(date_list)):
        date_list[i] = int(date_list[i])
    # creating datetime instances
    start_date = datetime(int(date_list[2]), date_list[1], int(date_list[0]))
    end_date = datetime(int(date_list[5]), date_list[4], int(date_list[3]))

    return [start_date, end_date]
