# Data Handling Scripts

## Data Cleaning
This script handles the process of cleaning the raw system call data. It takes as inputs the directory which contains the raw system call files and the target output directory to which to save the cleaned files.
##### `-i | --input <string>          Specify directory from which to take the raw data`
##### `-d | --destination <string>    Specify destination directory where cleaned files will be saved`
##### `-t | --time <int>              Specify for how long the script should run in Unix Timestamp`
## Frequency
This script calculates the normalized `frequency` and its `standard deviation` from the cleaned system call data. It takes as input the directories from which to take the data.
For example `-i C:/Users/{changeMe}/.../normalBehaviourSyscalls`. Multiple directories can also be passed, they have to be comma separated.
## Ngram
Ngram.py temporarly generates `n-grams` and calculates their respective normalized `frequency` and `standard deviation`. 
##### `-i | --input <string>          Specify directory from which to take the data`
##### `-n | --ngram <positive int>    Specify the length of n-grams.`
