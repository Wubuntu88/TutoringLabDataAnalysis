#!/usr/bin/python
import os

"""
This script will go through the data in the RawData folder, process it,
and print out the processed data.  To store the output in a file,
redirect IO to a file.  For example, you could type this on the command line:
./generate_aggregate_file.py > aggregate_data.tsv
"""


def process_line(the_line, date_prefix):
    components = the_line.split('\t')
    components = [comp.strip() for comp in components]
    components[0] = process_time_field(time=components[0], date_prefix=date_prefix)  # add date to time field
    components[3] = process_language_field(language_field=components[3])
    components[4] = process_name(components[4])
    return "\t".join(components)


def process_time_field(time, date_prefix):
    return date_prefix + ' ' + time


def process_language_field(language_field):
    if language_field == '':
        return "NA"
    elif language_field == 'LC-3' or language_field == 'LC3':
        return 'LC3'

    if len(language_field) >= 2:
        index_of_comma = language_field.find(',')  # see if someone put a comma
        if index_of_comma != -1:
            language_field = language_field[:index_of_comma]  # if so, throw away whats after it
        return language_field[0].upper() + language_field[1:].lower()
    else:
        return language_field


def process_name(name):
    return name[0].upper() + name[1:].lower()


records_to_write = []
relative_path_to_data_directory = '../RawData'
file_names = os.listdir(relative_path_to_data_directory)

print("Date\tDepartment\tCourse\tLanguage\tTutor")

for f_name in file_names:
    if f_name == '.DS_Store':
        continue
    comps = f_name.split()
    the_date_str = comps[-1].replace('.tsv', '')
    path_to_the_file = relative_path_to_data_directory + '/' + f_name
    the_file = open(path_to_the_file, 'r')
    header = the_file.readline()  # ignore header
    for line in the_file:
        line = line.rstrip('\n')
        if line[-1] == "\n":
            print("------READ NEWLINE------")
        new_line = process_line(line, the_date_str)
        print(new_line)
    the_file.close()

