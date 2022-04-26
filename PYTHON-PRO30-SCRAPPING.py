from tempfile import tempdir
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import requests

START_URL = "https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"
URL =  "https://en.wikipedia.org/wiki/List_of_brown_dwarfs"
browser = webdriver.Chrome("C:/Users/SOUSTIN/Downloads/chromedriver_win32")
browser.get(START_URL)
time.sleep(10)
def scrape():
    headers = ["name", "distance", "mass", "radius"]
    star_data = []
    new_star_data = []
    final_star_data = []
    for i in range(0, 98):
        soup = BeautifulSoup(browser.page_source,"html.parser")
        star_table = soup.find('table')
        temp_list = []
        table_rows = star_table.find_all('tr')
        for tr in table_rows:
            td = tr.find_all('td')
            row = [i.text.rstrip() for i in td]
            temp_list.append(row)
        
        Star_names = []
        Distance = []
        Mass = []
        Radius = []
        Lum = []

        for i in range(1, len(temp_list)):
            Star_names.append(temp_list[i][1])
            Distance.append(temp_list[i][3])
            Mass.append(temp_list[i][5])
            Radius.append(temp_list[i][6])
            Lum.append(temp_list[i][7])

    def scrape_more(hyperlink):
        page = requests.get(URL)
        soup = BeautifulSoup(page.text, 'html.parser')
        star_table = soup.find_all('table')
        table_rows = star_table[7].find_all('tr')
        for table_tag in soup.find_all("table", attrs={"class":"fact_row"}):
            td_tags = table_tag.find_all("td")
            temp_list = []
            for td_tag in td_tags:
                try:
                    temp_list.append(td_tag.find_all("div", attrs={"class":"value"})[0].contents[0])
                except:
                    temp_list.append("")
                new_star_data.append(temp_list)

    scrape()

    for data in star_data:
        scrape_more(data[4])

    for index, data in enumerate(star_data):
        final_star_data.append(data+final_star_data[index])

    with open("final.csv", "w") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(headers)
        csvwriter.writerows(final_star_data)