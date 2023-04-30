Whoscored v.3

Program is created in purpose of scraping data from whosored.com website.
Program:
- get data from whoscored.com about selected matches
- data from each match is saved as JSON file
- files can be connected in one csv file for each league

The main window of program is divided into 5 frames:
- Match Update
- Scraping from Series
- Creating CSV
- Options
- Cautions

Module Match Update is looking for matches that can be scraped and scrape them.
- You have to select league from menu (lauges are loaded from file leagues.txt).
- Input the ending date for serach (it starts from current data). 
- Date is validate only in terms of being int value. The date must be concluded in the current season. 
- "Search for update" activate function which is looking for matches played between current date and inputed date.
- Label "Matches to update" is displaying number of matches found by "Search for update" funcion.
- Text window displays list of IDs of found matches
- "Check update" butten activate function which read matches already saved in "data" catalog and compare list of read matches with list of founf matches.
- "New matches label" displays difference between list mentioned above - it is the number of matches that should be scraped.
- "Scrape update" button activate function which scrape data for matches that arent already scraped.

Module "Scraping from series" is scraping data for wholeseries of matches.
- You have to select league from menu (lauges are loaded from file leagues.txt).
- There are fields "Start ID" and "End ID" which inputs are starting and ending points of created list of matches
- "Scrape series" button activate function which scrape data for matches from thelist of matches.

Module "Creating CSV" is joining all match files (JSON) into one CSV file.
- You have to select league from menu (lauges are loaded from file leagues.txt).

Options module allows you to set "Sleeping time". It's time that is used in case of scraping as a pause between start of loading the website and start of getting data from website
Than the internet connection is slower than "Sleeping time" bigger should be.

Cautions module displays inforations from other modules:
- "Give correct date!!" - date elements are not integers
- "Wrong series numbers!!" - series numbers are not integers or starting number is greater than ending number

Files:

File data_scraper.py contains class "Scraper" with its method "scraping".
Class Scraper needs for its initiation:
- league name
- scraping driver
- waiting_time
It also generat empty parameters communicate and failed_list.
Method "scraping" needs one argument "match_id".
Method crate dictionary with data scraped from https://www.whoscored.com/Matches/{match_id}.
A the end of scraping proces dictionary is saved as the json file in catalog 'data/{self.league_country_param}/{match_id}.json'.
In case of error during scraping "Scraping error!" in "Cauions" appers. Also there is a sound signal after an error.
If there is no scraping error there is displayed match_id with time that scraping took.


File main_window.py contains class "Window" which creates completeMain Windowof program. It is base on tkinter library.
Class Window is reading leaue list from file "data/leagues.txt".

File json_csv contains class JsonToCsv and its methods get_dir_list and save_data_file.
JsonToCsv object is collecting all data saved in "data" catalog which refers to chosen league.
get_dir_list method is getting directions of all files hat refers to chosen legue
save_data_file is creating csv file from hole list of JSON files.
Class is based on liblaries: csv, datetime, os and json.
