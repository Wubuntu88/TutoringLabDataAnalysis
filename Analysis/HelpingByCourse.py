import pandas as pd
import matplotlib.pyplot as plt
from dateutil import parser
# import seaborn as sns

data_type_dict = \
    {"Date": str,
     "Department": str,
     "Course": str,
     "Language": str,
     "Tutor": str}

data_frame = pd.read_csv("../AggregateData/aggregate_data.tsv",
                         delimiter="\t",
                         dtype=data_type_dict)
data_frame['DeptCourse'] = data_frame.apply(lambda row: row["Department"] + " " + str(row["Course"]), axis=1)

data_frame.DeptCourse.value_counts().plot(kind='bar')

plt.title("Times GAs Helped Students by Course", fontsize=20),
plt.xlabel("Course", fontsize=16)
plt.ylabel("Helping Counts", fontsize=16)
plt.xticks(rotation=40)
plt.show()
