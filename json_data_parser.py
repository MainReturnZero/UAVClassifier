#!/usr/bin/env python
import json
INPUT_FILE = "./data/0402_3dr"

def read_json(input_file):
    with open(input_file) as i:
        return json.load(i)


class Packet(object):

    def __init__(self, packet):
        self._len = int(packet['_source']['layers']['frame']['frame.len'])
        self._time_stamp = float(packet['_source']['layers']['frame']['frame.time_epoch'])
        self._type = int(packet['_source']['layers']['frame']['frame.encap_type'])

    @property
    def len(self):
        return self._len

    @len.setter
    def len(self, len):
        self._len = int(len)

    @property
    def time_stamp(self):
        return float(self._time_stamp)

    @time_stamp.setter
    def time_stamp(self, time_stamp):
        self._time_stamp = time_stamp

    @property
    def type(self):
        return int(self._type)

    @type.setter
    def type(self, type):
        self._type = type


def main():
   data_packets = read_json(INPUT_FILE)
   packets = []
   for data_packet in data_packets:
       packet = Packet(data_packet)
       packets.append(packet)

   for packet in packets:
       print packet.len, packet.time_stamp, packet.type

if __name__ == "__main__":
    main()
