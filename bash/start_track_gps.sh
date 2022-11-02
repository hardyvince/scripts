#!/bin/bash
                                                          
gpx=`date +gpx%Y-%m-%dT%H%M%SZ`
fifofile=fifofile                                         
if [[ -f $fifofile ]]; then
       exit                                               
fi
if ! [[ -p $fifofile ]]; then
       echo "creating $fifofile"
       mkfifo $fifofile
fi
trap "rm $fifofile " EXIT

while true                                                
do
       {                                                  
               loc=`termux-location`;
	       if [[ -p $fifofile ]]; then
		       echo -n $loc > $fifofile;
	       fi
       }&
       #echo -n > $fifofile&                              
       sleep 10
done&
pid=$!
echo $pid

while true
do
        #loc=`termux-location -r updates`
        #echo $loc
	time=`date +%Y-%m-%dT%H:%M:%SZ`
        read line < fifofile
        echo "line: $line"
        if [[ "$line" == "stop" ]]; then
		rclone copy "$gpx.gpx" "hvgd:/sync/runs/"
                break
        fi


	lat=`echo -n $line | grep -o -E "latitude\":[[:space:]]+[^[:space:],]+" | grep -o -E "[[:digit:]]+[^[:space:]]+"`
	echo $lat

	lon=`echo -n $line | grep -o -E "longitude\":[[:space:]]+[^[:space:],]+" | grep -o -E "[[:digit:]]+[^[:space:]]+"`
	echo $lon

	alt=`echo -n $line | grep -o -E "altitude\":[[:space:]]+[^[:space:],]+" | grep -o -E "[[:digit:]]+[^[:space:]]+"`
	echo $alt


	echo \<trkpt lat=\"$lat\" lon=\"$lon\"\> >> $gpx.gpx
	echo -e "\t<ele>$alt</ele>" >> $gpx.gpx
	echo -e "\t<time>$time</time>" >> $gpx.gpx
	echo \</trkpt\> >> $gpx.gpx


        #date +%Y-%m-%dT%H:%M:%SZ
done                                                                                                                  
kill $pid 2>/dev/null
