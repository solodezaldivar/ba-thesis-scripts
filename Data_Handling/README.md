# Data Handling Scripts

## Data Cleaning
This script handles the process of cleaning the raw system call data. It takes as inputs the directory which contains the raw system call files and the target output directory to which to save the cleaned files.
##### `-i | --input <string>          Specify directory from which to take the raw data`
##### `-d | --destination <string>    Specify destination directory where cleaned files will be saved`
## Frequency (WIP)
This script calculates the `value count` and its `standard deviation` from the cleaned system call data. It takes as input the directories from which to take the data.
For example `-i C:/Users/{changeMe}/.../normalBehaviourSyscalls`. Multiple directories can also be passed, they have to be comma separated.
## Ngram (WIP)
Ngram.py generates `n-grams` and their respective `frequency` and standard deviation with n =[2,4,6]
