#!/usr/bin/env python
'''
For this file, they are all example code that are mostly used to generate plots from json data. It serves as an example, not final code, you have to modify the function to meet your own requirement.
'''
import json
import matplotlib.pyplot as plt
import numpy as np
import math as math
from scipy.interpolate import UnivariateSpline
from scipy.stats import norm

INPUT_FILE = "./data/parrot.json"
INPUT_FILE2 = "./data/parrot_lab.json"
#INPUT_FILE = "./data/encrypted_parrot_partial.json"


def dict_ignore_on_duplicates(ordered_pairs):
    """Reject duplicate keys."""
    d = {}
    for k, v in ordered_pairs:
        if k not in d:
           d[k] = v
    return d


def read_json(input_file):
    with open(input_file) as i:
        return json.load(i, object_pairs_hook=dict_ignore_on_duplicates)


class Packet(object):

    def __init__(self, packet):
        try:
            self._packet_size = int(packet['_source']['layers']['frame']['frame.len'])
            self._time_stamp = float(packet['_source']['layers']['frame']['frame.time_epoch'])
            self._time_delta = float(packet['_source']['layers']['frame']['frame.time_delta'])
            self._type = int(packet['_source']['layers']['frame']['frame.encap_type'])
            self._type_subtype = int(packet['_source']['layers']['wlan']['wlan.fc_tree']['wlan.fc.subtype'])
            self._mac_time = int(packet['_source']['layers']['wlan_radio']['wlan_radio.timestamp'])
            #self._signal = int(packet['_source']['layers']['wlan_radio']['wlan_radio.signal_dbm'])
            self._channel = int(packet['_source']['layers']['wlan_radio']['wlan_radio.channel'])
            #self._sa = packet['_source']['layers']['wlan']['wlan.sa']
            #self._da = packet['_source']['layers']['wlan']['wlan.da']
            self._data = packet['_source']['layers']['data']['data.data']

        except KeyError, e:
            self._packet_size = 0
            self._time_stamp = 0
            self._time_delta = 0
            self._type = 0
            self._type_subtype = -1
            self._mac_time = 0
            self._signal = 0
            self._channel = 0
            self._sa = None
            self._da = None
            self._ssid = None
            self._data = ""
            print "BAD PACKETS:", packet['_source']['layers']['frame']['frame.number']
            print e

        try:
            if packet['_source']['layers']['wlan_mgt'].get('wlan_mgt.tagged.all'):
                self._ssid = packet['_source']['layers']['wlan_mgt']['wlan_mgt.tagged.all']['wlan_mgt.tag']['wlan_mgt.ssid']
            else:
                self._ssid = ""
        except AttributeError:
            self._ssid = ""
        except KeyError:
            self._ssid = ""

    @property
    def packet_size(self):
        return self._packet_size

    @packet_size.setter
    def packet_size(self, packet_size):
        self._packet_size = int(packet_size)

    @property
    def time_stamp(self):
        return float(self._time_stamp)

    @time_stamp.setter
    def time_stamp(self, time_stamp):
        self._time_stamp = time_stamp

    @property
    def time_delta(self):
        return float(self._time_delta)

    @time_delta.setter
    def time_delta(self, time_delta):
        self._time_delta = time_delta

    @property
    def type(self):
        return int(self._type)

    @type.setter
    def type(self, type):
        self._type = type

    @property
    def type_subtype(self):
        return int(self._type_subtype)

    @type_subtype.setter
    def type_subtype(self, type_subtype):
        self._type_subtype = type_subtype

    @property
    def mac_time(self):
        return int(self._mac_time)

    @mac_time.setter
    def mac_time(self, mac_time):
        self._mac_time = mac_time

    @property
    def signal(self):
        return int(self._signal)

    @signal.setter
    def signal(self, signal):
        self._signal = signal

    @property
    def channel(self):
        return int(self._channel)

    @channel.setter
    def channel(self, channel):
        self._channel = channel

    @property
    def sa(self):
        return self._sa

    @sa.setter
    def sa(self, sa):
        self._sa = sa

    @property
    def da(self):
        return self._da

    @da.setter
    def da(self, da):
        self._da = da

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

    @property
    def ssid(self):
        return self._ssid

    @ssid.setter
    def ssid(self, ssid):
        self._ssid = ssid

    def get_addr_hash(self):
        if self.sa:
            return hash(self.sa)


def sizes_histogram():
    data_packets = read_json(INPUT_FILE)
    packets = []
    for data_packet in data_packets:
        packet = Packet(data_packet)
        packets.append(packet)

    sizes = dict()
    for packet in packets:
        if packet.packet_size > 100 and packet.packet_size < 200:
            if sizes.has_key(str(packet.packet_size)):
                sizes[str(packet.packet_size)] += 1
            else:
                sizes[str(packet.packet_size)] = 1
    x = np.arange(len(sizes))
    keylist = sizes.keys()
    keylist.sort()
    heights = []
    keys = []
    for key in keylist:
        keys.append(key)
        heights.append(sizes[key])
    plt.bar(x, height=heights)
    plt.xticks(rotation=330)
    plt.tick_params(labelsize=5)
    plt.xticks(x, keys)
    plt.show()


def pattern_timing():
    data_packets = read_json(INPUT_FILE)
    packets = []
    for data_packet in data_packets:
        packet = Packet(data_packet)
        packets.append(packet)

    firsts = []
    seconds = []
    start_time = 0
    flag = 1
    first_flag = 1
    second_flag = 0
    for packet in packets:
        if flag:
            start_time = packet.mac_time
        if packet.data.startswith('04:7e'):
            if first_flag:
                firsts.append(packet.mac_time)
                first_flag = 0
                second_flag = 1
        if packet.data.startswith('01:fe'):
            if second_flag:
                seconds.append(packet.mac_time)
                first_flag = 1
                second_flag = 0

    times = []
    for i in range(208):
        if seconds[i]-firsts[i] < 1000:
            times.append(seconds[i]-firsts[i])

    N = len(times)
    n = N/10
    print N
    '''
    #times.sort()
    p, x = np.histogram(times, bins=n)
    x = x[:-1] + (x[1] - x[0])/2
    f = UnivariateSpline(x, p, s=n)
    #plt.plot(times, '.')
    plt.plot(x, f(x))
    plt.xlabel('Time Interval')
    plt.show()
    '''
    # Fit a normal distribution to the data:
    mu, std = norm.fit(times)
    median = np.median(times)
    mean = np.mean(times)
    print median, mean

    # Plot the histogram.
    plt.hist(times, bins=n, normed=True, alpha=0.6, color='b')

    # Plot the PDF.
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = norm.pdf(x, mu, std)
    plt.plot(x, p, 'k', linewidth=2)
    title = "Fit results: mu = %.2f,  std = %.2f" % (mu, std)
    plt.title(title)
    plt.ylabel("Density after normalized")
    plt.xlabel("Time interval (ms)")

    plt.show()


def pattern4_timing():
    # Hualiangs-iMac:data lhl$ cat parrot.json | grep -E 'mactime|data.data' > temp

    data_packets = read_json(INPUT_FILE)
    packets = []
    for data_packet in data_packets:
        packet = Packet(data_packet)
        packets.append(packet)

    firsts = []
    seconds = []
    start_time = 0
    flag = 1
    count = 0
    for packet in packets:
        if flag:
            start_time = packet.mac_time
            flag = 0
        if packet.data.startswith('02:7f'):
            count += 1
            if count%4 is 1:
                firsts.append(packet.mac_time)
            if count%4 is 0:
                seconds.append(packet.mac_time)

    print len(firsts), len(seconds)

    times = []
    for i in range(1089):
        if seconds[i]-firsts[i] < 500000:
            times.append(seconds[i]-firsts[i])

    N = len(times)
    n = N/10

    # Fit a normal distribution to the data:
    mu, std = norm.fit(times)
    median = np.median(times)
    mean = np.mean(times)
    print median, mean

    # Plot the histogram.
    plt.hist(times, bins=n, normed=True, alpha=0.6, color='b')

    # Plot the PDF.
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = norm.pdf(x, mu, std)
    # plt.plot(x, p, 'k', linewidth=2)
    title = "Fit results: mu = %.2f,  std = %.2f" % (mu, std)
    plt.title(title)

    plt.show()


def main():
   data_packets = read_json(INPUT_FILE)
   packets = []
   for data_packet in data_packets:
       packet = Packet(data_packet)
       packets.append(packet)

   sizes = set()
   times_127 = []
   times_133 = []
   times_134 = []
   times_137 = []
   count = 0.0
   c = 0.0
   for packet in packets:
       #sizes.add(packet.packet_size)
       if packet.packet_size == 137:
           count += 1
           if packet.time_delta < 0.03:
               times_137.append(packet.time_delta)
           if abs(packet.time_delta -0.05) < 0.01:
               c += 1
       # print packet.packet_size, packet.time_stamp, packet.type
       if packet.packet_size == 127:
           times_127.append(packet.time_delta)
       if packet.packet_size == 133:
           times_133.append(packet.time_delta)
       if packet.packet_size == 134:
           times_134.append(packet.time_delta)
   #print c/count
   if len(times_127) < len(times_133):
       del times_133[len(times_127):]
   else:
       del times_127[len(times_133):]

   if len(times_134) < len(times_137):
       del times_137[len(times_134):]
   else:
       del times_134[len(times_137):]

   times_127.sort()
   times_133.sort()
   times_134.sort()
   times_137.sort()

   fig = plt.figure()
   ax = fig.add_subplot(1,1,1)
   ax1 = fig.add_subplot(2,2,1)
   ax2 = fig.add_subplot(2,2,3)
   ax3 = fig.add_subplot(2,2,2)
   ax4 = fig.add_subplot(2,2,4)
   ax1.plot(times_127, 'r-', label='Parrot Type 1')
   ax1.plot(times_133, 'g-', label='Parrot Type 1')
   ax1.legend(loc='upper left')
   ax2.plot(times_134, 'r-', label='Parrot Type 1')
   ax2.plot(times_137, 'g-', label='Solo Type 1')
   ax2.legend(loc='upper left')

   p1 = [(i, times_127[i]) for i in range(0, len(times_127), 20)]
   q1 = [(i, times_133[i]) for i in range(0, len(times_133), 20)]
   p2 = [(i, times_134[i]) for i in range(0, len(times_134), 20)]
   q2 = [(i, times_137[i]) for i in range(0, len(times_137), 20)]
   m1 = np.mean(times_127+times_133)
   m2 = np.mean(times_134+times_137)

   data_packets = read_json(INPUT_FILE2)
   packets = []
   for data_packet in data_packets:
       packet = Packet(data_packet)
       packets.append(packet)

   sizes = set()
   times_127 = []
   times_133 = []
   times_134 = []
   times_137 = []
   count = 0.0
   c = 0.0
   for packet in packets:
       #sizes.add(packet.packet_size)
       if packet.packet_size == 137:
           count += 1
           times_137.append(packet.time_delta)
           if abs(packet.time_delta -0.05) < 0.01:
               c += 1
       #print packet.packet_size, packet.time_stamp, packet.type
       if packet.packet_size == 127:
           times_127.append(packet.time_delta)
       if packet.packet_size == 133:
           times_133.append(packet.time_delta)
       if packet.packet_size == 134:
           times_134.append(packet.time_delta)
   #print c/count
   if len(times_127) < len(times_133):
       del times_133[len(times_127):]
   else:
       del times_127[len(times_133):]

   if len(times_134) < len(times_137):
       del times_137[len(times_134):]
   else:
       del times_134[len(times_137):]

   times_127.sort()
   times_133.sort()
   times_134.sort()
   times_137.sort()

   ax3.plot(times_127, 'r-', label='Parrot Type 2')
   ax3.plot(times_133, 'g-', label='Parrot Type 2')
   ax3.legend(loc='upper left')
   ax4.plot(times_134, 'r-', label='Parrot Type2')
   ax4.plot(times_137, 'g-', label='Solo Type2')
   ax4.legend(loc='upper left')

   # Turn off axis lines and ticks of the big subplot
   ax.spines['top'].set_color('none')
   ax.spines['bottom'].set_color('none')
   ax.spines['left'].set_color('none')
   ax.spines['right'].set_color('none')
   ax.tick_params(labelcolor='w', top='off', bottom='off', left='off', right='off')

   # Set common labels
   ax.set_xlabel('Packet Index')
   ax.set_ylabel('Time Interval (ms)')

   p3 = [(i, times_127[i]) for i in range(0, len(times_127), 20)]
   q3 = [(i, times_133[i]) for i in range(0, len(times_133), 20)]
   p4 = [(i, times_134[i]) for i in range(0, len(times_134), 20)]
   q4 = [(i, times_137[i]) for i in range(0, len(times_137), 20)]
   m3 = np.mean(times_127+times_133)
   m4 = np.mean(times_134+times_137)
   d1= m1/frechetDist(p1, q1)
   d2= m2/frechetDist(p2, q2)
   d3= m3/frechetDist(p3, q3)
   d4= m4/frechetDist(p4, q4)
   ax1.set_title('Similarity = ' + '{}'.format(d1), fontsize=7)
   ax2.set_xlabel('Similarity = ' + '{}'.format(d2), fontsize=7)
   ax3.set_title('Similarity = ' + '{}'.format(d3), fontsize=7)
   ax4.set_xlabel('Similarity = ' + '{}'.format(d4), fontsize=7)
   plt.show()


# Euclidean distance.
def euc_dist(pt1,pt2):
    return math.sqrt((pt2[0]-pt1[0])*(pt2[0]-pt1[0])+(pt2[1]-pt1[1])*(pt2[1]-pt1[1]))


def _c(ca,i,j,P,Q):
    if ca[i,j] > -1:
        return ca[i,j]
    elif i == 0 and j == 0:
        ca[i,j] = euc_dist(P[0],Q[0])
    elif i > 0 and j == 0:
        ca[i,j] = max(_c(ca,i-1,0,P,Q),euc_dist(P[i],Q[0]))
    elif i == 0 and j > 0:
        ca[i,j] = max(_c(ca,0,j-1,P,Q),euc_dist(P[0],Q[j]))
    elif i > 0 and j > 0:
        ca[i,j] = max(min(_c(ca,i-1,j,P,Q),_c(ca,i-1,j-1,P,Q),_c(ca,i,j-1,P,Q)),euc_dist(P[i],Q[j]))
    else:
        ca[i,j] = float("inf")
    return ca[i,j]

""" Computes the discrete frechet distance between two polygonal lines
Algorithm: http://www.kr.tuwien.ac.at/staff/eiter/et-archive/cdtr9464.pdf
P and Q are arrays of 2-element arrays (points)
"""


def frechetDist(P,Q):
    ca = np.ones((len(P),len(Q)))
    ca = np.multiply(ca,-1)
    return _c(ca,len(P)-1,len(Q)-1,P,Q)


def main1():
    data_packets = read_json(INPUT_FILE)
    packets = []
    for data_packet in data_packets:
        packet = Packet(data_packet)
        packets.append(packet)

    sizes = set()
    times_127 = []
    times_133 = []
    times_134 = []
    times_137 = []
    count = 0.0
    c = 0.0
    for packet in packets:
        #sizes.add(packet.packet_size)
        if packet.packet_size == 137:
            count += 1
            if packet.time_delta < 0.03:
                times_137.append(packet.time_delta)
            if abs(packet.time_delta -0.05) < 0.01:
                c += 1
        # print packet.packet_size, packet.time_stamp, packet.type
        if packet.packet_size == 127:
            times_127.append(packet.time_delta)
        if packet.packet_size == 133:
            times_133.append(packet.time_delta)
        if packet.packet_size == 134:
            times_134.append(packet.time_delta)
    #print c/count
    if len(times_127) < len(times_133):
        del times_133[len(times_127):]
    else:
        del times_127[len(times_133):]

    if len(times_134) < len(times_137):
        del times_137[len(times_134):]
    else:
        del times_134[len(times_137):]

    times_127.sort()
    times_133.sort()
    times_134.sort()
    times_137.sort()

    plt.plot(times_134, 'r-', label='Parrot Rank 1 - Trace 1')
    plt.plot(times_137, 'g-', label='Solo Rank 1 - Trace 1')
    plt.legend(loc='upper left')
    plt.xlabel("Packet Index")
    plt.ylabel("Time Interval (ms)")
    #plt.title("(c) Curve comparison between Rank 1 Packet from different drones")
    p1 = [(i, times_127[i]) for i in range(0, len(times_127), 20)]
    q1 = [(i, times_133[i]) for i in range(0, len(times_133), 20)]
    p2 = [(i, times_134[i]) for i in range(0, len(times_134), 20)]
    q2 = [(i, times_137[i]) for i in range(0, len(times_137), 20)]
    m1 = np.mean(times_127+times_133)
    m2 = np.mean(times_134+times_137)
    d1= m1/frechetDist(p1, q1)
    d2= m2/frechetDist(p2, q2)
    plt.text(500, 0.075, 'Similarity = ' + '{}'.format(d2), fontsize=10)

    plt.show()

    data_packets = read_json(INPUT_FILE2)
    packets = []
    for data_packet in data_packets:
        packet = Packet(data_packet)
        packets.append(packet)

    sizes = set()
    times_127 = []
    times_133 = []
    times_134 = []
    times_137 = []
    count = 0.0
    c = 0.0
    for packet in packets:
        #sizes.add(packet.packet_size)
        if packet.packet_size == 137:
            count += 1
            times_137.append(packet.time_delta)
            if abs(packet.time_delta -0.05) < 0.01:
                c += 1
        #print packet.packet_size, packet.time_stamp, packet.type
        if packet.packet_size == 127:
            times_127.append(packet.time_delta)
        if packet.packet_size == 133:
            times_133.append(packet.time_delta)
        if packet.packet_size == 134:
            times_134.append(packet.time_delta)
    #print c/count
    if len(times_127) < len(times_133):
        del times_133[len(times_127):]
    else:
        del times_127[len(times_133):]

    if len(times_134) < len(times_137):
        del times_137[len(times_134):]
    else:
        del times_134[len(times_137):]

    times_127.sort()
    times_133.sort()
    times_134.sort()
    times_137.sort()

    plt.plot(times_134, 'r-', label='Parrot Rank 2 - Trace 1')
    plt.plot(times_137, 'g-', label='Solo Rank 2 - Trace 1')
    plt.legend(loc='upper left')
    plt.xlabel("Packet Index")
    plt.ylabel("Time Interval (ms)")
    #plt.title("(d) Curve comparison between Rank 2 Packet from different drones")

    p3 = [(i, times_127[i]) for i in range(0, len(times_127), 20)]
    q3 = [(i, times_133[i]) for i in range(0, len(times_133), 20)]
    p4 = [(i, times_134[i]) for i in range(0, len(times_134), 20)]
    q4 = [(i, times_137[i]) for i in range(0, len(times_137), 20)]
    m3 = np.mean(times_127+times_133)
    m4 = np.mean(times_134+times_137)
    d3= m3/frechetDist(p3, q3)
    d4= m4/frechetDist(p4, q4)
    plt.text(200, 0.05, 'Similarity = ' + '{}'.format(d4), fontsize=10)
    '''
    ax1.set_title('Similarity = ' + '{}'.format(d1), fontsize=7)
    ax2.set_xlabel('Similarity = ' + '{}'.format(d2), fontsize=7)
    ax3.set_title('Similarity = ' + '{}'.format(d3), fontsize=7)
    ax4.set_xlabel('Similarity = ' + '{}'.format(d4), fontsize=7)
    '''
    plt.show()

if __name__ == "__main__":
    main1()
    #sizes_histogram()
    #pattern_timing()
    #pattern4_timing()
    #print frechetDist()
