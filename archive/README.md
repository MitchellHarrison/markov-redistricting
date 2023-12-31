## Data Scraping for markov-redistricting


### CCI-District-Map-2020.png

Map displaying all of Colorado's 64 counties, along with their neighboring counties.
Source: https://ccionline.org/info-center-library/maps/

### county_adjacency.txt

Adjacent county data sourced from the US Census at https://www.census.gov/programs-surveys/geography/library/reference/county-adjacency-file.html \[1\]

Lists all counties and their adjacent neighbors in "all 50 states, the District of Columbia, Puerto Rico and the Island Areas (American Samoa, the Commonwealth of the Northern Mariana Islands, Guam, and the U.S. Virgin Islands)." \[1\]

When the data was collected, the page was last revised on December 16, 2021.


### county.csv

Cleaned CSV file that takes in all \[County, Neighbor\] pairs in county_adjacency.txt, such that both counties are in Colorado (CO). If there exists a pair of counties \[a, b\] in the CSV, the pair \[b, a\] will also exist in the CSV.


### ColoradoScraper.py

Python file used to clean county_adjacency.txt into county.csv. Ran on Python 3.11.2 and requires the `re` and `csv` libraries to run.


### ColoradoGraph.ipynb

Jupyter notebook that demonstrates how to extract node and edge information from county.csv to be used for NetworkX graphs.

### data_by_county.csv

CSV file compiling various statistics from partisan lean, population, and registered voters.

Data Dictionary:

- County: County name (in Colorado, sorted in alphabetical order)
- PVI: Partisan Voting Index
  - Represents whether a county favors the Democratic or Republican presidential candidate more
  - Positive values indicate that the county favors the Democratic candidate
  - Negative vaues indicate that the county favors the Republican candidate
  - Zero represents a neutral county
- Population: County population based on 2022 estimates
- #Democrats: Number of Democrats in the county as of 2023 estimates
- #Republicans: Number of Republicans in the county as of 2023 estimates
