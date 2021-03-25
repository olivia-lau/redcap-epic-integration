#!/usr/bin/env python3

import csv
import re
import pandas as pd
from pandas import ExcelWriter
from datetime import date
from datetime import datetime

csv_path = '/Users/olivia/Downloads/meds.csv'

all_data = {
    'data_all_other_meds' : [],
    'data_all_date_found' : [],
    'data_all_no_date' : []}

with open(csv_path, 'r') as file:
    data = csv.reader(file)
    for row_index, row in enumerate(data):
        if 'Oth_' in row[1]:
            all_data['data_all_other_meds'].append(row)
        elif len(re.findall('\d{2,4}-\d{2}-\d{2}', row[2])) > 0 or len(re.findall('\d{2,4}/\d{2}/\d{2,4}', row[2])) > 0 or len(re.findall('20\d{2}', row[2])) > 0:
            all_data['data_all_date_found'].append(row)
        else:
            all_data['data_all_no_date'].append(row)
            # len(re.findall('mg', row[2])) == 0:
            # print(row[2])
        # print(row[0].strip())


#
# for x in all_data['data_all_other_meds']:
#     print(x)



data_date_processed = {
    'date_to_date_list' : [],
    'date_single_list' : [],
    'date_date_list' : [],
    'date_to_dc_list' : [],
    'multidate_list' : [],
    'no_date_other' : []}

# all_data['data_all_other_meds'] = []
# all_data['data_all_date_found'] = []
# all_data['data_all_no_date'] = []
# all_data['data_all_other_meds'] = []
# data_date_processed['date_single_list'] = []
# data_date_processed['date_date_list'] = []
# data_date_processed['date_to_dc_list'] = []
# data_date_processed['multidate_list'] = []
# data_date_processed['no_date_other'] = []



date_to_date_pattern = '\d{2,4}\s*-\d{1,2}-\d{1,2}\s*to\s*\d{2,4}\s*-\d{1,2}-\d{1,2}'
date_date_pattern = '\d{2,4}\s*-\d{1,2}-\d{1,2}\s*-\s*\d{2,4}\s*-\d{1,2}-\d{1,2}'
date_to_dc_pattern = '\d{2,4}\s*-\d{2}-\d{2}\s*to\st*o*\s*\w/*\w*'
date_pattern = '\d{2,4}\s*-\d{1,2}-\d{1,2}'



index_to_pop = []

for index, x in enumerate(all_data['data_all_date_found']):
    if re.search(date_to_date_pattern, x[2]) is not None and len(re.findall(date_pattern, x[2])) <= 2:
        pass
    elif re.search(date_date_pattern, x[2]) is not None and len(re.findall(date_pattern, x[2])) <= 2:
        pass
    elif len(re.findall(date_pattern, x[2])) > 1:
        max_split = len(x[2].split(';'))
        h = 0
        for m in x[2].split(';'):
            if re.search(date_pattern, m) is None:
                h += 1
        if h == 0 and len(x[2].split(';')) > 1:
            split_x = x[2].split(';')
            proceed = 0
            for m in split_x:
                if len(re.findall(date_pattern,m)) > 2:
                    proceed += 1
            # print(len(x[2].split(';')))
            # print(index)
            if proceed == 0:
                index_to_pop.append(index)


for n in index_to_pop:
    amend_meds = all_data['data_all_date_found'][n]
    for y in amend_meds[2].split(';'):
        new_list_add = [amend_meds[0], amend_meds[1], y]
        # print(new_list_add)
        all_data['data_all_date_found'].append(new_list_add)
    all_data['data_all_date_found'].pop(n)

for x in all_data['data_all_date_found']:
    if re.search(date_to_date_pattern, x[2]) is not None and len(re.findall(date_pattern, x[2])) <= 2:
        # print(re.findall(date_pattern, x[2]))
        # print(re.search(date_to_date_pattern, x[2]))
        before_date_index = re.search(date_to_date_pattern, x[2]).span()[0]
        after_date_index = re.search(date_to_date_pattern, x[2]).span()[1]
        date_to_date = re.search(date_to_date_pattern, x[2]).group(0)
        dose = (x[2][:before_date_index] + ' ' + x[2][after_date_index:]).strip().replace('   ', '').replace('  ', '')
        formatted_date_dose = (x[0], x[1], date_to_date, dose.strip())
        data_date_processed['date_to_date_list'].append(formatted_date_dose)
        # print(formatted_date_dose)
    elif re.search(date_date_pattern, x[2]) is not None and len(re.findall(date_pattern, x[2])) <= 2:
        # print(re.findall(date_pattern, x[2]))
        before_date_index_1 = re.search(date_date_pattern, x[2]).span()[0]
        after_date_index_1 = re.search(date_date_pattern, x[2]).span()[1]
        dose = (x[2][:before_date_index_1] + ' ' + x[2][after_date_index_1:]).strip().replace('   ', '').replace('  ', '')
        date_date = re.search(date_date_pattern, x[2]).group(0)
        formatted_date_dose = (x[0], x[1], date_date, dose.strip())
        # print(formatted_date_dose)
        data_date_processed['date_date_list'].append(formatted_date_dose)
    elif len(re.findall(date_pattern, x[2])) > 1: ### multiple dates
        # print(re.findall('\d{2,4}-\d{2}-\d{2}', x[2]))
        # print(re.sub(date_pattern + ',*','', x[2]))
        # print(x[2])
        # print('-------------')
        # for n in re.findall(date_pattern, x[2]):
        #     print(n)
        data_date_processed['multidate_list'].append(x)
    elif re.search(date_to_dc_pattern, x[2]) is not None:
        # print(x)
        before_date_index_2 = re.search(date_to_dc_pattern, x[2]).span()[0]
        after_date_index_2 = re.search(date_to_dc_pattern, x[2]).span()[1]
        date_to_dc = re.search(date_to_dc_pattern, x[2]).group(0)
        # print(date_to_dc)
        dose = (x[2][:before_date_index_2] + ' ' + x[2][after_date_index_2:]).strip().replace('   ', '').replace('  ', '')
        # print(dose)
        # print(x[2])
        # print('---------------------')
        formatted_date_dose = (x[0], x[1], date_to_dc, dose.strip())
        data_date_processed['date_to_dc_list'].append(formatted_date_dose)
        # print(formatted_date_dose)
    elif len(re.findall(date_pattern, x[2])) == 1:
        date_single = ''
        if len(re.search(date_pattern, x[2]).group(0)) < 10:
            date_single += '20' + re.search(date_pattern, x[2]).group(0)
        else:
            date_single += re.search(date_pattern, x[2]).group(0)
        before_date_index_3 = re.search(date_pattern, x[2]).span()[0]
        after_date_index_3 = re.search(date_pattern, x[2]).span()[1]
        dose = x[2][:before_date_index_3] + ' ' + x[2][after_date_index_3:].strip().replace('   ', '').replace('  ', '')
        formatted_date_dose = (x[0], x[1], date_single, dose.strip())
        data_date_processed['date_single_list'].append(formatted_date_dose)
        # print(formatted_date_dose)
    else:
        data_date_processed['no_date_other'].append(x)
        # print(x)


# for x in data_date_processed['date_date_list']:
#     print(x)
#
# print('--------------')
#
# for x in data_date_processed['date_single_list']:
#     print(x)
#
# print('--------------')
#
# for x in all_data['data_all_other_meds']:
#     print(x)
#
# print('--------------')
#
# for x in data_date_processed['date_to_dc_list']:
#     print(x)


with ExcelWriter('Meds_' + datetime.strftime(date.today(), '%y-%m-%d') + '.xlsx') as writer:
    for data_type, list in data_date_processed.items():
        df = pd.DataFrame(data_date_processed[data_type], columns = None) #['ID', 'Meds', 'Date', 'Dose']
        # print(df)
        df.to_excel(writer, sheet_name = data_type, index = None, columns = None, header = False)
    for data_type, list in all_data.items():
        if data_type != 'data_all_date_found':
            df = pd.DataFrame(all_data[data_type], columns = None) #['ID', 'Meds', 'Date', 'Dose']
            df.to_excel(writer, sheet_name = data_type, index = None, columns = None, header = False)
        #
        # print(df)


# print(len(data_date_processed['multidate_list']))
#     if len(x[2].split(';')) > 1:
#         print(x[2].split(';'))
# data_date_processed['date_single_list'] = []
# data_date_processed['date_date_list'] = []
# data_date_processed['date_to_dc_list'] = []
# data_date_processed['multidate_list'] = []
# data_date_processed['no_date_other']
