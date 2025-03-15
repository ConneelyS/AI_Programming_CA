import os, requests, json, csv, time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Problem 1 (3 Marks)

def get_apod_data(api_key, date):
    url = "https://api.nasa.gov/planetary/apod"
    api_parameters = {"api_key": api_key, "date": date}

    # Making the API call to retrieve APOD data using requests library
    try:
        response = requests.get(url, params=api_parameters)
        
        # Print status code for successful API call
        if response.status_code == 200:
            print(f"API Call Successful: {response.status_code}")

        # Raise a HTTP error if any occurs
        # Returns None value
        response.raise_for_status()

        # Storing the response data from API call to json data
        data = response.json()

        # Creating the payload for returned data as Dictionary
        data_return = {
            "date": data.get("date"),
            "title": data.get("title"),
            "url": data.get("url"),
            "explanation": data.get("explanation"),
            "media_type": data.get("media_type")
        }

        # Returning data in dict from function
        # This is the expected data flow
        return data_return
    
    # Print error if unable to make API call
    # Error is printed and None value is returned
    except requests.exceptions.RequestException as error:
        print(f"Error fetching data for {date}: {error}")
        return None

def fetch_multiple_apod_data(api_key, start_date, end_date, json_file="apod_data.json"):

    # Using pandas to call for multiple dates - pd.date_range more intuiative than datetime lib
    date_range = pd.date_range(start=start_date, end=end_date)
    data_list = []
    
    # Checking if the apod_data.json file exists
    if os.path.exists(json_file):
        try:
            # Opening json file in read mode
            with open(json_file, "r") as read_file:
                # Using json.load to return json object with key value pairs
                data_list = json.load(read_file)
                # print(type(data_list))

            # Eception handling in case of json formatting issues
        except (json.JSONDecodeError, IOError) as jsonLoadError:
            print(f"Error reading existing JSON file: {jsonLoadError}")
    
    # Looping through date arugments provided using pd.date_range
    # This loops allows API to make multiple calls for different dates
    for date in date_range:
        date_str = date.strftime("%Y-%m-%d")
        data = get_apod_data(api_key, date_str)

        # Appending dict data returned from get_apod_data() to list
        # Adding 1 second of wait time to API call
        if data:
            data_list.append(data)
        time.sleep(1)
    
    # Writing to the JSON file
    # Contents of data_list is written to file using json.dump()
    try:
        with open(json_file, "w") as write_file:
            json.dump(data_list, write_file, indent = 4)

    except IOError as jsonWriteError:
        print(f"Error writing to JSON file: {jsonWriteError}")

# Problem 2 (27 Marks)

# This is function reads the data from the json file and stores it in a python dict
def read_apod_data(json_filename="apod_data.json"):
    try:
        # Loads apod_data.json file
        with open(json_filename, "r") as file:
            
            # Creates a list to store json
            data = json.load(file)

        # This code was originally uncommented but because read_apod_data() was
        # being called twice content of the json file was being printed out twice.
        # Decided to add the code to print the contents of json file in other method.
            # Print the contents of json file to console
            # for entry in data:
            #     print(f"Date: {entry['date']}, Title: {entry['title']}")

            # Expected data flow
            return data
    
    # Exception Handling for pssible errors
    except FileNotFoundError:
        print("JSON file not found.")
    except json.JSONDecodeError:
        print("JSON file is empty or corrupted.")
    except IOError as jsonReadError:
        print(f"Error reading JSON file: {jsonReadError}")

        # Returns empty list to the analyze_apod_media() if exception is thrown
    return []

# Moved this code snippet to a seperate method to remove the issue of json content printing twice
def print_json_content():
    # Reading json file content
    json_file_content_data = read_apod_data()
    # Looping through list and printing 'date' and 'title' from each element
    for entry in json_file_content_data:
            print(f"Date: {entry['date']}, Title: {entry['title']}")

def analyze_apod_media(json_filename="apod_data.json"):
    data = read_apod_data(json_filename)

    # Handles error if empty list is returned from read_apod_data()
    # Stops program from crashing on the max() longest_explanation variable
    if not data:
        return
    
    # Variables to store values for the number of images and videos in json file
    image_count = sum(1 for entry in data if entry["media_type"] == "image")
    video_count = sum(1 for entry in data if entry["media_type"] == "video")
    longest_explanation = max(data, key=lambda x: len(x["explanation"]))
    explanation_length = len(longest_explanation['explanation'])

    # Printing counts and length of explanation
    print(f"Image count: {image_count}")
    print(f"Video count: {video_count}")
    print(f"Longest Explanation: {longest_explanation['date']}\nLength: {explanation_length} characters")

def write_csv(json_filename="apod_data.json", csv_file="apod_summary.csv"):
    data = read_apod_data(json_filename)

    # Handles error if empty list is returned from read_apod_data()
    # Stops program from crashing out
    if not data:
        return
    
    # Checking for file using os lib
    file_exists = os.path.exists(csv_file)
    
    try:
        with open(csv_file, "a", newline="") as csv_file:
            # using the csv.writer method to pass data in the csv_file
            writer = csv.writer(csv_file)

            # If the csv file doesn't exist a new one is create with the headings below
            if not file_exists:
                # Headings
                writer.writerow(["Date", "Title", "Media Type", "URL"])
            
            # Adds each new row to the csv file apod_summary
            for entry in data:
                writer.writerow([entry["date"], entry["title"], entry["media_type"], entry["url"]])

    # Throws error if the script couldn't write to the csv file
    except IOError as csvWriteError:
        print(f"Error writing to CSV file: {csvWriteError}")

# Adding a check function to make sure date range is correct
def check_valid_dates(dates):
    # Taking the 
    try:
        date_input = pd.to_datetime(dates, format = "%Y-%m-%d", errors = 'coerce')

        # Creating a date range for valid dates according to the APOD data
        first_apod_date = pd.Timestamp("1995-06-16") # First date available from APOD
        today_date = pd.Timestamp.today() # Setting today as the newest date that can be called

        if not (first_apod_date <= date_input <= today_date):
            print(f"{dates} is not within expected date range ({first_apod_date.date()} - {today_date.date()})")
            return None
        
        return date_input.strftime("%Y-%m-%d") # Returns the expected
    
    except Exception as time_error:
        print(f"Error while checking valid dates {dates}: {time_error}")
        return None

def main():
    # Setting some constants for the script.
    # Editing the date range here will allow for API to call different dates
    API_KEY = os.getenv("NASA_API_KEY")
    START_DATE = "2016-06-01"
    END_DATE = "2016-07-16"

    # Error is API key isn't found
    if not API_KEY:
        raise ValueError("NASA API Key not set up as environment variable")
    
    # Variables for date range checker method
    # Passing constant values to date checker
    start_date = check_valid_dates(START_DATE)
    end_date = check_valid_dates(END_DATE)

    if not start_date or not end_date:
        print("The selected dates are invalid")
        return
    
    # valid_date_range = pd.date_range(start_date, end_date)
    if start_date > end_date:
        print("The START_DATE entered must be before END_DATE")
        return

### Calling of each method is done below ### 

    fetch_multiple_apod_data(API_KEY, START_DATE, END_DATE)
    print_json_content()
    analyze_apod_media()
    write_csv()
    
##### Testing API Call ##### 
    # get_apod_data(API_KEY, START_DATE)
    # fetch_multiple_apod_data(API_KEY, START_DATE, END_DATE)
    # read_apod_data(json_filename="apod_data.json")
    # analyze_apod_media()
    # write_csv()
    # print(API_KEY)

if __name__ == "__main__":
    main()
