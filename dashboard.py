import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

BASE = os.path.dirname(os.path.abspath(__file__))
con = sqlite3.connect(os.path.join(BASE, "ola.db"))
T = "Ola_Booking_Table"
OUT = os.path.join(BASE, "screenshots")
os.makedirs(OUT, exist_ok=True)


def q(sql):
    return pd.read_sql(sql, con)


# ---- Data for each chart ----
kpi = q(f"""SELECT COUNT(*) AS total_rides,
                   SUM(CASE WHEN "Booking Status"='Success'
                            THEN "Booking Value" ELSE 0 END) AS total_value
            FROM {T};""").iloc[0]

by_vehicle = q(f"""SELECT "Vehicle Type" AS vehicle, SUM("Booking Value") AS value
                   FROM {T} WHERE "Booking Status"='Success'
                   GROUP BY vehicle ORDER BY value DESC;""")

by_payment = q(f"""SELECT "Payment Method" AS method, SUM("Booking Value") AS value
                   FROM {T} WHERE "Booking Status"='Success'
                   GROUP BY method ORDER BY value DESC;""")

status = q(f"""SELECT "Booking Status" AS status, COUNT(*) AS n
               FROM {T} GROUP BY status ORDER BY n DESC;""")

distance = q(f"""SELECT "Ride Distance" AS d FROM {T}
                 WHERE "Ride Distance" IS NOT NULL;""")

cust_reasons = q(f"""SELECT "Reason for Cancelling by Customer" AS reason, COUNT(*) AS n
                     FROM {T} WHERE "Reason for Cancelling by Customer" IS NOT NULL
                     GROUP BY reason ORDER BY n DESC;""")

drv_reasons = q(f"""SELECT "Reason for Cancelling by Driver" AS reason, COUNT(*) AS n
                    FROM {T} WHERE "Reason for Cancelling by Driver" IS NOT NULL
                    GROUP BY reason ORDER BY n DESC;""")

ratings = q(f"""SELECT "Vehicle Type" AS vehicle,
                       AVG("Customer Rating") AS customer,
                       AVG("Driver Ratings") AS driver
                FROM {T} GROUP BY vehicle;""")

by_hour = q(f"""SELECT CAST(SUBSTR("Time", 1, 2) AS INTEGER) AS hour, COUNT(*) AS n
                FROM {T} GROUP BY hour ORDER BY hour;""")


# ---- Combined dashboard ----
fig, ax = plt.subplots(3, 3, figsize=(20, 14))
fig.suptitle(
    f"Ola Bengaluru Bookings Dashboard   |   Total rides: {int(kpi.total_rides):,}"
    f"   |   Successful booking value: Rs {kpi.total_value:,.0f}",
    fontsize=16, fontweight="bold",
)

ax[0, 0].bar(by_vehicle.vehicle, by_vehicle.value, color="#2a9d8f")
ax[0, 0].set_title("Booking value by vehicle type")
ax[0, 0].tick_params(axis="x", rotation=45)

ax[0, 1].barh(by_payment.method, by_payment.value, color="#e9c46a")
ax[0, 1].set_title("Revenue by payment method")

ax[0, 2].pie(status.n, labels=status.status, autopct="%1.1f%%", startangle=90)
ax[0, 2].set_title("Booking status share")

ax[1, 0].hist(distance.d, bins=20, color="#264653")
ax[1, 0].set_title("Ride distance distribution")
ax[1, 0].set_xlabel("Distance")

ax[1, 1].barh(cust_reasons.reason, cust_reasons.n, color="#e76f51")
ax[1, 1].set_title("Customer cancellation reasons")
ax[1, 1].invert_yaxis()

ax[1, 2].barh(drv_reasons.reason, drv_reasons.n, color="#f4a261")
ax[1, 2].set_title("Driver cancellation reasons")
ax[1, 2].invert_yaxis()

x = range(len(ratings))
w = 0.4
ax[2, 0].bar([i - w / 2 for i in x], ratings.customer, w, label="Customer", color="#2a9d8f")
ax[2, 0].bar([i + w / 2 for i in x], ratings.driver, w, label="Driver", color="#264653")
ax[2, 0].set_xticks(list(x))
ax[2, 0].set_xticklabels(ratings.vehicle, rotation=45)
ax[2, 0].set_title("Average ratings by vehicle type")
ax[2, 0].legend()

ax[2, 1].plot(by_hour.hour, by_hour.n, marker="o", color="#e76f51")
ax[2, 1].set_title("Bookings by hour of day")
ax[2, 1].set_xlabel("Hour")

ax[2, 2].axis("off")
ax[2, 2].text(0.5, 0.6, f"{int(kpi.total_rides):,}\nTotal rides", ha="center",
              fontsize=22, fontweight="bold")
ax[2, 2].text(0.5, 0.2, f"Rs {kpi.total_value:,.0f}\nSuccessful booking value", ha="center",
              fontsize=22, fontweight="bold")

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig(os.path.join(OUT, "ola_dashboard.png"), dpi=150)
print("Saved:", os.path.join(OUT, "ola_dashboard.png"))
plt.show()
con.close()
