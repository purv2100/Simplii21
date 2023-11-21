#
# Copyright 2023 Simplii from Group74 NCSU CSC510
#
# Licensed under the MIT/X11 License (http://opensource.org/licenses/MIT)
#

import pymongo
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
import os
import sys
from datetime import date

client = pymongo.MongoClient('mongodb://localhost:27017')
db = client["simplii"]
p_details = db["tasks"]  # profile details
records = p_details.find()
list_record = list(records)

df = pd.DataFrame(list_record)

start = df['startdate'].tolist()
due = df['duedate'].tolist()
email = df['email'].tolist()

format = '%Y-%m-%d'

st, dt = [], []
for i in start:
    st.append(datetime.datetime.strptime(i, format).date())

for i in due:
    dt.append(datetime.datetime.strptime(i, format).date())

in_prog = df.loc[df['status'] == 'In Progress']
in_prog = in_prog.drop(['_id', 'status'], axis=1)

blocked = df.loc[df['status'] == 'Blocked']
blocked = blocked.drop(['_id', 'status'], axis=1)

sip, dip, sb, db = [], [], [], []
start1 = in_prog['startdate'].tolist()
due1 = in_prog['duedate'].tolist()

start2 = blocked['startdate'].tolist()
due2 = blocked['duedate'].tolist()

for i in start1:
    sip.append(datetime.datetime.strptime(i, format).date())

for i in start2:
    sb.append(datetime.datetime.strptime(i, format).date())

for i in due1:
    dip.append(datetime.datetime.strptime(i, format).date())

for i in due2:
    db.append(datetime.datetime.strptime(i, format).date())

in_prog['startdate'] = pd.to_datetime(in_prog['startdate'])
in_prog['duedate'] = pd.to_datetime(in_prog['duedate'])

blocked['startdate'] = pd.to_datetime(blocked['startdate'])
blocked['duedate'] = pd.to_datetime(blocked['duedate'])

df1 = in_prog.loc[(in_prog['startdate'] <= pd.to_datetime('today').floor('D')) & (
    in_prog['duedate'] >= pd.to_datetime('today').floor('D')) & (in_prog['email'] == email[0])]
df2 = blocked.loc[(blocked['duedate'] >= pd.to_datetime(
    'today').floor('D')) & (blocked['email'] == email[0])]

# print(df1)
# print(df2)

#df1 = df1.loc[df1['email'] == email[0]]
#df2 = df2.loc[df2['email'] == email[0]]

df1 = df1.drop(['email'], axis=1)
df2 = df2.drop(['email'], axis=1)


# (blocked['startdate'] <= pd.to_datetime('today').floor('D')) &

# RECOMMENDATIONS IN TXT FILE
with open(os.path.join(sys.path[0], "task_recommendation.txt"), 'wt') as f:
    x = df1.to_csv(sep='\t', index=False, header=True)
    y = df2.to_csv(sep='\t', index=False, header=True)

    f.write("Here's your task recommendation on tasks you're working...\n\n")
    f.write(x)
    f.write("\n\n")
    f.write("Here are some task recommnedation so you don't miss the deadlines...\n\n")
    f.write(y)

# RECOMMENDATIONS IN CSV FILE
with open(os.path.join(sys.path[0], "task_recommendation.csv"), 'wt') as f:
    x = df1.to_csv(index=False, header=True)
    y = df2.to_csv(index=False, header=False)

    #f.write("Here's your task recommendation on tasks you're working...\n\n")
    f.write(x)
    # f.write("\n\n")
    #f.write("Here are some task recommnedation so you don't miss the deadlines...\n\n")
    f.write(y)
