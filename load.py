import sqlite3, pandas as pd

df = pd.read_csv("Bengaluru_Ola_Booking_Data.csv")
conn = sqlite3.connect("ola.db")
df.to_sql("ola_booking_table", conn, if_exists="replace", index=False)

print("Rows, columns:", df.shape)
print(df.columns.tolist())
print(df["Booking Status"].value_counts())
print(pd.read_sql_query("SELECT * FROM ola_booking_table LIMIT 5", conn))
