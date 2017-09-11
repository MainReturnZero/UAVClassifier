#!/usr/bin/env python
import json
INPUT_FILE = "./data/0402_3dr"


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
            self._type = int(packet['_source']['layers']['frame']['frame.encap_type'])
            self._type_subtype = int(packet['_source']['layers']['wlan']['wlan.fc_tree']['wlan.fc.subtype'])
            self._mac_time = int(packet['_source']['layers']['wlan_radio']['wlan_radio.timestamp'])
            self._signal = int(packet['_source']['layers']['wlan_radio']['wlan_radio.signal_dbm'])
            self._channel = int(packet['_source']['layers']['wlan_radio']['wlan_radio.channel'])
            self._sa = packet['_source']['layers']['wlan']['wlan.sa']
            self._da = packet['_source']['layers']['wlan']['wlan.da']

        except KeyError:
            self._packet_size = 0
            self._time_stamp = 0
            self._type = 0
            self._type_subtype = -1
            self._mac_time = 0
            self._signal = 0
            self._channel = 0
            self._sa = None
            self._da = None
            self._ssid = None
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
    def ssid(self):
        return self._ssid

    @ssid.setter
    def ssid(self, ssid):
        self._ssid = ssid

    def get_addr_hash(self):
        if self.sa:
            return hash(self.sa)

def main():
   data_packets = read_json(INPUT_FILE)
   packets = []
   for data_packet in data_packets:
       packet = Packet(data_packet)
       packets.append(packet)

   for packet in packets:
       print packet.packet_size, packet.time_stamp, packet.type

if __name__ == "__main__":
    main()
