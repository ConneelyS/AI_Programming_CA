import os, requests, json, csv, time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

##### Problem 3 (18 Marks)

def generate_random_array():
    array = np.random.randint(10, 101, size = (20, 5))
    return array

def get_array_shape(array):
    array_shape = array.shape
    return array_shape

def adjust_rows_to_even(array):
    # Storing sum total for each row in array
    row_sum_total = array.sum(1)

    # Boolean mask for each row sum that is odd or even
    odd_rows = row_sum_total % 2 

    # Selects a random int between low=0 and high=5 and stores in NDArray of length 20
    random_odd = np.random.randint(0, 5, size = 20)

    array[np.arange(20), random_odd] += odd_rows
    # array[x, y] += odd_rows(1 OR 0)
    # [0, 3] if odd + 1
    # [1, 2] if odd + 1
    # [2, 1] if even + 0
    # [3, 3] if even + 0
    # Numpy uses efficient broadcasting to avoid using IF statments

def get_array_total(array):
    array_sum_total = array.sum()
    return array_sum_total

def adjust_sum_total(array):
    # Checking if array sum is divisible by 5
    array_modulo_remainder = array_sum_total % 5

    # Picking a random element in the inital NDArray to adjust the value of
    row = np.random.randint(0, 20)
    column = np.random.randint(0, 5)

    # Subtracting the modulo remainder from the element picked at random to make the sum divisible 
    array[row, column] -= array_modulo_remainder
    array_new_sum_total = array_sum_total - array_modulo_remainder

    return array_new_sum_total

def divisable_5_and_3(array):
    # Creating a Boolean Mask for values % 5 and 3 == 0
    mask = (array % 5 == 0) & (array % 3 == 0)
    return mask

def replace_with_mean(array):
    # Replace elements > 75 by the mean for entire array
    # mean_of_array = array.mean()

    array[array > 75] = array.mean()
    # print(f"NUMPY ARRAY VALUES OVER 75 REPLACED BY MEAN\n{array}")

    over_75_bool_mask = array > 75
    return over_75_bool_mask

def get_standard_dev(array):
    standard_deviation = np.std(array)
    return standard_deviation

def get_mean(array):
    mean_value = np.mean(array)
    return mean_value

def get_median(array):
    median_value = np.median(array)
    return median_value

# Calling methods
array = generate_random_array()
array_shape = get_array_shape(array)
array_sum_total = get_array_total(array)
div_mask = divisable_5_and_3(array)
over_75_bool_mask_2 = replace_with_mean(array)
array_new_sum_total = adjust_sum_total(array)
standard_deviation = get_standard_dev(array)
mean_value = get_mean(array)
median_value = get_median(array)

# Print the full NDArray
# print(f"INITAL NUMPY ARRAY GENERATED\n{array}")

# Printing the shape of the NDArray (rows, columns)
print(f"Array Shape\nRows: {array_shape[0]}\nColumns: {array_shape[1]}")

# Printing sum total of the array after adjusting values to multiples of 5 and all rows to be even
array_sum_total = get_array_total(array)
print(f"\nSum total of array values: {array_new_sum_total}")

# Printing values that are divisable by 5 and 3
print(f"Divisable by 5 and 3: {array[div_mask]}")

# Checking for any values in the array over 75
print(f"\n{array}")
print(f"Values > 75 = {over_75_bool_mask_2.any(where=array > 75)}")

# Printing the statistical operations
print(f"\nPERFORMING STATISTICAL OPERATIONS")
print(f"Standard Deviation: {standard_deviation}")
print(f"Mean: {mean_value}")
print(f"Median: {median_value}")
