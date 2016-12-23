# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 10:38:18 2016

@author: Jeremy
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import os
import pickle
all_the_data = []

save_dir = '/media/jeremy/San/Data'
filename = 'nyt_data.pkl'

if not os.path.exists(save_dir):
    os.makedirs(save_dir)

saved = os.path.join(save_dir,filename)

if os.path.exists(saved):
    fin = open(saved,'r+b')
    all_the_data = pickle.load(fin)
else:
    fout = open(saved,'w+b')
    for i in range(0,32):
        all_the_data.append(
                pd.read_csv(
                    'http://stat.columbia.edu/~rachel/datasets/nyt{}.csv'.format(i)
                )
        )
    pickle.dump(all_the_data,fout)

all_the_data = all_the_data[1:]

print(all_the_data[0])
for i in range(len(all_the_data)):
    all_the_data[i] = all_the_data[i][all_the_data[i]['Signed_In']==True]
    all_the_data[i].drop(['Signed_In'],axis = 1)

print(all_the_data[0].columns)
print('The age is zero: {} out of {}'.format(
    sum(all_the_data[0]['Age']==0),
    len(all_the_data[0])
    )
)


n_logins = np.array([d.shape[0] for d in all_the_data])

avg_impressions = [d['Impressions'].mean() for d in all_the_data]
plt.figure()

plt.subplot2grid((2,1),(0,0))
plt.plot(n_logins)
plt.subplot2grid((2,1),(1,0))
plt.plot(avg_impressions)

data1 = all_the_data[1]

plt.figure()
plt.hist(data1['Impressions'])
plt.xlabel('Impressions [by bin]')
plt.ylabel('Count')

plt.figure()
plt.hist(data1['Age'])
plt.xlabel('Age [by bin]')
plt.ylabel('Count')

plt.figure()
data1['Age'].value_counts().plot(kind = 'bar')
plt.title('Exact Histogram')

is_male = data1['Gender'] == 1

male_impression_count = data1[is_male]['Impressions'].value_counts()
total_impression_count = data1['Impressions'].value_counts()

plt.figure()
(male_impression_count/total_impression_count)[total_impression_count >10].plot(kind = 'bar')
plt.title('Percentage of male contributions')


plt.show()

def age_group(age):
    if age < 18: return '<18'
    if age < 24: return '18-24'
    if age < 34: return '25-34'
    if age < 44: return '35-44'
    if age < 54: return '45-54'
    if age < 64: return '55-64'
    return '65+'

data1['age_group'] = data1['Age'].apply(age_group)

grouping_by_age = data1[data1['Age'] > 0].groupby('age_group')


impressions_by_age = grouping_by_age['Impressions'].aggregate(sum)
users_by_age = data1['age_group'].value_counts()

impressions_per_user = impressions_by_age/users_by_age
print(impressions_per_user)
