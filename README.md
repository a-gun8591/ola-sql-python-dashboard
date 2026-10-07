# Ola Booking Analysis (SQL + Python)

SQL and Python analysis of 50,000 Ola ride bookings in Bengaluru: cancellations, revenue, ratings and a dashboard.

![Dashboard](ola_dashboard.png)

## Tools
Python, SQLite, pandas, matplotlib

## Dataset
Bengaluru Ola booking data (50,000 rows, 21 columns): https://github.com/Satyam638/OLA_DataAnalyst_Project

Based on the GeeksforGeeks tutorial: https://www.geeksforgeeks.org/sql/ola-data-analysis-with-sql/
I used SQLite and Python instead of MySQL Workbench and Power BI, and added my own queries and charts.

## Project files
- `load.py` loads the CSV into a SQLite database (`ola.db`)
- `run_queries.py` runs 15 SQL queries (10 from the tutorial and 5 of my own)
- `dashboard.py` builds the dashboard image from the database

## How to run
1. Download the CSV from the dataset link into this folder
2. `pip install pandas matplotlib`
3. `python load.py`
4. `python run_queries.py`
5. `python dashboard.py`

## Key insights
- [Booking success rate and cancellation rates]
- [Top payment method by revenue]
- [Peak booking hours]
- [Most common cancellation reasons]
