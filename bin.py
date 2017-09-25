
class Bin(object):
    def __init__(self):
        self._packet_bin = []
        self._valid_size = 0

    def __iter__(self):
        for packet in self.packet_bin:
            yield packet

    def __getitem__(self, key):
        return self.packet_bin[key]

    @property
    def packet_bin(self):
        return self._packet_bin

    @packet_bin.setter
    def packet_bin(self, packet_bin):
        self._packet_bin = packet_bin

    @property
    def valid_size(self):
        return self._valid_size

    @valid_size.setter
    def valid_size(self, valid_size):
        self._valid_size = valid_size

    def append(self, packet):
        self.packet_bin.append(packet)

    def __len__(self):
        return len(self.packet_bin)

    def generate_y_data(self, data_name):
        y_data = []
        count = 0
        for packet in self.packet_bin:
            if hasattr(packet, data_name):
                att = getattr(packet, data_name)
                if att:
                    y_data.append(att)
                    count += 1
        self.valid_size = count

        if data_name == 'packet_size':
            y_data = sorted(y_data)
        if data_name == 'time_stamp' or data_name == 'mac_time':
            minimum = getattr(self.packet_bin[0], data_name)
            y_data = [data-minimum for data in y_data]

        return y_data