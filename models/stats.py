#
# Copyright 2023 Simplii from Group74 NCSU CSC510
#
# Licensed under the MIT/X11 License (http://opensource.org/licenses/MIT)
#

import pymongo
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

client = pymongo.MongoClient('mongodb://localhost:27017')
db = client["simplii"]
p_details = db["tasks"]  # profile details
records = p_details.find()
list_record = list(records)

df_tasks = pd.DataFrame(list_record)
# print(df_tasks)

intx = df_tasks.loc[df_tasks['category'] == 'Intellectual']
int_count = intx.shape[0]
phy = df_tasks.loc[df_tasks['category'] == 'physical']
phy_count = phy.shape[0]

done = df_tasks.loc[df_tasks['status'] == 'Done']
done_count = done.shape[0]
in_prog = df_tasks.loc[df_tasks['status'] == 'In Progress']
in_prog_count = in_prog.shape[0]
blocked = df_tasks.loc[df_tasks['status'] == 'Blocked']
blocked_count = blocked.shape[0]

# unique email list
email = list(set(df_tasks['email'].tolist()))

'''
y = np.array([done_count, in_prog_count, blocked_count])
mylabels = ["Done", "In Progress", "Blocked"]
#all tasks
plt.pie(y, labels = mylabels, autopct='%1.1f%%')
plt.legend()
plt.title('Summary of all tasks')
plt.show()
'''


def all_tasks(i):
    done_user = df_tasks.loc[(df_tasks['status'] == 'Done')
                             & (df_tasks['email'] == i)]
    dc = done_user.shape[0]
    inprog_user = df_tasks.loc[(
        df_tasks['status'] == 'In Progress') & (df_tasks['email'] == i)]
    ipc = inprog_user.shape[0]
    blocked_user = df_tasks.loc[(
        df_tasks['status'] == 'Blocked') & (df_tasks['email'] == i)]
    bc = blocked_user.shape[0]

    y = np.array([dc, ipc, bc])
    mylabels = ["Done", "In Progress", "Blocked"]

    plt.pie(y, labels=mylabels, autopct='%1.1f%%')
    plt.legend()
    plt.title('Status of all tasks:')
    plt.show()


def int_tasks(i):
    di = df_tasks.loc[(df_tasks['status'] == 'Done') & (
        df_tasks['category'] == 'Intellectual') & (df_tasks['email'] == i)]
    dic = di.shape[0]
    ipi = df_tasks.loc[(df_tasks['status'] == 'In Progress') & (
        df_tasks['category'] == 'Intellectual') & (df_tasks['email'] == i)]
    ipic = ipi.shape[0]
    bi = df_tasks.loc[(df_tasks['status'] == 'Blocked') & (
        df_tasks['category'] == 'Intellectual') & (df_tasks['email'] == i)]
    bic = bi.shape[0]

    y = np.array([dic, ipic, bic])
    mylabels = ["Done", "In Progress", "Blocked"]

    plt.pie(y, labels=mylabels, autopct='%1.1f%%')
    plt.legend()
    plt.title('Status of intellectual tasks:')
    plt.show()


def phy_tasks(i):
    di = df_tasks.loc[(df_tasks['status'] == 'Done') & (
        df_tasks['category'] == 'physical') & (df_tasks['email'] == i)]
    dic = di.shape[0]
    ipi = df_tasks.loc[(df_tasks['status'] == 'In Progress') & (
        df_tasks['category'] == 'physical') & (df_tasks['email'] == i)]
    ipic = ipi.shape[0]
    bi = df_tasks.loc[(df_tasks['status'] == 'Blocked') & (
        df_tasks['category'] == 'physical') & (df_tasks['email'] == i)]
    bic = bi.shape[0]

    y = np.array([dic, ipic, bic])
    mylabels = ["Done", "In Progress", "Blocked"]

    plt.pie(y, labels=mylabels, autopct='%1.1f%%')
    plt.legend()
    plt.title('Status of physical tasks:')
    plt.show()


for i in email:
    all_tasks(i)
    int_tasks(i)
    phy_tasks(i)
