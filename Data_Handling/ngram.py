from email import header
from locale import normalize
from turtle import color
from numpy import average
import pandas as pd
import os
import matplotlib.pyplot as plt
import csv 
import numpy as np
import itertools
import sys
from nltk import ngrams

pd.set_option('display.float_format', lambda x: '%.30f' % x)
dir = ["C:/Users/RamonSolodezaldivar/Documents/test1/tt/", "C:/Users/RamonSolodezaldivar/Documents/test1/tick/"]

for file in dir:
    df = pd.read_csv("C:/Users/RamonSolodezaldivar/Documents/test1/tt/14-03-21_50_55.log", sep="\t", names=["ABS TIME  ", "Process Name", "PID ", "System_Call"])
    df['System_Call'] = df['System_Call'].str.replace('*', '')
    words = (df.System_Call.str.split().explode())
    n = 2
    sixgrams = ngrams(words, n)
    l = pd.DataFrame(sixgrams)
    val_count = l.value_counts(normalize=True)
            # val_count = df.System_Call.str.split(expand=True).stack().value_counts(normalize=True).sort_index()
    # for sixgram in sixgrams:
        # print(sixgram)
    print(l)
    print(val_count)
    val_count.to_csv('2gramclean.csv')
