from email import header
from turtle import color
from numpy import average
import pandas as pd
import os
import matplotlib.pyplot as plt
import csv 
import numpy as np
import itertools
import sys
from optparse import OptionParser

def get_comma_separated_args(option, opt, value, parser):
    setattr(parser.values, option.dest, value.split(','))

pd.set_option('display.float_format', lambda x: '%.30f' % x)
parser = OptionParser()
parser.add_option('-i', '--input', dest = 'input',
                    type = 'string',
                    action = 'callback',
                    callback = get_comma_separated_args,
                    help = 'specify input directory/directories from to calculate standard deviation/variance')
(options, args) = parser.parse_args()
if(options.input == None):
    print(parser.usage)
    exit(0)
else:
    dir = options.input
print(dir)

# create nested list to save values temporarly
d = [[],[]]

# dir = ["C:/Users/RamonSolodezaldivar/Documents/test1/tt/", "C:/Users/RamonSolodezaldivar/Documents/test1/tick/"]
count = 1
round = 1
df1 = pd.DataFrame()
df2 = pd.DataFrame()

for dir in dir:
    for subdir, dirs, files in os.walk(dir):
        for filename in files:
            file = (os.path.join(subdir,filename))
            print(file)
            df = pd.read_csv(file, sep="\t", names=["ABS TIME  ", "Process Name", "PID ", "System_Call"])
            df['System_Call'] = df['System_Call'].str.replace('*', '')

            val_count = df.System_Call.str.split(expand=True).stack().value_counts(normalize=True).sort_index()

            if(count > len(d)-1):
                d.append(['NaN']*len(d[0]))
            
            for key in val_count.keys():
                if key not in d[0] and count==1:
                    d[0].append(key)
                    index = len(d[0]) - 2
                    d[1].append(val_count[key])

                elif key not in d[0] and count!=1:
                    d[0].append(key)
                    for i in range(1,len(d)-1):
                        d[i].append('NaN')
                    d[count].append(val_count[key])

                elif key in d[0]:
                    index = d[0].index(key)
                    if index > len(d[count])-1:
                        d[count].append(val_count[key])
                    elif d[count][index] == 'NaN':
                        d[count][index] = val_count[key]

            count+=1
        df = pd.DataFrame(d, columns=[d[0]])
        if round == 1:
            df1 = pd.concat([df1, df.iloc[1: , :]])
            df1.drop('nanosleep', inplace=True,axis=1)

        elif round == 2:
            df2 = pd.concat([df1, df.iloc[1: , :]])
            df2.drop('nanosleep', inplace=True,axis=1)

    round+=1
# print(df1)
# df1.to_csv('df1.csv')
# df2.to_csv('df2.csv')

var1 = df1.std()
var2 = df2.std()
# xaxis = first_list + list(set(second_list) - set(first_list))
dd = pd.DataFrame({'normal': var1, 'thetick': var2})
print(dd)
xaxis = [dd.keys]
ax = dd.head().plot.bar(color=['darkgray','gray'], rot=0, title="Normal vs tick")
ax.set_xlabel("Syscalls")
ax.set_ylabel("Standard Deviation")
plt.xticks(fontsize=5)

plt.yscale("log")
plt.tight_layout()
# plt.xticks(xaxis)
plt.show()
# ax.xaxis.set_major_formatter(plt.FixedFormatter(times`))





# ax = var1.plot(x='syscall', y='Variance', kind='bar')
# var2.plot(ax=ax, )
# plt.show()
# plt.savefig('normal/normal.png')

            
