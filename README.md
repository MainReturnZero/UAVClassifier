This repo is for UAV classification project conducted in UH Manoa EE department.
We try to identify drone model by looking into its wireless network data.
At current stage, we assume the data is captured by wireshark. However, we should be able
to eliminate this third party tool by using TCPDump and build our own network packet parsing tool.

HOW TO USE:
usage: observer.py [-h] --input input json captured data

Ideally, the captured data should be stored in /data directory, the output plots should be stored in /plots directory
When export data from wireshark, export it as json format:
    File -> Export Packet Dissections -> As JSON...
    Then select the packets range 

The paper can be accessed here: https://drive.google.com/drive/u/2/folders/0BygAqxtj1ASvVTRLSS1EejFfZk0
You have to obtain the google drive access permission by Email yingfei@hawaii.edu

When using this project repo, please cite as:
Drone profiling through wireless fingerprinting
Hualiang Li, Garret Johnson, Maverick Jennings and Yingfei Dong
2017 IEEE 7th Annual International Conference on CYBER Technology in Automation, Control, and Intelligent Systems (CYBER)
