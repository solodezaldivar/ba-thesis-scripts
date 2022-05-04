#!/bin/bash

################################################################
###################          Setup           ###################
################################################################
usage() { echo "Usage: $0 [-d destination directory <string>] [-i results directory <string>] [-s <int> in seconds] [-t <string>, for example '2 days']" exit 0; }

digit='^[0-9]+$'

while getopts "d:h:p:i:s:t" arg; do
	case $arg in
		d)
			RSYNC_PATH=$OPTARG
			;;
		h)
			usage
			exit
			;;
		i)
			RESULTS_PATH=$OPTARG
			;;
		t)
			TIME=$OPTARG
			;;
		s)
			SLEEP=$OPTARG
			[[ ($SLEEP == "$digit") && ($SLEEP -ge 0) ]] || usage
			;;
		*)
			usage
			;;
	esac
done

if [ -z "$TIME" ]
then
TIME="2 days"
fi

if [ -z "$SLEEP" ]
then
SLEEP=10
fi

echo "Starting monitoring script"

Unix_time_current=$(date +%s)
Unix_time_start_plus=$(date +%s --date="$TIME")
echo "Timestamp start: " "$Unix_time_current"
echo "Time in $TIME: " "$Unix_time_start_plus"
counter=0

################################################################
##############          Monitoring Loop           ##############
################################################################
while [[ "$Unix_time_current" -le "$Unix_time_start_plus" ]]


################################################################
###############          Data Transfer           ###############
################################################################
do
	if [ "$counter" -ge 1 ]
	then
		counter=0
		for filename in $RESULTS_PATH/*
		do 
			echo "$filename"
			rsync -z --chmod=ugo=rwX --remove-source-files ${filename} "$RSYNC_PATH" &			 
		done
	fi

################################################################
##########          Data Gathering + Output           ##########
################################################################
	echo "Time now: " "$Unix_time_current"	
	echo "Gathering Syscalls"
	UPTIME=$(cat /proc/uptime | awk '{print $1}')
	EPOCH=$(date +%s.%3N)
	Date_Hourly=$(date -d @"$EPOCH" +%d-%m-%H_%M_%S)
		
	perf trace -S -T -o "./results/${Date_Hourly}".log -a -- sleep "$SLEEP"
	echo -e "EPOCH: $EPOCH \nUPTIME:$UPTIME" >> $RESULTS_PATH/"${Date_Hourly}".log &
	Unix_time_current=$(date +%s)
	counter=$((counter+1))
done
################################################################
###############          Data Transfer           ###############
################################################################
echo "cleanup results directory"
for filename in $RESULTS_PATH/*
	do
		echo "$filename"
		rsync -z --chmod=ugo=rwX --remove-source-files ${filename} "$RSYNC_PATH"
	done
echo "exited MonitoringScript"
exit 0

