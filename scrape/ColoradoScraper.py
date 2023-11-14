# run on python 3.11.2
import re
from csv import writer

"""
Input:  string (containing county name, "County", and state name)

Output: row of length == 3 where
        row[0] = county name
        row[1] = "County"
        row[2] = state name     (two-char string)

"""
def find_county_name(string):
    
    """
    Base Case:
    The county only consists of one word.
    
    Example:
    string = 'Garfield County CO'
    row    = ['Garfield', 'County', 'CO']
    
    Checking for len(row) == 3 guarantees that the county only has one word.
    """
    row = string.split(" ")
    if len(row) == 3:
        return row
    
    # the last three entries consist of ["County", state, ID]
    # concatenate everything but the last three entries
    name = " ".join(row[:-2])
    return [name] + row[-2:]

# converts a txt file (separated by whitespace) to a csv file
def find_colorado_counties(input_path: str, output_path: str):
    
    with open(input_path, "r") as input_file:
        with open(output_path, "w") as out_file:

            # label the header of the csv with the appropriate labels
            csv_writer = writer(out_file, lineterminator="\n")
            header = ["County", "Neighbor"]
            csv_writer.writerow(header)
            
            # the txt is formatted so that the current county's line has 8 objects
            # in that case, consider this county to be the "target"
            target_county = ""

            # write each row from the txt file to the csv
            for line in input_file:
                
                """
                Cleaning the lines.
                1. Remove commas and quotes from the string via regex prior to splitting.
                2. Split based on \t characters.
                
                If the line has two counties, the row should look like this:
                row = ['Rio Blanco County CO', '08103', 'Garfield County CO', '08045']
                
                If the line only has one county, the row should look like this:
                row = ['', '', 'Moffat County CO', '08081']
                
                We can check if a line has one or two counties by checking if row[0] == ""                
                """
                cleaned_line = re.sub('[,"]', '', line)
                row = cleaned_line.split("\t")
                
                # find all the county instances in the line
                try:
                    
                    """
                    Read above explanation for why row[0] != "" guarantees
                    that a line has two counties.
                    """
                    if row[0] != "":
                        
                        """
                        Find the two counties on the row and convert them into lists
                        For example, for the following row:
                        
                        row = ['Rio Blanco County CO', '08103', 'Garfield County CO', '08045']
                        
                        We can extract:
                        row[0] = 'Rio Blanco County CO'
                        row[2] = 'Garfield County CO'
                        
                        And convert them into lists
                        first  = ['Rio Blanco', 'County', 'CO']
                        second = ['Garfield',   'County', 'CO']
                        
                        """
                        first = find_county_name(row[0])
                        second = find_county_name(row[2])
                        
                        # if the first county isn't in colorado, find the next county
                        if first[2] != "CO":
                            target_county = ""
                            continue
                        
                        # otherwise, find the name of the county
                        target_county = first[0]
                        
                        """
                        If both counties are different names, and are both in Colorado,
                        append the second county's name to the list. In this example,
                        we'll append ['Rio Blanco', 'Garfield']
                        """
                        if second[2] == "CO" and first[0] != second[0]:
                            neighbor_county = second[0]
                            data = [target_county, neighbor_county]
                            csv_writer.writerow(data)
                            
                            
                    else:
                        
                        """
                        Ignore the row if the most recent target county isn't in Colorado.
                        """
                        if target_county == "":
                            continue
                        
                        """
                        If the target county is in CO, we'll add the remaining counties
                        to the CSV. Recall that CO counties can border other states.
                        
                        Recall that if we reached the else statement, the row only has one county.
                        It will look something like this, for example:
                        
                        row = ['', '', 'Moffat County CO', '08081']
                        
                        We can access the neighbor county by getting row[2].
                        
                        After formatting, we can find a row by calling the
                        find_county_name function used previously.
                        
                        neighbor = ['Moffat', 'County', 'CO']
                        neighbor_county = 'Moffat'
                        neighbor_state  = 'CO'
                        """
                    
                        # find the neighbor county's name and state
                        neighbor = find_county_name(row[2])
                        neighbor_county = neighbor[0]
                        neighbor_state = neighbor[2]
                        
                        # check if the county is in colorado
                        # or is the target county and the neighbor county have the same name
                        if neighbor_state != "CO" or target_county == neighbor_county:
                            continue
                        
                        # if the county names are distinct, add the data
                        data = [target_county, neighbor_county]
                        csv_writer.writerow(data)
                
                except Exception as e:
                    print(str(e))

# main method that calls the web scraper function
if __name__ == "__main__":
    input_path = "scrape/county_adjacency.txt"
    output_path = "scrape/county.csv"
    find_colorado_counties(input_path, output_path)
