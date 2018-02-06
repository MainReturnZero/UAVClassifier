#!/usr/bin/env python
import json
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import UnivariateSpline
from scipy.stats import norm

INPUT_FILE = "./data/parrot.json"


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
            self._signal = int(packet['_source']['layers']['wlan_radio']['wlan_radio.signal_dbm'])
            self._channel = int(packet['_source']['layers']['wlan_radio']['wlan_radio.channel'])
            self._sa = packet['_source']['layers']['wlan']['wlan.sa']
            self._da = packet['_source']['layers']['wlan']['wlan.da']
            self._data = packet['_source']['layers']['data']['data.data']

        except KeyError:
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
   times = []
   count = 0.0
   c = 0.0
   for packet in packets:
       sizes.add(packet.packet_size)
       if packet.packet_size == 137:
           count += 1
           times.append(packet.time_delta)
           if abs(packet.time_delta -0.05) < 0.01:
               c += 1
       # print packet.packet_size, packet.time_stamp, packet.type
   print c/count
   times.sort()
   plt.plot(times, '.')
   plt.show()


if __name__ == "__main__":
    #main()
    #sizes_histogram()
    #pattern_timing()
    pattern4_timing()
