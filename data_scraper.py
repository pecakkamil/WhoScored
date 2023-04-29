import json
import time
from selenium.webdriver.common.by import By
import datetime
import winsound

# settings of beep signal after an error
frequency = 2500  # Set Frequency To 2500 Hertz
duration = 500  # Set Duration To 1000 ms == 1 second


class Scraper:
    def __init__(self, league_country_param, driver, waiting_time):

        self.league_country_param = league_country_param
        self.driver = driver
        self.waiting_time = waiting_time
        self.communicate = ""
        self.failed_list = []

    def scraping(self, match_id):
        # data dictionary used to save data from each point
        scrape_dict = {"match_id": match_id}
        t1 = datetime.datetime.now()
        try:
            # opening the website
            self.driver.get(f"https://www.whoscored.com/Matches/{match_id}")
            time.sleep(self.waiting_time)
            # getting country value
            country = self.driver.find_element(By.XPATH, '//*[@id="breadcrumb-nav"]/span[1]')
            scrape_dict["country"] = country.text

            # getting league value
            league = self.driver.find_element(By.XPATH, '//*[@id="breadcrumb-nav"]/a')
            scrape_dict["league"] = league.text

            # clicking link 'Match Centre'
            match_centre = self.driver.find_element(By.LINK_TEXT, 'Match Centre')
            match_centre.click()
            # time for page loading
            time.sleep(2 * self.waiting_time)

            # getting referee value
            referee = self.driver.find_element(By.XPATH, '//*[@id="stadium"]/div[1]/div[2]/div[1]/span[3]/a/span[2]')
            scrape_dict["referee"] = referee.text

            # getting date value
            date = self.driver.find_element(By.XPATH, '//*[@id="match-header"]/table/tbody/tr[2]/td[2]/div[3]/dl/dd[2]')
            scrape_dict["date"] = date.text

            # getting host value
            host = self.driver.find_element(By.XPATH, '//*[@id="match-header"]/table/tbody/tr[1]/td[1]/a')
            scrape_dict["host"] = host.text

            # getting uest value
            guest = self.driver.find_element(By.XPATH, '//*[@id="match-header"]/table/tbody/tr[1]/td[3]/a')
            scrape_dict["guest"] = guest.text

            # getting result value
            result = self.driver.find_element(By.XPATH, '//*[@id="match-header"]/table/tbody/tr[1]/td[2]')
            scrape_dict["result"] = result.text

            # getting host corners value
            host_corners = self.driver.find_element(By.XPATH,
                                                    '//*[@id="match-centre-stats"]/div[1]/ul[1]/li[8]/div[1]/span[1]')
            scrape_dict["host_corners"] = host_corners.text

            # getting guest corners value
            guest_corners = self.driver.find_element(By.XPATH,
                                                     '//*[@id="match-centre-stats"]/div[1]/ul[1]/li[8]/div[1]/span[3]')
            scrape_dict["guest_corners"] = guest_corners.text

            # getting host shots value
            host_shots = self.driver.find_element(By.XPATH,
                                                  '//*[@id="match-centre-stats"]/div[1]/ul[1]/li[2]/div[1]/span[1]')
            scrape_dict["host_shots"] = host_shots.text

            # getting guests shots value
            guest_shots = self.driver.find_element(By.XPATH,
                                                   '//*[@id="match-centre-stats"]/div[1]/ul[1]/li[2]/div[1]/span[3]')
            scrape_dict["guest_shots"] = guest_shots.text

            # clicking button 'More' opening additional data in the website
            more_button1 = self.driver.find_element(By.XPATH,
                                                    '//*[@id="match-centre-stats"]/div[1]/ul[1]/li[2]/div[2]/label')
            more_button1.click()

            # getting host shots on target value
            host_shots_on_target = self.driver.find_element(By.XPATH,
                                                            '//*[@id="match-centre-stats"]/div[1]/ul[2]/li[2]/div[1]/ul/li[3]/div/span[1]')
            scrape_dict["host_shots_on_target"] = host_shots_on_target.text

            # getting guest shots on target value
            guest_shots_on_target = self.driver.find_element(By.XPATH,
                                                             '//*[@id="match-centre-stats"]/div[1]/ul[2]/li[2]/div[1]/ul/li[3]/div/span[3]')
            scrape_dict["guest_shots_on_target"] = guest_shots_on_target.text

            # getting host shots off target value
            host_shots_off_target = self.driver.find_element(By.XPATH,
                                                             '//*[@id="match-centre-stats"]/div[1]/ul[2]/li[2]/div[1]/ul/li[4]/div/span[1]')
            scrape_dict["host_shots_off_target"] = host_shots_off_target.text

            # getting host shots on target value
            guest_shots_off_target = self.driver.find_element(By.XPATH,
                                                              '//*[@id="match-centre-stats"]/div[1]/ul[2]/li[2]/div[1]/ul/li[4]/div/span[3]')
            scrape_dict["guest_shots_off_target"] = guest_shots_off_target.text

            # getting host woodwork value
            host_shots_woodwork = self.driver.find_element(By.XPATH,
                                                           '//*[@id="match-centre-stats"]/div[1]/ul[2]/li[2]/div[1]/ul/li[2]/div/span[1]')
            scrape_dict["host_shots_woodwork"] = host_shots_woodwork.text

            # getting guest woodwork value
            guest_shots_woodwork = self.driver.find_element(By.XPATH,
                                                            '//*[@id="match-centre-stats"]/div[1]/ul[2]/li[2]/div[1]/ul/li[2]/div/span[3]')
            scrape_dict["guest_shots_woodwork"] = guest_shots_woodwork.text

            # getting host blocked value
            host_shots_blocked = self.driver.find_element(By.XPATH,
                                                          '//*[@id="match-centre-stats"]/div[1]/ul[2]/li[2]/div[1]/ul/li[5]/div/span[1]')
            scrape_dict["host_shots_blocked"] = host_shots_blocked.text

            # getting guest blocked value
            guest_shots_blocked = self.driver.find_element(By.XPATH,
                                                           '//*[@id="match-centre-stats"]/div[1]/ul[2]/li[2]/div[1]/ul/li[5]/div/span[3]')
            scrape_dict["guest_shots_blocked"] = guest_shots_blocked.text

            # clicking link to the match aport site
            match_report = self.driver.find_element(By.LINK_TEXT, 'Match Report')
            match_report.click()

            # time for page loading
            time.sleep(self.waiting_time)

            # clicking card button
            card_button1 = self.driver.find_element(By.XPATH, '//*[@id="live-chart-stats-options"]/li[3]/a')
            card_button1.click()

            time.sleep(self.waiting_time)

            # getting host fouls value
            host_fouls = self.driver.find_element(By.XPATH, '//*[@id="live-aggression-info"]/div/div[5]/span[2]/span')
            scrape_dict["host_fouls"] = host_fouls.text

            # getting guest fouls value
            guest_fouls = self.driver.find_element(By.XPATH, '//*[@id="live-aggression-info"]/div/div[5]/span[4]/span')
            scrape_dict["guest_fouls"] = guest_fouls.text

            # getting host yellow cards value
            host_yellow_cards = self.driver.find_element(By.XPATH,
                                                         '//*[@id="live-aggression-info"]/div/div[3]/span[2]/span')
            scrape_dict["host_yellow_cards"] = host_yellow_cards.text

            # getting guest yellow cards value
            guest_yellow_cards = self.driver.find_element(By.XPATH,
                                                          '//*[@id="live-aggression-info"]/div/div[3]/span[4]/span')
            scrape_dict["guest_yellow_cards"] = guest_yellow_cards.text

            # getting host red cards value
            host_red_cards = self.driver.find_element(By.XPATH,
                                                      '//*[@id="live-aggression-info"]/div/div[2]/span[2]/span')
            scrape_dict["host_red_cards"] = host_red_cards.text

            # getting guest red cards value
            guest_red_cards = self.driver.find_element(By.XPATH,
                                                       '//*[@id="live-aggression-info"]/div/div[2]/span[4]/span')
            scrape_dict["guest_red_cards"] = guest_red_cards.text

            # showing all scraped data
            print(scrape_dict)

            # saving dictionary as a file
            with open(f'data/{self.league_country_param}/{match_id}.json', "w") as file:
                json.dump(scrape_dict, file)
        except:
            self.communicate = str(match_id) + ": Scraping error! \n"
            self.failed_list.append(match_id)
            winsound.Beep(frequency, duration)
        else:
            t2 = datetime.datetime.now()
            time_difference = t2 - t1
            print(time_difference)
            self.communicate = str(match_id) + ": Scraping time: " + str(time_difference.total_seconds()) + "\n"
