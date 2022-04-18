from email import header
import pandas as pd
import os
import matplotlib.pyplot as plt
import csv 
import numpy as np
import itertools
import sys
from nltk import ngrams
from optparse import OptionParser
import datetime
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)

################################################################
###################          Setup           ###################
################################################################
def get_comma_separated_args(option, opt, value, parser):
    setattr(parser.values, option.dest, value.split(','))

pd.set_option('display.float_format', lambda x: '%.30f' % x)
parser = OptionParser()
parser.add_option('-i', '--input', dest = 'input',
                    type = 'string',
                    action = 'callback',
                    callback = get_comma_separated_args,
                    help = 'specify input directory/directories from to calculate standard deviation/variance')
parser.add_option('-n', '--ngram', dest = 'n',
                    type = 'int',
                    help = 'specify n-gram length')
(options, args) = parser.parse_args()
if(options.input == None):
    print(parser.usage)
    exit(0)
else:
    dirs = options.input

if(options.n == None):
    print(parser.usage)
    exit(0)
else:
    n = options.n

print("Starting {} gram processing.".format(n))

index = []
count = 1
round = 1
df1 = pd.DataFrame()
df2 = pd.DataFrame()
df_hourWise = pd.DataFrame()
################################################################
#################          Main Loop           #################
################################################################
for dir in dirs:
    behavior = dir.split("/")[-2]
    subdirs = [x[0] for x in os.walk(dir)]
    print(subdirs)
    # iterate through subdirs[1:] to avoid directory self reference
    for subdir in subdirs[1:]:
        print("Subdir:",subdir)
        hour = subdir.split("/")[-1]
        d = [[],[]] 
        print(subdirs)
        for files in os.walk(subdir):
            for filename in files[2]:
                file = os.path.join(subdir,filename)
                file = file.replace("\\\\", "\\")
                try:
                    print("Current file {}\n Time: {}".format(file, datetime.datetime.now()))
                    df = pd.read_csv(file, sep="\t", names=["ABS TIME", "Process Name", "PID", "System_Call"])
                    df.columns = df.columns.str.replace('\s+', '_')
                    
                    # remove rsync, perf and monitoringScri 
                    df = df[df['Process_Name'].str.contains("rsync")==False]
                    df = df[df['Process_Name'].str.contains("perf")==False]
                    df = df[df['Process_Name'].str.contains("monitoringScri")==False]

                    df['System_Call'] = df['System_Call'].str.replace('*', '')

                    words = (df.System_Call.str.split().explode())
                    n_gram = ngrams(words, n)
                    n_gram_df = pd.DataFrame(n_gram)
                    val_count = n_gram_df.value_counts(normalize=True)
                    if(count > len(d)-1):
                        d.append(['NaN']*len(d[0]))
                    print("Count: {}, len(d): {}".format(count,len(d)))
                    
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
                            i = d[0].index(key)
                            if i > len(d[count])-1:
                                d[count].append(val_count[key])
                            elif d[count][i] == 'NaN':
                                d[count][i] = val_count[key]
                    count+=1
                except FileNotFoundError as err:
                    print(err)
                except Exception as err:
                    print(err)
            df = pd.DataFrame(d[1:], columns=d[0])
            mean = df.mean()
            mean.name = '{}'.format(hour)
            df_hourWise = pd.concat([df_hourWise, mean], axis=1)
            count = 1

        
################################################################
################               Mean             ################
################################################################
    mean = df_hourWise.mean(axis=1)
    mean.name = '{}'.format(behavior)
    if round == 1:
        df1 = pd.DataFrame(mean)
    else:
        df1 = pd.concat([df1, mean], axis=1)

################################################################
###########            Standard Deviation            ###########
################################################################
    std = df_hourWise.std(axis=1)
    std.name = '{}'.format(behavior)
    if round == 1:
        df2 = pd.DataFrame(std)
    else:
        df2 = pd.concat([df2, std], axis=1)
    round+=1


################################################################
#################            Output            #################
################################################################
#These names are place holders, change as you see fit.
df1.to_csv('ngram_freq.csv') 
df2.to_csv('ngram_std_dev.csv')
