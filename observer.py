#!/usr/bin/env python
import argparse
import numpy as np
from plot import Plotter
from json_data_parser import Packet, read_json

DEFAULT_PLOT_NAME = 'plot.pdf'
PLOT_DIR = './plots/'
VALID_PACKET_COUNT_THREADHOLD = 1000


class Observer(object):
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

    def get_addr_map(self):
        addr_map = {}
        for packet in self.packets:
            if packet.sa is not None:
                if addr_map.get(packet.get_addr_hash()):
                    addr_map[packet.get_addr_hash()].append(packet)
                else:
                    addr_map[packet.get_addr_hash()] = [packet]
        return addr_map

    def generate_y_data(self):
        y_data = []
        count = 0
        for packet in self.packets:
            if hasattr(packet, self.observer):
                att = getattr(packet, self.observer)
                if att:
                    y_data.append(att)
                    count += 1
        self.size = count

        if self.observer == 'packet_size':
            y_data = sorted(y_data)
        if self.observer == 'time_stamp' or 'mac_time':
            minimum = getattr(self._packets[0], self.observer)
            y_data = [data-minimum for data in y_data]

        return y_data

    def observe(self):
        y_data = self.generate_y_data()
        plotter = Plotter(range(self.size), [y_data])
        plotter.output_file = PLOT_DIR + '_'.join(self.plot_name.split()) + '.pdf'
        plotter.title = self.plot_name
        plotter.x_label = 'Packet Sequence NO.'
        plotter.y_label = self.observer
        plotter.plot()

    @staticmethod
    def get_signal_sdt(data_list):
        return np.std(data_list)

def main():
    parser = argparse.ArgumentParser(description='UAV DATA Observer')
    parser.add_argument('--input', '-i', metavar='<input json captured data>', required=True)
    parser.add_argument('--observer', '-o', metavar='<y axis value type>', required=True,
                        choices=['packet_size', 'time_stamp', 'mac_time', 'signal'])
    parser.add_argument('--plot', '-p', metavar='<plot name>')
    args = parser.parse_args()
    print "processing packets..."
    data_packets = read_json(args.input)
    print "creating observer..."
    observer = Observer(data_packets, args.observer, args.plot)

    addr_map = observer.get_addr_map()

    stds = []
    for addr, packets in addr_map.iteritems():
        if len(packets) > VALID_PACKET_COUNT_THREADHOLD:
            std = observer.get_signal_sdt([packet.signal for packet in packets])
            stds.append(std)
            print len(packets)
            print "FROM: %s TO: %s STD: %s SSID: %s" % (packets[0].sa, packets[0].da, std, packets[0].ssid)

    print "plotting..."
    observer.observe()

if __name__ == "__main__":
    main()
