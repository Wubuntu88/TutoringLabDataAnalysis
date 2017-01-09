#!/usr/bin/python
import pandas as pd
import matplotlib.pyplot as plt
import time as time
import datetime as datetime

"""
This script creates a box plot showing the quartile distribution
of tutoring times by the hour time bins of the day;
"""


def get_time_bin(date_hour):
    comps = date_hour.split(" ")
    hour = comps[1].split(":")[0]
    am_pm = comps[2]
    time_string = hour + " " + am_pm
    the_time = time.strptime(time_string, "%I %p")
    return the_time


def date_hour_category(row):
    comps = row[0].split(" ")
    the_date = comps[0]
    hour = comps[1].split(":")[0]
    am_pm = comps[2]
    time_string = the_date + " " + hour + " " + am_pm
    return time_string


data_type_dict = \
    {"Date": str,
     "Department": str,
     "Course": str,
     "Language": str,
     "Tutor": str}

data_frame = pd.read_csv("../AggregateData/aggregate_data.tsv",
                         delimiter="\t",
                         dtype=data_type_dict)

data_frame['DateHour'] = data_frame.apply(lambda row: date_hour_category(row=row), axis=1)
gb = data_frame.groupby('DateHour').size()

dates_as_str = gb.index.tolist()
counts = gb.values
# make a hashmap of date hours (key) to tutoring counts (value)
date_hour_to_tutoring_count = {}
assert len(dates_as_str) == len(counts)
for index in range(len(dates_as_str)):
    date_hour = dates_as_str[index]
    date_hour_to_tutoring_count[date_hour] = counts[index]
# print(date_hour_to_tutoring_count)

# now we get the dates
pure_dates = [the_date_hour.split()[0] for the_date_hour in dates_as_str]
# print(pure_dates)
hours = [" " + the_date_hour.split(" ", 1)[1] for the_date_hour in dates_as_str]
hours = list(set(hours))  # remove duplicates

hours.sort(key=lambda hour_pm: datetime.datetime.strptime(hour_pm, " %I %p"))
hours.remove(' 1 AM')
hours.remove(' 2 AM')
# print(hours)

pure_dates_sorted_no_dups = list(set(pure_dates))
pure_dates_sorted_no_dups.sort(key=lambda the_date: datetime.datetime.strptime(the_date, "%Y-%m-%d"))
# print(pure_dates_sorted_no_dups)

# now we will create a big array of all the date hour times
all_date_hours = []
for the_pure_date in pure_dates_sorted_no_dups:
    for le_hour in hours:
        all_date_hours.append(the_pure_date + le_hour)
# print(all_date_hours)

tutoring_counts_for_day_hour = [0 for x in range(len(all_date_hours))]

for i in range(len(all_date_hours)):
    current_date_hour = all_date_hours[i]
    if current_date_hour in date_hour_to_tutoring_count:
        tutoring_counts_for_day_hour[i] = date_hour_to_tutoring_count[current_date_hour]
# print(tutoring_counts_for_day_hour)


date_hour_data_frame = pd.DataFrame(data={"date_hour": all_date_hours,
                                          "tutoring_counts": tutoring_counts_for_day_hour})
date_hour_data_frame['JustHour'] = date_hour_data_frame.apply(lambda row: row[0].split(" ", 1)[1], axis=1)

trimmed_hours = [hour.strip() for hour in hours]

if len(trimmed_hours) > 10:  # gets rid of any hours after 8pm (or 7pm - 8pm slot)
    trimmed_hours = trimmed_hours[:len(trimmed_hours)-2]

data_in_bins = [[] for l in trimmed_hours]
for index, row in date_hour_data_frame.iterrows():
    the_hour = row['JustHour']
    try:
        idx = trimmed_hours.index(the_hour)

        data_in_bins[idx].append(row["tutoring_counts"])
    except ValueError:
        print(the_hour, " not found in hours array")
        continue

# print(date_hour_data_frame)
z = zip(hours, data_in_bins)
print(list(z))

plt.boxplot(data_in_bins)
plt.xticks(range(1, len(trimmed_hours)+1), trimmed_hours)
plt.title("Box Plot of Helping Times by hour", fontsize=20)
plt.xlabel("Hour Bin", fontsize=16)
plt.ylabel("Times Helped", fontsize=16)
plt.show()
