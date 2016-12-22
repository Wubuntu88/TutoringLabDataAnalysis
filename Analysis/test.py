#!/usr/bin/python
import pandas as pd
import matplotlib.pyplot as plt
from dateutil import parser


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

# take Friday out
date_count_tuple = zip(dates_as_str, counts)
the_dates = []
the_counts = []
for tup in date_count_tuple:
    if parser.parse(tup[0]).weekday() != 4:
        the_dates.append(tup[0])
        the_counts.append(tup[1])


plt.plot_date(x=the_dates, y=the_counts, fmt='r-', linewidth=2)
plt.xticks(rotation=10)

plt.title("Helping Instances per day: Fall 2016 Semester (without Friday)", fontsize=16)
plt.xlabel("Date", fontsize=16)
plt.ylabel("helping instance count", fontsize=16)
plt.show()
