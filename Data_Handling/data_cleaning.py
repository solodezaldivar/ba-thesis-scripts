import sys
import csv
import time
import os
import shutil
from optparse import OptionParser

# pd.set_option('display.float_format', lambda x: '%.30f' % x)
################################################################
###################          Setup           ###################
################################################################
parser = OptionParser()
parser.add_option('-d', '--destination', dest = 'destination',
                    type = 'string',
                    help = 'specify destination directory where cleaned files will be saved')
parser.add_option('-i', '--input', dest = 'input',
                    type = 'string',
                    help = 'specify input directory from which to clean files')
parser.add_option('-t', '--time', dest = 'time',
                    type = 'int',
                    help = 'specify input directory from which to clean files')
(options, args) = parser.parse_args()


if(options.destination == None):
    print(parser.usage)
    exit(0)
else:
    destination_dir = options.destination

if(options.input == None):
    print(parser.usage)
    exit(0)
else:
    input_dir = options.input

if(options.time == None):
    print(parser.usage)
    exit(0)
elif(options.time < int(time.time())):
    print(parser.usage)
    print('-t has to specify unix timestamp in the future')
    exit(0)
else:
    max_time = options.time

epoch, uptime = 0.0, 0.0
counter = int(time.time())
current_time = int(time.time())



################################################################
#################          Main Loop           #################
################################################################
while(current_time <= max_time):
    if (int(time.time()) - counter >= 1):
        counter = int(time.time())
        for filename in os.listdir(input_dir):
            if filename.endswith(".log"):
                print("Running")
                summaryBool = False

                
                file = os.path.join(input_dir, filename)
                with open(file, "r+", newline='') as output:
                    # read epoch and uptime values and assign them to variables
                    for line in open(file, 'r'):
                        if (line.__contains__("EPOCH")):
                            epoch = float(line.split(":")[1])
                        elif (line.__contains__("UPTIME")):
                            uptime = float(line.split(":")[1])
                    csv_writer = csv.writer(output, delimiter='\t',quotechar='',quoting=csv.QUOTE_NONE, escapechar='\\')

                    # separate perf trace summary log onto a different file
                    for line in open(file, 'r+').readlines():
                        if (line.__contains__("Summary of events") and (not line.__contains__("EPOCH") or not line.__contains__("EPOCH")) or summaryBool):
                            summaryBool = True
                            summary = filename.split(".")[0] + "-Summary"
                            summaryFile = os.path.join(input_dir, summary)
                            with open("E:/summary/{}.txt".format(summary), 'a+', newline='') as summaryOutput:
                                csv_summary = csv.writer(summaryOutput, delimiter='\t')
                                csv_summary.writerow([line])
                        
                        
                        ################################################################
                        ################          Data Cleaning           ##############
                        ################################################################
                        elif (not summaryBool):
                            try:
                                    perf_trace_line = line.split(":")
                                    if (perf_trace_line[0].__contains__("0.000")):
                                        continue
                                    else:   
                                        abs_time_temp = perf_trace_line[0].split("(")
                                        abs_time = epoch - uptime + float(abs_time_temp[0])/1000

                                    process_name_and_pid = perf_trace_line[1].split("/")
                                    process_name = process_name_and_pid[0]

                                    if (process_name_and_pid[1].__contains__("...")):
                                        pid_temp = process_name_and_pid[1].split("...")
                                        pid = pid_temp[0]
                                        syscall_temp = perf_trace_line[2].split("(")
                                        syscall = syscall_temp[0]+"*"
                                    else:
                                        pid_and_syscall = process_name_and_pid[1].split(" ")
                                        pid = pid_and_syscall[0]
                                        syscall_temp = pid_and_syscall[1].split("(")
                                        syscall = syscall_temp[0]
                                    csv_writer.writerow([abs_time, process_name, pid, syscall])
                            except (IndexError, ValueError) as e:
                                continue
                    output.truncate() #shrink cleaned file size 
                    output.close()
                    
                    ################################################################
                    ###############          Data Outputting           #############
                    ################################################################
                    DIR = destination_dir+filename.split("_")[0]
                    if not os.path.isdir(DIR):
                        os.makedirs(DIR)
                        print("created folder : ", DIR)
                    else:
                        print(DIR, "folder already exists")
                    os.replace(file, DIR+'/'+filename)
        current_time = int(time.time())