#!/usr/bin/python
import pandas as pd
import matplotlib.pyplot as plt
from dateutil import parser
import seaborn as sns

data_type_dict = \
    {"Date": str,
     "Department": str,
     "Course": str,
     "Language": str,
     "Tutor": str}

data_frame = pd.read_csv("../AggregateData/aggregate_data.tsv",
                         delimiter="\t",
                         dtype=data_type_dict)