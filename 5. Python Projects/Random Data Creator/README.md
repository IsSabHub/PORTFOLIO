Sales Data Generator

This is a Python script for generating random sales data for a fictional e-commerce website. The data includes order numbers, product names, prices, quantities, order dates, and shipping addresses. This data can be used for exploration, visualisation, testing and training machine learning models.

Requirements

Python 3
pandas
numpy

Installation

pip install pandas numpy

Run the script with the command 

python generate_sales_data.py.

Usage

The script generates sales data for the months of January to December of a given year. The number of orders for each month is randomly generated based on a normal distribution. The script also randomly selects products and quantities for each order, and generates random order dates and shipping addresses.

By default, the script generates data for the year 2022. You can change the year by modifying the generate_random_time() function in the script.

The output is a CSV file named sales_data.csv, which is saved in the same directory as the script.