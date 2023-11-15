# run on python 3.11.2
from bs4 import BeautifulSoup
import requests
from csv import writer

# scrapes a url to get partisan lean for each colorado county
def find_partisan_lean(url: str):
    
    # access the website using BeatifulSoup and requests
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    # open a new csv file in a new folder (SRCMOD/srcmod.csv) to write data into
    with open("scrape/partisan_lean.csv", "w", newline="", encoding="utf8") as f:

        # the header labels each column for readability
        csv_writer = writer(f)
        header = ["County", "PVI"]
        csv_writer.writerow(header)

        # find the partisan leans stored in the website's table (accessed via html <table> tag)
        # for each row's (<tr>) cell (<td>), add the data into a list then append it into the CSV
        counties = soup.find("table", class_="table table-striped table-bordered table-hover table-condensed")
        rows = counties.find_all("tr")
        for row in rows:
            partisan_lean_data = []
            for cell in row.find_all("td"):
                print(cell.text.strip())
            csv_writer.writerow(partisan_lean_data)

# main method that calls the web scraper function
if __name__ == "__main__":
    pvi_site = "https://www.zipdatamaps.com/counties/state/politics/map-of-partisan-voting-index-for-counties-in-colorado"
    find_partisan_lean(pvi_site)