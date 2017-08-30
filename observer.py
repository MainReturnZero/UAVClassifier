#!/usr/bin/env python
import argparse
from plot import Plotter
from json_data_parser import Packet, read_json

INPUT_FILE = './data/0402_3dr'


class Observer(object):
    def __init__(self, data_packets):
        self._packets = [Packet(data_packet) for data_packet in data_packets]
        self._size = len(data_packets)

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size):
        self._size = size

    @property
    def packets(self):
        return self._packets

    @packets.setter
    def packets(self, packets):
        self._packets = packets

    def timer(self):
        plotter = Plotter(range(self.size), [[packet.time_stamp for packet in self.packets]], 'plots/timer.pdf')
        plotter.plot()

    def sizer(self):
        y_data = sorted([packet.len for packet in self.packets])
        y_datas = [y_data]
        plotter = Plotter(range(self.size), y_datas, 'plots/sizer.pdf')
        plotter.plot()


def main():
    parser = argparse.ArgumentParser(description='UAV DATA Observer')
    parser.add_argument('--input', '-i', metavar='input json captured data', required=True)
    args = parser.parse_args()
    data_packets = read_json(args.input)
    observer = Observer(data_packets)
    observer.sizer()

if __name__ == "__main__":
    main()