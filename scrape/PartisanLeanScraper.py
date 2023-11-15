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
        
        # store all counties and pvi values
        # some rows may not be in sorted order.
        counties_and_pvi = []

        # find the partisan leans stored in the website's table (accessed via html <table> tag)
        # for each row's (<tr>) cell (<td>), add the data into a list then append it into the CSV
        counties = soup.find("table", class_="table table-striped table-bordered table-hover table-condensed")
        rows = counties.find_all("tr")
        for row in rows:
            cells = row.find_all("td")
            
            # only cells with 5 entries have a county and pvi reading
            if len(cells) == 5:
                
                # extract the county and pvi from a row
                long_county = cells[-2].text.strip()
                long_pvi = cells[-1].text.strip()
                
                # find the county as a string
                county = " ".join(long_county.split(" ")[:-1])
                
                # if the county favors democrats, set the bias positive
                # if the county favors republicans, set the bias negative
                party, pvi = long_pvi.split()
                pvi = int(pvi)
                
                if party == "Republican":
                    pvi *= -1
                    
                # add this combination to the list
                counties_and_pvi.append([county, pvi])
        
        # sort the counties in alphabetical order
        counties_and_pvi.sort()
        csv_writer.writerows(counties_and_pvi)

# main method that calls the web scraper function
if __name__ == "__main__":
    pvi_site = "https://www.zipdatamaps.com/counties/state/politics/map-of-partisan-voting-index-for-counties-in-colorado"
    find_partisan_lean(pvi_site)