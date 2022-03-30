#!/bin/bash

usage() { echo "Usage: $0 [-d <string>] [-s <int>] [-t <string>, for example '2 days'] [-s <int>] [-p <string>]" 1>&2; exit 1; }

digit='^[0-9]+$'

while getopts "d:h:s:t" arg; do
	case $arg in
		d)
			RSYNC_PATH=$OPTARG
			;;
		t)
			TIME=$OPTARG
			;;
		s)
			SLEEP=$OPTARG
			[[ (SLEEP == "$digit") && (SLEEP -ge 0) ]] || usage
			;;
		h)
			usage
			exit
			;;
		*)
			usage
			;;
	esac
done




echo "Starting monitoring script"

RESULTS_PATH=~"/ramonThesis/scripts/results/"
Unix_time_current=$(date +%s)
Unix_time_start_plus=$(date +%s --date="$TIME")
echo "Timestamp start: " "$Unix_time_current"
echo "Time in $TIME: " "$Unix_time_start_plus"

counter=0
while [[ "$Unix_time_current" -le "$Unix_time_start_plus" ]]
do
	if [ "$counter" -ge 1 ]
	then
		counter=0
		for filename in results/*
		do 
			echo "$filename"
			rsync -z --chmod=ugo=rwX --remove-source-files $RESULTS_PATH/"${filename}" "$RSYNC_PATH" &			 
		done
	fi

	echo "Time now: " "$Unix_time_current"
	
	echo "Gathering Syscalls"
	UPTIME=$(cat /proc/uptime | awk '{print $1}')
	EPOCH=$(date +%s.%3N)
	Date_Hourly=$(date -d @"$EPOCH" +%d-%m-%H_%M_%S)
	
	
	#PERF=top -b | grep -e "perf" | awk '{print $9}'
	perf trace -S -T -o "./results/${Date_Hourly}".log -a -- sleep "$SLEEP"
	echo -e "EPOCH: $EPOCH \nUPTIME:$UPTIME" >> $RESULTS_PATH/"${Date_Hourly}".log &
	Unix_time_current=$(date +%s)
	counter=$((counter+1))
done

echo "cleanup results directory"
for filename in results/*
	do
		echo "$filename"
		rsync -z --chmod=ugo=rwX --remove-source-files $RESULTS_PATH/"${filename}" "$RSYNC_PATH"
	done
echo "exited MonitoringScript"
exit 0

