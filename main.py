import looking_for_update
import json_csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import data_scraper
import time
from main_window import *


# creating driver which is scraping data from website. Driver is based on chromedriver.exe
def create_driver():

    options = Options()
    # pictures are not loaded during scraping
    options.page_load_strategy = 'eager'
    # service = Service(r"chromedriver.exe")
    driver = webdriver.Chrome(executable_path="chromedriver.exe", options=options)
    return driver


# matches that aren't already scraped
match_to_update_list = []


# function getting data from catalog data with all matches already scraped (saved)
def matches_already_scraped():
    # label in the mian window that shows number of matches that are not already scraped
    global window
    # creating JsonToCsv object to get list of all created files for the league chosen in league_menu_match_update
    match_list = json_csv.JsonToCsv(str(window.league_menu_match_update_var.get()))
    # removing files already updated from list of matches to update
    for match in match_list.data_list:
        if str(match['match_id']) in match_to_update_list:
            match_to_update_list.remove(str(match['match_id']))
    # number of new matches to update
    new_matches_to_update = len(match_to_update_list)
    # changing number of new_matches_label in main window
    window.new_matches_label.config(text=f"New matches: {new_matches_to_update}")


# functions that by scraping gts matches which arent already scraped
def get_matches_to_update():
    global match_to_update_list
    # removing text from caution frame in main window
    window.caution_text.delete(1.0, END)
    # getting league from league menu
    league = str(window.league_menu_match_update_var.get())

    try:
        # getting date from main window
        year = int(window.year_var.get())
        month = int(window.month_var.get())
        day = int(window.day_var.get())
        print(f"{month} {day} {year}")
        # creating scraping driver
        driver = create_driver()
        print("test")
        # creating Update object
        update = looking_for_update.Update(league, driver, window.sleeping_time, [year, month, day])
        # starting get_update method from update instance
        update.get_update()
        # changing match_to_update_list by filling it with paramater id_numbers from update instance
        match_to_update_list = update.id_numbers

        print(match_to_update_list)
        # closing scraping river
        driver.quit()
        # writing all matches from list in matches_frame in main window
        for match in match_to_update_list:
            window.matches_frame.insert(END, match + '\n')
    except:
        window.caution_text.insert(END, "Give correct date!!")

    # displaying how manny matches arent already scraped
    window.matches_to_update_label.config(text=f"New matches: {len(match_to_update_list)} ")
    # making check update button active
    window.check_update_button.config(state=ACTIVE)


def create_csv():
    # removing text from caution text
    window.caution_text.delete(1.0, END)
    # creating new csv file
    new_file = json_csv.JsonToCsv(str(window.menu2_var.get()))
    new_file.save_data_file()
    # adding text to caution text
    window.caution_text.insert(END, "File created: ")
    # adding csv file name to caution text
    window.caution_text.insert(END, str(new_file.file_name))


#
def scrape_update():
    # removing text from caution text
    window.caution_text.delete(1.0, END)
    # creating scraping driver
    driver = create_driver()
    # crating instance of Scraper object
    scrape_updater = data_scraper.Scraper(str(window.league_menu_match_update_var.get()), driver, window.sleeping_time)
    # opening the website
    driver.get(f"https://www.whoscored.com")
    # pause in scraping for website loading
    time.sleep(2)
    # clicking the agree button before opening site
    agree_button = driver.find_element(By.XPATH, '//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]')
    agree_button.click()
    # using method scraping of Scraper class for each match inthe list
    for match in match_to_update_list:
        scrape_updater.scraping(match)
        # printing information from scrape updater
        window.caution_text.insert(END, scrape_updater.communicate)
        window.update()
    # saving failed_list from scrape_updater as txt file in data catalogue
    with open(f'data/failed_file.txt', "a") as file1:
        file1.write("\n".join(str(item) for item in scrape_updater.failed_list))
    # printing failed list in main window
    window.caution_text.insert(END, scrape_updater.failed_list)
    # closing scraping driver
    driver.close()


# function that is scraping matches from the list created from starting and ending match number
def scrape_series():
    # removing text from caution text
    window.caution_text.delete(1.0, END)
    # creating scraping driver
    driver = create_driver()
    scrape_updater = data_scraper.Scraper(str(window.menu3_var.get()), driver, window.sleeping_time)
    # opening the website
    driver.get(f"https://www.whoscored.com")
    time.sleep(2)
    # clicking the agree button before opening site
    agree_button = driver.find_element(By.XPATH, '//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]')
    agree_button.click()
    # creating series list
    try:
        start_point = int(window.start_id.get())
        end_point = int(window.end_id.get()) + 1
        series_list = [i for i in range(start_point, end_point)]
    except:
        window.caution_text.insert(END, "Wrong series numbers!!")
    else:
        # scraping for each match in series_list
        for match in series_list:
            scrape_updater.scraping(match)
            window.caution_text.insert(END, scrape_updater.communicate)
            window.caution_text.insert(END,
                                       f"{series_list.index(match) + 1}/{len(series_list)} already tried, "
                                       f"{len(scrape_updater.failed_list)} failed \n")
            window.update()
    window.caution_text.insert(END, f"Matches failed: {scrape_updater.failed_list}")
    # saving failed_list from scrape_updater as txt file in data catalogue
    with open(f'data/failed_file.txt', "a") as file2:
        file2.write("\n".join(str(item) for item in scrape_updater.failed_list))
    driver.close()

import os
with open("data/leagues.txt") as file:
    leagues_dict = json.loads(file.read())
    leagues=leagues_dict.keys()

for league in leagues:
    if not os.path.isdir(f'data/{league}'):
        os.mkdir(f'data/{league}')


window = Window(get_matches_to_update, matches_already_scraped, scrape_update, scrape_series, create_csv)

window.mainloop()
