#!/bin/bash

#Checks to see if mitmdump is already running
#If so, kills the processes
PROCESS=$(ps aux | grep mitmdump | tr -s " " | cut -d " " -f 2,11)
echo "$PROCESS" | while read -r i
do
    PSNAME=$(echo "$i" | cut -d " " -f 2)

    if [[ "$PSNAME" == *"./mitmdump"* ]]
    then
        PSNUM=$(echo "$i" | cut -d " " -f 1)
        echo "Shutting down process $PSNUM $PSNAME"
	kill -9 $PSNUM
    fi
done

echo "" > stream.txt
echo "" > capture.txt

#Starts mitmdump and outputs to stream.txt
~/mitm/mitmdump --set block_global=false --set flow_detail=3 --verbose -s mitmdecode.py > stream.txt  2>/dev/null &

#Every 5 seconds, put stream into capture
#Then empty the contents to stream
while [ 0 -lt 1 ]
do
	sleep 10s
	cat stream.txt >> capture.txt
	tr < capture.txt -d '\000' > capturefixed.txt
	cat capturefixed.txt >> backup.txt
	echo "" > stream.txt
	python3 ./AnalysisMain.py
	echo "" > capture.txt
done
