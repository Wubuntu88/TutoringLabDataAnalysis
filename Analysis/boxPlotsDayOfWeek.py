#!/usr/bin/python
import pandas as pd
import matplotlib.pyplot as plt
from dateutil import parser

"""
This script creates a box plot showing the quartile distribution
of tutoring times by the day of the week;
"""

data_type_dict = \
    {"Date": str,
     "Department": str,
     "Course": str,
     "Language": str,
     "Tutor": str}

data_frame = pd.read_csv("../AggregateData/aggregate_data.tsv",
                         delimiter="\t",
                         dtype=data_type_dict)

data_frame['JustDate'] = data_frame.apply(lambda row: row[0].split()[0], axis=1)
gb = data_frame.groupby('JustDate').size()

dates_as_str = gb.index.tolist()
counts = gb.values

mondays, tuesdays, wednesdays, thursdays, fridays = [[] for _ in range(5)]

dates_counts_zip = zip(dates_as_str, counts)


for date_count_tuple in dates_counts_zip:
    day_of_week = parser.parse(date_count_tuple[0]).weekday()  # 0-4 is Mon-Fri
    the_count = int(date_count_tuple[1])
    if day_of_week == 0:
        mondays.append(the_count)
    elif day_of_week == 1:
        tuesdays.append(the_count)
    elif day_of_week == 2:
        wednesdays.append(the_count)
    elif day_of_week == 3:
        thursdays.append(the_count)
    elif day_of_week == 4:
        fridays.append(the_count)
    else:
        raise Exception("Invalid day of week")

data = [mondays, tuesdays, wednesdays, thursdays, fridays]
names = ["M", "Tu", "W", "Th", "F"]
plt.boxplot(data)
plt.xticks(range(1, 6), names)
plt.title("Box Plot of Helping Times by day of week", fontsize=20)
plt.xlabel("Day of Week", fontsize=16)
plt.ylabel("Times Helped", fontsize=16)
plt.show()
