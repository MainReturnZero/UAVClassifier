#!/usr/bin/env python
import argparse
import datetime
import subprocess
import os
import numpy as np
from plot import Plotter
from bin import Bin
from json_data_parser import Packet, read_json

DEFAULT_PLOT_NAME = str(datetime.datetime.now())
PLOT_DIR = './plots/'
VALID_PACKET_COUNT_THRESHOLD = 10


class Observer(object):
    bins = {}

    def __init__(self, data_packets, observer, plot_name=DEFAULT_PLOT_NAME):
        self._packets = [Packet(data_packet) for data_packet in data_packets]
        self._observer = observer
        self._size = len(data_packets)
        self._plot_name = plot_name or DEFAULT_PLOT_NAME

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size):
        self._size = size

    @property
    def packets(self):
        return self._packets

    @property
    def observer(self):
        return self._observer

    @observer.setter
    def observer(self, observer):
        self._observer = observer

    @packets.setter
    def packets(self, packets):
        self._packets = packets

    @property
    def plot_name(self):
        return self._plot_name

    @plot_name.setter
    def plot_name(self, plot_name):
        self._plot_name = plot_name

    def sort_in_bins(self):
        for packet in self.packets:
            if packet.sa is not None:
                if not self.bins.get(packet.sa):
                    self.bins[packet.sa] = Bin()
                self.bins[packet.sa].append(packet)
        return self.bins

    def observe(self):
        y_data_list = []
        addrs = []
        for addr, packet_bin in self.bins.iteritems():
            if len(packet_bin) > VALID_PACKET_COUNT_THRESHOLD:
                y_data_list.append(packet_bin.generate_y_data(self.observer))
                addrs.append(addr)
        plotter = Plotter(range(self.size), y_data_list)
        plotter.output_file = PLOT_DIR + '_'.join(self.plot_name.split()) + '.pdf'
        plotter.x_label = 'Packet Sequence Number'
        plotter.y_label = addrs
        plotter.plot()

    def print_bin(self, bin_name):
        if self.bins.get(bin_name):
            for packet in self.bins[bin_name]:
                print packet.sa, packet.da

    @staticmethod
    def get_signal_std(data_list):
        return np.std(data_list)

    @staticmethod
    def get_signal_avg(data_list):
        return np.mean(data_list)

    @staticmethod
    def get_signal_without_3std(data_list):
        std = np.std(data_list)
        avg = np.mean(data_list)
        new_data_list = [data for data in data_list if avg - 3 * std <= data <= avg + 3 * std]
        return np.std(new_data_list)


def main():
    parser = argparse.ArgumentParser(description='UAV DATA Observer')
    parser.add_argument('--input', '-i', metavar='<input json captured data>', required=True)
    parser.add_argument('--observer', '-o', metavar='<y axis value type>', required=True,
                        choices=['packet_size', 'time_stamp', 'mac_time', 'signal'])
    parser.add_argument('--plot', '-p', metavar='<plot name>')
    args = parser.parse_args()

    file_director, file_name = os.path.split(args.input)
    plot_name = file_name.split('.')[0]

    print "processing packets..."
    try:
        data_packets = read_json(args.input)
    except ValueError:
        CONVERT_PCAP_TO_JSON = 'tshark -r ' + str(args.input) + ' -l -n -T json > ' + str(plot_name) + '.json'
        os.system(CONVERT_PCAP_TO_JSON)
        data_packets = read_json(str(plot_name) + '.json')

    print "creating observer..."
    observer = Observer(data_packets, args.observer, plot_name=plot_name)

    packet_bins = observer.sort_in_bins()

    stds = []
    for addr, packets in packet_bins.iteritems():
        if len(packets) > VALID_PACKET_COUNT_THRESHOLD:
            ## std = Observer.get_signal_without_3std([packet.signal for packet in packets])
            std = Observer.get_signal_std([packet.signal for packet in packets])
            avg = Observer.get_signal_avg([packet.signal for packet in packets])
            stds.append(std)
            print len(packets)
            print "FROM: %s TO: %s STD: %s  AVG: %s SSID: %s" % (packets[0].sa, packets[0].da, std, avg, packets[0].ssid)

    print "plotting..."
    observer.observe()
    observer.print_bin('8a:dc:96:3b:a8:bf')

if __name__ == "__main__":
    main()
