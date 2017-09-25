#!/bin/bash
##Path to pcap files.
FILES = /Users/lhl/GoogleDrive/02_hualiang/UAV_Classifier/*
##gets all files that are in the Folder
for f in $FILES
do
  ##Takes the old file name and removes the last 4 chars.
  ##Then adds "json" to the end of the string.
  chmod 755 $f
  OUT=$(echo $f| rev | cut -c 5- | rev | echo "$(cat -)json")
  ##Converts a pcap file to a json file and outputs the json file
  ##where the pcap file is.
  tshark -T json -r $f > $OUT
  echo "Created: $OUT"
done