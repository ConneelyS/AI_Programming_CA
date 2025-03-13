import os, requests, json, csv, time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

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



##### Problem 3 (18 Marks)

array = np.random.randint(10, 101, size = (20, 5))

## Print the full NDArray
# print(array)

## Printing the shape of the NDArray (rows, columns)
# print(f"Rows: {array.shape[0]}\nColumns: {array.shape[1]}")

## Checking if values in array are Even
# print(np.where(array % 2 == 0, True, False))

## Printing the sum of each row in the NDArray
## Checking the sum for each row using axis=1
# print(array.sum(1))

row_sum_total = array.sum(1) # Returns a NDArray containing the sum of each row in array
# print(row_sum_total)

odd_rows = row_sum_total % 2 # Returns a boolean mask NDArray for each row sum that is odd or even
# print(odd_rows)

random_odd = np.random.randint(0, 5, size = 20) # Selects a random int between low=0 and high=5 and stores in NDArray of length 20
# print(random_odd)

array[np.arange(20), random_odd] += odd_rows
# array[x, y] += odd_rows(1 OR 0)
# [0, 3] if odd + 1
# [1, 2] if odd + 1
# [2, 1] if even + 0
# [3, 3] if even + 0
# Numpy uses efficient broadcasting to avoid using IF statments

## Checking total sum of NDArray
array_sum_total = array.sum()
# print(array_sum_total)

# Checking if array sum is divisible by 5
array_modulo_remainder = array_sum_total % 5
# print(f"Remaining: {array_modulo_remainder}")

# Picking a random element in the inital NDArray to adjust the value of
row = np.random.randint(0, 20)
column = np.random.randint(0, 5)

# Subtracting the modulo remainder from the element picked at random to make the sum divisible 
array[row, column] -= array_modulo_remainder
array_new_sum_total = array_sum_total - array_modulo_remainder



###### Problem 4 (22 Marks)
# How many data points are there in this data set?
# What are the data types of the columns?
# What are the column names?
# How many species of flower are included in the data? 

df = pd.read_csv('iris.csv')
# print(df.head())

shape_of_data = df.shape
# print(f"Data points: {shape_of_data[0]}")

column_list = df.columns.tolist()
# print(f"Column Names: {column_list}")

# print(datatypes)
# print(df.columns[0])

datatypes = df.dtypes
# for col in df.columns:
    # print(f"{col} - {datatypes[col]}")

# species_set = set(df.Species.to_list())
# print(species_set)
# print("\n")

# Using 1-indexing the error is located in the 35th and 38th rows
# Data must be changed at index 34 and 37 using iloc
# print(df.iloc[34])
# Sepal.Length       4.9
# Sepal.Width        3.1
# Petal.Length       1.5
# Petal.Width        0.1
# Species         setosa

# print(df.iloc[37])
# Sepal.Length       4.9
# Sepal.Width        3.1
# Petal.Length       1.5
# Petal.Width        0.1
# Species         setosa

# series = df.iloc[37]

# print(df.iloc[37])

# print(series)

# print(len(df.iloc[37]))
# print(df.iloc[37])

# print(df.iloc[37, 3])
# Updating the value of row 37
df.iloc[37, 3] = 0.2
# print(df.iloc[37])

# print(df.iloc[40]) 
df.iloc[40] = [4.9, 3.6, 1.4, 0.1, 'setosa']
# print(df.iloc[40]) 

copy_df = df
petal_ratio = copy_df['Petal.Width']
print(petal_ratio)

copy_df['Petal Ratio'] = copy_df['Petal.Length'] / copy_df['Petal.Width']
copy_df['Sepal ratio'] = copy_df['Sepal.Length'] / copy_df['Sepal.Width']

print(copy_df.head())
# copy_df.to_csv("iris_corrected.csv", index=False)

# print(copy_df.iloc[40])

data_correlation = copy_df.corr(numeric_only=True)
print(data_correlation)

# Mask used to remove mirrored data from the correlation visualisation
mask = np.triu(np.ones_like(data_correlation, dtype=bool))
# sns.heatmap(data_correlation, cmap='viridis', vmin=-1, vmax=1, center=0, annot=True, square=True, linewidths=.5, mask=mask)
# plt.show()

print("##############")
# all_correlation_value = data_correlation
# highest_pairwise_correlation = 
# print(data_correlation.min())
# print(data_correlation.max())

# flattened_values = []

# data_correlation.to_numpy()
# print(type(data_correlation.to_numpy()))

data_correlation_copy = data_correlation
np.fill_diagonal(data_correlation_copy.values, np.nan)
print(data_correlation_copy)

# sns.heatmap(data_correlation_copy, cmap='viridis', vmin=-1, vmax=1, center=0, annot=True, square=True, linewidths=.5, mask=mask)
# plt.show()

### Calculating the Min and Max values for the correlation matrix
# Calculating .max() value will not work as expected due to diagonal correlations = 1
# Flattening the correlation data into a list to sort and get new max value below 1

# print(f"Min: {data_correlation_copy.min()}\nMax: {data_correlation_copy.max()}")

# print(flattened_values < 1)
# new_values = []
# new_values.append(flattened_values < 1)

# for x in new_values:
#     print(x)





# list_correlation_values = np.eye(data_correlation.shape[0], dtype=bool)
# no_diagonal_correlation_values = data_correlation.where(~list_correlation_values).stack()

# min_correlation_value = data_correlation_copy.min()
# max_correlation_value = data_correlation_copy.max()



min_list_values = list(data_correlation_copy.min())
# print(min_list_values)
# print(sorted(min_list_values))
print(f"Min Value: {sorted(min_list_values)[-1]}")

max_list_values = list(data_correlation_copy.max())
# print(max_list_values)
# print(sorted(max_list_values))
print(f"Max Value: {sorted(max_list_values)[-1]}")

# for x in min_list_values:
#     print(x)

# sorted_list = min_list_values.sort()

# print(sorted_list)


# min_correlation_value.to_list()
# max_correlation_value.to_list()

# print(min_correlation_value)
# print(max_correlation_value)

# print(min_correlation_value, max_correlation_value)
# for x in data_correlation.to_numpy():
#     print(x)

# numpy_data = data_correlation.to_numpy()
# print(numpy_data)
# highest_value = numpy_data.max()
# print(highest_value)


# Scatter Plot for Ratio Values

# x_axis = copy_df['Petal Ratio']
# y_axis = copy_df['Sepal ratio']

# sns.lmplot(copy_df, x=x_axis, y=y_axis, hue="Species")

# sns.lmplot(data=copy_df, x="Petal Ratio", y="Sepal ratio", hue="Species")
# plt.xlabel("Petal Ratio")
# plt.ylabel("Sepal Ratio")

# scatter_plot = plt.scatter(x_axis, y_axis)

# sns.scatterplot(copy_df, x=x_axis, y=y_axis, hue="Species")
# sns.regplot(copy_df, x=x_axis, y=y_axis)

# Calculating the Linear Regression using Numpy in order to overlay in over the scatterplot
# m, b = np.polyfit(x_axis, y_axis, 1)
# plt.plot(x_axis, m * x_axis + b, color='red')

sns.pairplot(copy_df, hue='Species')

plt.show()