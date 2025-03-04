import os, requests, json, csv, time
import pandas as pd
import numpy as np

# Problem 1 (3 Marks)

def get_apod_data(api_key, date):
    url = "https://api.nasa.gov/planetary/apod"
    params = {"api_key": api_key, "date": date}

    try:
        response = requests.get(url, params=params)
        
        # Print status code for successful API call
        if response.status_code == 200:
            print(f"API Call Successful: {response.status_code}")

        response.raise_for_status()
        data = response.json()

        data_return = {
            "date": data.get("date"),
            "title": data.get("title"),
            "url": data.get("url"),
            "explanation": data.get("explanation"),
            "media_type": data.get("media_type")
        }

        return data_return
    
    # Print error if unable to make API call
    except requests.exceptions.RequestException as error:
        print(f"Error fetching data for {date}: {error}")
        return None

def fetch_multiple_apod_data(api_key, start_date, end_date, json_filename="apod_data.json"):

    # Using pandas to call for multiple dates - pd.date_range more intuiative than datetime lib
    date_range = pd.date_range(start=start_date, end=end_date)
    data_list = []
    
    # Checking if the apod_data.json file exists
    if os.path.exists(json_filename):
        try:
            with open(json_filename, "r") as file:
                data_list = json.load(file)
                # print(type(data_list))
        except (json.JSONDecodeError, IOError) as jsonLoadError:
            print(f"Error reading existing JSON file: {jsonLoadError}")
    
    for date in date_range:
        date_str = date.strftime("%Y-%m-%d")
        data = get_apod_data(api_key, date_str)

        if data:
            data_list.append(data)
        time.sleep(1)
    
    # Writing to the JSON file
    # Contents of data_list is written to file using json.dump()
    try:
        with open(json_filename, "w") as file:
            json.dump(data_list, file, indent = 4)

    except IOError as jsonWriteError:
        print(f"Error writing to JSON file: {jsonWriteError}")


# Problem 2 (27 Marks)

def read_apod_data(json_filename="apod_data.json"):
    try:
        # Loads apod_data.json file
        with open(json_filename, "r") as file:
            
            # Creates a list to store json
            data = json.load(file)

            # Print the contents of json file to console
            for entry in data:
                print(f"Date: {entry['date']}, Title: {entry['title']}\nDataType: {type(entry)}")

            return data
        
    except FileNotFoundError:
        print("JSON file not found.")
    except json.JSONDecodeError:
        print("JSON file is empty or corrupted.")
    except IOError as jsonReadError:
        print(f"Error reading JSON file: {jsonReadError}")

        # Returns empty list to the analyze_apod_media() if exception is thrown
    return []

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

def write_csv(json_filename="apod_data.json", csv_filename="apod_summary.csv"):
    data = read_apod_data(json_filename)

    # Handles error if empty list is returned from read_apod_data()
    # Stops program from crashing out
    if not data:
        return
    
    file_exists = os.path.exists(csv_filename)
    
    try:
        with open(csv_filename, "a", newline="") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Date", "Title", "Media Type", "URL"])
            
            for entry in data:
                writer.writerow([entry["date"], entry["title"], entry["media_type"], entry["url"]])
    except IOError as csvWriteError:
        print(f"Error writing to CSV file: {csvWriteError}")

if __name__ == "__main__":
    API_KEY = os.getenv("NASA_API_KEY")
    START_DATE = "2020-01-01"
    END_DATE = "2020-01-10"

    if not API_KEY:
        raise ValueError("NASA API Key not set up as environment variable")
    
    # fetch_multiple_apod_data(API_KEY, START_DATE, END_DATE)
    # analyze_apod_media()
    # write_csv()
    
    ##### Testing ##### 
    # get_apod_data(API_KEY, START_DATE)
    # fetch_multiple_apod_data(API_KEY, START_DATE, END_DATE)
    # read_apod_data(json_filename="apod_data.json")
    # analyze_apod_media()
    # write_csv()
    # print(API_KEY)

# Problem 3 (18 Marks)

array = np.random.randint(10, 101, size = (20, 5))

print(array)
# print(f"Rows: {array.shape[0]}\nColumns: {array.shape[1]}")

# Checking if values in array are Even
# print(np.where(array % 2 == 0, True, False))

# Checking sum of the values across rows
print(sum(array))
# print(array.sum(0))
print(np.where(array.sum(0) % 2 == 0, True, False))

# if np.where(array.sum(0) % 2 == 0, True, False):
#     array[-1] + 1

print(np.any(array, where = (array.sum(0) % 2 == 0)))
print(array[0][0])

# if np.any(array, where = (array.sum(0) % 2 == 0)):
    # print(np.all(array.item))
# print(np.any(array, 0, where = (array.sum(0) % 2 == 0)))

