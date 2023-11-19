# run on python 3.11.2
import re
from csv import writer

# extracts populations for each colorado county
def find_ethnicity_pct(input_path: str, output_path: str):
    
    with open(input_path, "r") as input_file:
        with open(output_path, "w") as out_file:

            # label the header of the csv with the appropriate labels
            csv_writer = writer(out_file, lineterminator="\n")
            header = ["County", "White"]
            csv_writer.writerow(header)

            # skip the header
            next(input_file, None)
            
            # store white population counts per county
            ethnicity = dict()
            populations = dict()

            # write each row from the txt file to the csv
            for line in input_file:
                
                try:
                    """
                    We'll extract the following columns from each row:
                    - County name           row[4]
                    - County population     row[7]
                    - White male count      row[10]
                    - White female count    row[11]
                    """
                    row = line.split(",")
                    county_name = row[4]
                    county_population = int(row[7])
                    white_male_count = int(row[10])
                    white_female_count = int(row[11])
                    
                    # increase the number of white people per county
                    if county_name not in ethnicity:
                        ethnicity[county_name] = 0
                    ethnicity[county_name] += (white_male_count + white_female_count)
                    
                    # increase the total number of people in the county
                    if county_name not in populations:
                        populations[county_name] = 0
                    populations[county_name] += county_population
                    
                # if something went wrong, print it
                except Exception as e:
                    print(str(e))
                    
            # divide each county population by the total population (to get percentages)
            for key in ethnicity:
                county_pct = ethnicity[key] / populations[key]
                ethnicity[key] = int(100 * county_pct) / 100
                
            # add (key, value) pairs into a list
            rows = []
            for key in sorted(ethnicity.keys()):
                county = key.split(" County")[0]
                rows.append((county, ethnicity[key]))
            csv_writer.writerows(rows)

# main method that calls the web scraper function
if __name__ == "__main__":
    input_path = "scrape/ethnicity/cc-est2022-alldata-08.csv"
    output_path = "scrape/merge/ethnicity.csv"
    find_ethnicity_pct(input_path, output_path)
