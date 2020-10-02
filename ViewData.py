import csv
import datetime
import math
import matplotlib.pyplot as plt
import numpy as np

# TODO: plot functions from desmos using the date format.
def roundup(x):
    return int(math.ceil(x / 100.0)) * 100

x = []
y = []
yDelta = [0]
xDelta = []
day1 = 0
# Load data
with open('PlaytimeData.csv', 'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        x.append(datetime.datetime.strptime(row[0], "%d/%m/%Y").date())
        y.append(int(row[1]) / 60)
# find deltas
for i in range(1, len(y)):
    yDelta.append(y[i] - y[i-1])
# set day 1 (to find deltas for x
day1 = x[0]
for date in x:
    xDelta.append((date - day1).days)


# Graphs

plt.figure(figsize=(6,9))
plt.suptitle('Playtime graphs', fontsize=18)
# TOTAL
plt.subplot(211)
# total playtime
plt.plot(xDelta, y, 'ro', label="Playtime (hours)")
# average playtime
m, c = np.polyfit(xDelta, y, 1)
npxDelta = np.array(xDelta)
plt.plot(npxDelta, m*npxDelta + c, label="Average playtime")
# average playtime from the past week
m, c = np.polyfit(xDelta[-7:], y[-7:], 1)
npxDelta2 = np.array(xDelta[-7:])
plt.plot(npxDelta2, m*npxDelta2 + c, label="Past week average")

plt.xlabel(f'days since {x[0].strftime("%d/%m/%Y")}')
plt.ylabel('hours')
plt.title("Total playtime")
plt.legend()

plt.subplot(212)
# BARS
plt.bar(xDelta, yDelta)
plt.xlabel(f'days since {x[0].strftime("%d/%m/%Y")}')
plt.ylabel('hours')
plt.title("Playtime per day")

# Stats
print("GENERAL STATISTICS")
print(f"Average playtime is {np.round(m, 2)} hours p. day ({np.round(m*7, 2)} p. week).")
print(f"Highest playtime is {max(yDelta)} hours on {x[yDelta.index(max(yDelta))].strftime('%d/%m/%Y')}.")
hoursLeft = np.round(roundup(y[-1]) - y[-1], 2)
daysLeft = math.ceil(hoursLeft / m)
print(f"Next 100 hour mark ({roundup(y[-1])} hours) is {hoursLeft} hours away! You can get that in around {daysLeft} days.")

# Show graphs after printing statistics
plt.show()