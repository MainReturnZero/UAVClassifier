This repo is for UAV classification project conducted in UH Manoa EE department.
We try to identify drone model by looking into its wireless network data.
At current stage, we assume the data is captured by wireshark. However, we should be able
to eliminate this third party tool by using TCPDump and build our own network packet parsing tool.

HOW TO CAPTURE in CLI:

    usage: capture.py [-h] [--monitor] [--file <output file for captured data>]
                  [--packet_count <packet upper limit for capturing>]
                  [--other [<other> [<other> ...]]]
                  
HOW TO USE:

    usage: observer.py [-h] --input <input json captured data>

                        --observer <y axis value type>

                        [--plot <plot name>]

When export data from wireshark, export it as json format:

    File -> Export Packet Dissections -> As JSON...

    Then select the packets range

For Developers:

Ideally, the captured data should be stored in /data directory, the output plots should be stored in /plots directory

The most updated source are in 'dev' branch, however, it is not tested and unstable. The safe code is in master branch.


The paper which explains this project can be accessed here: https://drive.google.com/drive/u/2/folders/0BygAqxtj1ASvVTRLSS1EejFfZk0

You have to obtain the google drive access permission by Email yingfei@hawaii.edu

When using this project repo, please cite as:

Drone profiling through wireless fingerprinting
Hualiang Li, Garret Johnson, Maverick Jennings and Yingfei Dong
2017 IEEE 7th Annual International Conference on CYBER Technology in Automation, Control, and Intelligent Systems (CYBER)

A brief documentation about each script file:

bin.py:
    This file contains a bin class. Each bin object is a container for a set of packet with same characteristics. You can define this characteristics by yourself.

capture.py:
    This file is a class that contains different capture options using wireshark. For example, you can define if you want to capture in monitor mode, you can capture with certain MAC address, or you can specify the file name you want to save your captured data to.

constant.py:
    This file collect WiFi standard constant data, for example, the probe request frame is 4.

json_data_parser.py:
    This file is a class of a packet object. This object is a structure of a Wifi packet, it contains: 
            _packet_size
            _time_stamp
            _time_delta
            _type
            _type_subtype
            _mac_time
            _signal
            _channel
            _sa
            _da
            _ssid
            _data
    The class can read in a formatted wifi packets JSON file, and convert it into a list of Packets object. In this way, you can simply call the object instant to get the value you want for each packet.
    If you want to do packet analysis, you are very likely to add function in this file since you can get each field of a WIFI packet directly after reading a JSON file.
    You can run your function by substitute the function name in '__main__'

observer.py:
    This file contains a oberver class. You can think it as a monitor for a specific field of a packet. For example, if you want to monitor the signal strength changing for a sequence of packet, you can define you observor as signal_strength.

plot.py:
    This file is a wrap of pyplot to visualize the data we want to analysis.
    
search_channel.py:
    This file search channel 1-11 to see if there is any potential drone data we want to monitor.
   
system_call.py:
    This file deals with system call. For example, call wireshark to capture a certain set of Wifi packets. If you have system dependent error when running this application, it is very likely that it is caused by the system call. Potentially, if you run it on windows, you want to modify the system calls adapting to the Windows OS.
    