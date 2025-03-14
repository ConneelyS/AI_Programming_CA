import os, requests, json, csv, time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

###### Problem 4 (22 Marks)
# How many data points are there in this data set?
# What are the data types of the columns?
# What are the column names?
# How many species of flower are included in the data? 

df = pd.read_csv('iris.csv')
# print(df.head())

shape_of_data = df.shape
print(f"Data points: {shape_of_data[0]}\n")

datatypes = df.dtypes
print(f"Data Types of each Column:\n{datatypes}")

column_list = df.columns.tolist()
print(f"\nColumn Names: {column_list}")

species_set = set(df.Species.to_list())
print(f"Species in dataset: {species_set}")

# Using 1-indexing the error is located in the 35th and 38th rows
# Data must be changed at index 35 and 38 using iloc
# print(f"\n{df.iloc[37]}")
# Sepal.Length       4.9
# Sepal.Width        3.1
# Petal.Length       1.5
# Petal.Width        0.1
# Species         setosa

# print(f"\n{df.iloc[40]}")
# Sepal.Length       4.9
# Sepal.Width        3.1
# Petal.Length       1.5
# Petal.Width        0.1
# Species         setosa

# Updating the value of row 35
df.iloc[37, 3] = 0.2
print(f"\n{df.iloc[37]}")

# Updating the value of row 38
# print(df.iloc[40])
df.iloc[40] = [4.9, 3.6, 1.4, 0.1, 'setosa']
print(f"\n{df.iloc[40]}")

# Creating a copy of the DataFrame
copy_df = df
petal_ratio = copy_df['Petal.Width']
# print(petal_ratio)

# Adding both new columns to the DataFrame
copy_df['Petal Ratio'] = copy_df['Petal.Length'] / copy_df['Petal.Width']
copy_df['Sepal ratio'] = copy_df['Sepal.Length'] / copy_df['Sepal.Width']

# print(copy_df.head())
# copy_df.to_csv("iris_corrected.csv", index=False)

# Calculating the correlation of numeric values in the DataFrame
data_correlation = copy_df.corr(numeric_only=True)
# print(data_correlation)

### CORRELATION HEATMAP ###
# Mask used to remove mirrored data from the correlation visualisation
mask = np.triu(np.ones_like(data_correlation, dtype=bool))
# sns.heatmap(data_correlation, cmap='viridis', vmin=-1, vmax=1, center=0, annot=True, square=True, linewidths=.5, mask=mask)

# Creating a correlation matrix with the diagonal values removed to allow min
#   and max values to be calculated correctly without self correlation values
data_correlation_copy = data_correlation
np.fill_diagonal(data_correlation_copy.values, np.nan)
print(f"\nCorrelation Matrix without diganol vlaues removed\n{data_correlation_copy}\n")

### Calculating the Min and Max values for the correlation matrix
# Calculating .max() value will not work as expected due to diagonal correlations = 1
# Flattening the correlation data into a list to sort and get new max value below 1

min_list_values = list(data_correlation_copy.min())
print(f"Min Value: {sorted(min_list_values)[0]}")

max_list_values = list(data_correlation_copy.max())
print(f"Max Value: {sorted(max_list_values)[-1]}")

### SCATTERPLOT WITH REGRESSION ###
# sns.lmplot(data=copy_df, x="Petal Ratio", y="Sepal ratio", hue="Species")
# plt.xlabel("Petal Ratio")
# plt.ylabel("Sepal Ratio")

### PAIRPLOT ###
sns.pairplot(copy_df, hue='Species')

# Uncomment whichever plot you would like to generate to show
plt.show()