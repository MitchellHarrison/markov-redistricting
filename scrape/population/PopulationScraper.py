# run on python 3.11.2
import re
from csv import writer

# extracts populations for each colorado county
def find_populations(input_path: str, output_path: str):
    
    with open(input_path, "r") as input_file:
        with open(output_path, "w") as out_file:

            # label the header of the csv with the appropriate labels
            csv_writer = writer(out_file, lineterminator="\n")
            header = ["County", "Population"]
            csv_writer.writerow(header)

            # skip the first five lines (as they are useless headers)
            for k in range(5): next(input_file, None)
            
            # store all counties and populations in a list
            # we'll sort them by county prior to entering them
            counties_and_populations = []

            # write each row from the txt file to the csv
            for line in input_file:
                
                try:
                    """
                    Cleaning the lines.
                    1. Remove periods and quotes from the string via regex prior to splitting.
                    2. Split based on \t characters.
                    
                    Since this is a CSV, we can extract each cell value by splitting for commas.        
                    """
                    cleaned_line = re.sub('[.\n]', '', line)
                    row = cleaned_line.split("\",\"")
                    if len(row) != 5: continue
                    
                    # extract the county and population values
                    long_name = re.sub('[,\"]', '', row[0])
                    
                    # format the strings to extract the name and population
                    name = " ".join(long_name.split(" ")[:-2])
                    pop = int(re.sub('[,\"]', '', row[-1]))
                    counties_and_populations.append([name, pop])
                    
                except Exception as e:
                    print(str(e))
                    
            # sort the counties in alphabetical order
            counties_and_populations.sort()
            csv_writer.writerows(counties_and_populations)

# main method that calls the web scraper function
if __name__ == "__main__":
    input_path = "scrape/population/CO-Population-Estimates-2022.csv"
    output_path = "scrape/population.csv"
    find_populations(input_path, output_path)
