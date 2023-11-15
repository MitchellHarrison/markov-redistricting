# run on python 3.11.2
import re
from csv import writer

# extracts populations for each colorado county
def find_registered(input_path: str, output_path: str):
    
    with open(input_path, "r") as input_file:
        with open(output_path, "w") as out_file:

            # label the header of the csv with the appropriate labels
            csv_writer = writer(out_file, lineterminator="\n")
            header = ["County", "#Democrats", "#Republicans"]
            csv_writer.writerow(header)

            # skip the header line for the input file
            next(input_file, None)
            
            # store all counties and populations in a list
            # we'll sort them by county prior to entering them
            county_dem_rep = []

            # write each row from the txt file to the csv
            for line in input_file:
                
                try:
                    """
                    Minor fixes to the dataset.
                    Making sure that population counts are integers.
                    """
                    cleaned_line = re.sub('[\"]', '', line)
                    county, dem, rep = cleaned_line.split(",")
                    dem = int(dem)
                    rep = int(rep)
                    county_dem_rep.append([county, dem, rep])
                    
                except Exception as e:
                    print(str(e))
                    
            # sort the counties in alphabetical order
            county_dem_rep.sort()
            csv_writer.writerows(county_dem_rep)

# main method that calls the web scraper function
if __name__ == "__main__":
    input_path = "scrape/registered/dem_rep_data.csv"
    output_path = "scrape/merge/registered.csv"
    find_registered(input_path, output_path)
