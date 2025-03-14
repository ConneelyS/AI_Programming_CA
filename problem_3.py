import os, requests, json, csv, time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

##### Problem 3 (18 Marks)

array = np.random.randint(10, 101, size = (20, 5))

## Print the full NDArray
print(f"INITAL NUMPY ARRAY GENERATED\n{array}")

## Printing the shape of the NDArray (rows, columns)
print(f"Rows: {array.shape[0]}\nColumns: {array.shape[1]}")

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
print(f"\nSum total of array values: {array_sum_total}")

# Checking if array sum is divisible by 5
array_modulo_remainder = array_sum_total % 5
# print(f"Remaining: {array_modulo_remainder}")

# Picking a random element in the inital NDArray to adjust the value of
row = np.random.randint(0, 20)
column = np.random.randint(0, 5)

# print(array[row, column])
# Subtracting the modulo remainder from the element picked at random to make the sum divisible 
array[row, column] -= array_modulo_remainder
array_new_sum_total = array_sum_total - array_modulo_remainder

# import timeit

# Work done using Array Indexing and Loops
# new_list = []
# for x in array_list: 
#     for y in x:
#         if (y % 3 == 0) & (y % 5 == 0):
#             new_list.append(y)
# print(f"Divisable by 5 and 3: {new_list}")

# Work completed using Numpy Vectorised NDArrays and Boolean Indexing instead of Loops
# Tested the execution speed of numpy vs loops and numpy was faster every time
mask = (array % 5 == 0) & (array % 3 == 0)
print(f"Divisable by 5 and 3: {array[mask]}")

# Replace elements > 75 by the mean for entire array
mean_of_array = array.mean()
print(f"\nMean of array: {mean_of_array}")

# Checking the array before replacement operation
# print(array)

array[array > 75] = array.mean()
print(f"NUMPY ARRAY VALUES OVER 75 REPLACED BY MEAN\n{array}")

over_75_bool_mask = array > 75
# print(over_75_bool_mask)

standard_deviation = np.std(array)
mean_value = np.mean(array)
median_value = np.median(array)

print(f"\nPERFORMING STATISTICAL OPERATIONS")
print(f"Standard Deviation: {standard_deviation}")
print(f"Mean: {mean_value}")
print(f"Median: {median_value}")
