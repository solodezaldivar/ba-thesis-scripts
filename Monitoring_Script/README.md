# Monitoring Script

This script runs on a device and exports the gathered data via rsync to a user specified remote server. In order to use this script and the rsync functionality you need to establish a passwordless SSH connection between the two devices. [Follow this manual](https://medium.com/@ramon.solodezaldivar/how-to-establish-a-passwordless-ssh-s-connection-between-windows-and-linux-c75a948513b2).

To run the script you need to set multiple flags.
##### `-d` the string establishing the path on the remote server where the rsync command will send the gathered data. This is needed to start the script
##### `-i` the directory in which the results will be temporarly stored on the target device. This argument is needed to start the script
##### `-t` time for which the script will run. Can be specified in seconds/days/weeks. For example: `-t 3 days` | Default is 2 days
##### `-s` monitoring interval in seconds. Each interval will create a .txt file with the gathered system calls | Default is 10s
##### `-c` set the max number of iterations before the data is sent to the server
