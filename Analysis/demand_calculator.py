#!/usr/bin/python
import pandas as pd
import numpy as np
import time as time
from datetime import datetime
import matplotlib.pyplot as plt


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

days_of_the_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

hour_bin_indices = ['10 AM', '11 AM', '12 PM', '1 PM', '2 PM', '3 PM', '4 PM', '5 PM', '6 PM', '7 PM']
hour_bin_indices_set = set(hour_bin_indices)

demand_data_frame_counts = pd.DataFrame({
    'Monday': pd.Series([[] for _ in range(0, len(hour_bin_indices))], index=hour_bin_indices),
    'Tuesday': pd.Series([[] for _ in range(0, len(hour_bin_indices))], index=hour_bin_indices),
    'Wednesday': pd.Series([[] for _ in range(0, len(hour_bin_indices))], index=hour_bin_indices),
    'Thursday': pd.Series([[] for _ in range(0, len(hour_bin_indices))], index=hour_bin_indices)
})

# print(demand_data_frame_counts)

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
date_hour_counts = data_frame.groupby('DateHour').size()

date_hour_set = set(date_hour_counts.index.values)
date_set = set([line.split()[0] for line in date_hour_counts.index.values])

# create indexes for date hour bins that do not have any counts (nobody asked for help in those times)
# add that index to the series with the value of 0 (because no one asked for help)
for date in date_set:
    for hour in hour_bin_indices:
        the_date_time = date + " " + hour
        if the_date_time not in date_hour_set:
            date_hour_counts[the_date_time] = 0

# loop through the date hour conts, and put the values in the corresponding locations in the dataframe

friday_str = 'Friday'
for date_hour, count in date_hour_counts.iteritems():
    comps = date_hour.split(" ", 1)
    just_the_date_str = comps[0]
    just_the_time_str = comps[1]
    just_the_date_as_datetime_object = datetime.strptime(just_the_date_str, "%Y-%m-%d")
    the_day_of_week = days_of_the_week[datetime.weekday(just_the_date_as_datetime_object)]
    if the_day_of_week != friday_str and just_the_time_str in hour_bin_indices_set:
        day_of_week_and_hour_demand_list = demand_data_frame_counts[the_day_of_week][just_the_time_str]
        day_of_week_and_hour_demand_list.append(count)

# this calculates averages
demand_data_frame_averages = demand_data_frame_counts.applymap(lambda element: sum(element) / len(element))
# this calculates medians
#demand_data_frame_averages = demand_data_frame_counts.applymap(lambda elements_list: np.median(np.array(elements_list)))


# print(demand_data_frame_averages)
demand_data_frame_averages = demand_data_frame_averages.reindex(columns=['Monday', 'Tuesday', 'Wednesday', 'Thursday'])
# print(demand_data_frame_averages)

demand_data_frame_averages.plot(kind='bar')
plt.title('Average People helped per hour bin Monday-Thursday', fontsize=36)
plt.xlabel('hour bin', fontsize=28)
plt.ylabel('number of students helped', fontsize=28)
plt.tick_params(labelsize=22)
plt.xticks(rotation=0)
plt.show()




