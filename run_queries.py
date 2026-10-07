import os
import sqlite3
import pandas as pd

# Find ola.db next to this script, so it works from any folder
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ola.db")
con = sqlite3.connect(DB_PATH)
T = "Ola_Booking_Table"

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 20)

queries = {
    # ---- Tutorial queries ----
    "Q1. Successful bookings (first 10)": f"""
        SELECT "Booking ID", "Booking Status", "Customer ID", "Vehicle Type"
        FROM {T} WHERE "Booking Status" = 'Success' LIMIT 10;""",

    "Q2. Average ride distance per vehicle type": f"""
        SELECT "Vehicle Type", ROUND(AVG("Ride Distance"), 2) AS avg_distance
        FROM {T} GROUP BY "Vehicle Type";""",

    "Q3. Rides cancelled by customers": f"""
        SELECT COUNT(*) AS cancelled_by_customer
        FROM {T} WHERE "Booking Status" = 'Cancelled by Customer';""",

    "Q4. Top 5 customers by number of rides": f"""
        SELECT "Customer ID", COUNT("Booking ID") AS total_rides
        FROM {T} GROUP BY "Customer ID"
        ORDER BY total_rides DESC LIMIT 5;""",

    "Q5. Driver cancellations: personal & car issues": f"""
        SELECT COUNT(*) AS personal_car_issue
        FROM {T}
        WHERE "Reason for Cancelling by Driver" = 'Personal & Car related issue';""",

    "Q6. Max / min driver rating for Prime Sedan": f"""
        SELECT MAX("Driver Ratings") AS max_rating,
               MIN("Driver Ratings") AS min_rating
        FROM {T} WHERE "Vehicle Type" = 'Prime Sedan';""",

    "Q7. UPI payments (first 10)": f"""
        SELECT "Booking ID", "Vehicle Type", "Payment Method", "Booking Value"
        FROM {T} WHERE "Payment Method" = 'UPI' LIMIT 10;""",

    "Q8. Average customer rating per vehicle type": f"""
        SELECT "Vehicle Type", ROUND(AVG("Customer Rating"), 2) AS avg_customer_rating
        FROM {T} GROUP BY "Vehicle Type";""",

    "Q9. Total booking value of successful rides": f"""
        SELECT SUM("Booking Value") AS total_successful_value
        FROM {T} WHERE "Booking Status" = 'Success';""",

    "Q10. Driver cancellation reasons (first 5)": f"""
        SELECT "Booking ID", "Reason for Cancelling by Driver"
        FROM {T} WHERE "Reason for Cancelling by Driver" IS NOT NULL LIMIT 5;""",

    # ---- Extra queries of your own ----
    "X1. Booking status share (%)": f"""
        SELECT "Booking Status", COUNT(*) AS rides,
               ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM {T}), 2) AS pct
        FROM {T} GROUP BY "Booking Status" ORDER BY rides DESC;""",

    "X2. Revenue by payment method": f"""
        SELECT "Payment Method", COUNT(*) AS rides,
               ROUND(SUM("Booking Value"), 2) AS revenue
        FROM {T} WHERE "Booking Status" = 'Success'
        GROUP BY "Payment Method" ORDER BY revenue DESC;""",

    "X3. Bookings by hour of day": f"""
        SELECT SUBSTR("Time", 1, 2) AS hour, COUNT(*) AS bookings
        FROM {T} GROUP BY hour ORDER BY hour;""",

    "X4. Top customer cancellation reasons": f"""
        SELECT "Reason for Cancelling by Customer" AS reason, COUNT(*) AS n
        FROM {T} WHERE "Reason for Cancelling by Customer" IS NOT NULL
        GROUP BY reason ORDER BY n DESC;""",

    "X5. Top 5 customers by spend (with rank)": f"""
        SELECT "Customer ID", ROUND(SUM("Booking Value"), 2) AS total_spent,
               RANK() OVER (ORDER BY SUM("Booking Value") DESC) AS spend_rank
        FROM {T} WHERE "Booking Status" = 'Success'
        GROUP BY "Customer ID" ORDER BY spend_rank LIMIT 5;""",
}

for title, sql in queries.items():
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)
    try:
        print(pd.read_sql(sql, con).to_string(index=False))
    except Exception as e:
        print("Query failed:", e)

# Helper: see the real values stored in a column (useful for Q5 and Q10)
print("\n" + "=" * 70)
print("Distinct driver cancellation reasons actually in your data")
print("=" * 70)
print(pd.read_sql(
    f'SELECT DISTINCT "Reason for Cancelling by Driver" AS reason FROM {T};', con
).to_string(index=False))

con.close()
