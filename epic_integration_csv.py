#!/usr/bin/env python3

import csv
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd
from pandas import ExcelWriter
from datetime import date
from datetime import datetime
csv_path = '/Users/olivia/Downloads/AEGeneExpressionData_DATA_LABELS_2021-03-23_1421.csv'


columns_to_keep = {
'Demographics':[(9,28)],
'Vital Signs':[(30,34)],
'Labs': [(36,40)],
'Medications':[(42,48)],
'Problem List':[(50,58)],
'Allergies':[(60,67)]
}

sort_data = {
'Demographics':[],
'Vital Signs': [],
'Labs': [],
'Medications':[],
'Problem List':[],
'Allergies':[]
}

headings_dict = {}
column_ranges = {}
all_data = []
default_cells = [0, 1, 2, 8]
record_num_mrn = {}
csv_file_names = []

def print_dict(dict_name):
    for index, header in dict_name.items():
        print('{} - {}'.format(index, header))

with open(csv_path, 'r') as file:
    data = csv.reader(file)
    for row_index, row in enumerate(data):
        if row_index == 0:
            for cell_index, cell in enumerate(row):
                headings_dict[cell_index] = cell
        else:
            row_type = row[1]
            row_record_num = row[0]
            row_mrn = row[8]
            if row_type == '':
                row_type += 'Demographics'
                # print(row)
                if row_record_num not in record_num_mrn:
                    # print(row_mrn + '-' + row_record_num)
                    record_num_mrn[row_record_num] = row_mrn
            if row_type not in column_ranges:
                cell_index_to_keep = [0, 1, 2, 8]
                start_col_num = columns_to_keep[row_type][0][0]
                end_col_num = columns_to_keep[row_type][0][1]
                for m in range(start_col_num, end_col_num):
                    cell_index_to_keep.append(m)
                column_ranges[row_type] = cell_index_to_keep
            row_data = []
            for x in column_ranges[row_type]:
                row_data.append(row[x])
            all_data.append(row_data)

for x in all_data:
    category = x[1]
    if category == '':
        category += 'Demographics'
    if len(sort_data[category]) == 0:
        category_heading_index = column_ranges[category]
        category_headings = []
        for n in category_heading_index:
            category_headings.append(headings_dict[n])
        # print(category_headings)
        sort_data[category].append(category_headings)
    if category != 'Demographics':
        x[3] = record_num_mrn[x[0]]
        # if category == 'Vital Signs' or category == 'Labs':
        #     x[5] = '"' + str(x[5]) + '"' ## LOINC --> Do not convert to datetime
    sort_data[category].append(x)

with ExcelWriter('REDCap_EPIC_Datapull_' + datetime.strftime(date.today(), '%y-%m-%d') + '.xlsx') as writer:
    for category, data in sort_data.items():
        file_data = pd.DataFrame(data, columns = None, index = None)
        file_data.to_excel(writer, sheet_name = category, index = None, columns = None, header = False)

    # csv_file_name = category + '.csv'
    # csv_file_names.append(csv_file_name)
    # with open(csv_file_name, 'w') as file:
    #     writer = csv.writer(file)
    #     writer.writerows(data)


# with ExcelWriter('path_to_file.xlsx') as writer:
#     for csv_file_name in csv_file_names:
#     for category, data in sort_data.items():
#
#         file_data = pd.read_csv(csv_file_name)
#         file_data.to_excel(writer, sheet_name = csv_file_name[:-4], index = None, header = True)
