from system_call import find_wifi_interface, get_cmd
import argparse
import subprocess

class CaptureTag(object):
    interface = 'i'
    monitor_mod = 'I'
    save_to = 'w'
    packet_limit = 'c'
    other = ''


class CaptureOptions(object):
    tag = CaptureTag()

    def __init__(self, interface, monitor_mod=True, save_to='my.pcap', packet_limit=None,
                 source_addr=None, dst_addr=None, other=None):
        self._interface = interface
        self._monitor_mod = monitor_mod
        self._save_to = save_to
        self._packet_limit = packet_limit
        self._source_addr = source_addr
        self._dst_addr = dst_addr
        self._other = other

    @property
    def interface(self):
        return self._interface

    @interface.setter
    def interface(self, interface):
        self._interface = interface

    @property
    def monitor_mod(self):
        return self._monitor_mod

    @monitor_mod.setter
    def monitor_mod(self, monitor_mod):
        if isinstance(monitor_mod, bool):
            self._monitor_mod = monitor_mod
        else:
            TypeError("Monitor mode is a boolean value, got %s" % type(monitor_mod))

    @property
    def save_to(self):
        return self._save_to

    @save_to.setter
    def save_to(self, save_to):
        self._save_to = save_to

    @property
    def packet_limit(self):
        return self._packet_limit

    @packet_limit.setter
    def packet_limit(self, packet_limit):
        self._packet_limit = packet_limit

    @property
    def source_addr(self):
        return self._source_addr

    @source_addr.setter
    def source_addr(self, source_addr):
        self._source_addr = source_addr

    @property
    def dst_addr(self):
        return self._dst_addr

    @dst_addr.setter
    def dst_addr(self, dst_addr):
        self._dst_addr = dst_addr

    @property
    def other(self):
        return self._other

    @other.setter
    def other(self, other):
        self._other = other

    def generate(self):
        options = []
        for option, value in self.__dict__.iteritems():
            if option == "_monitor_mod" and value:
                options.append('-' + str(getattr(self.tag, option[1:])))    # TODO: [1:0] is a dirty hack
            elif value and option != '_other':
                options.append('-' + str(getattr(self.tag, option[1:])) + ' ' + str(value))
        if self.other:
            options.append(self.other)
        return ' '.join(options)


def test():
    options = CaptureOptions(monitor_mod=True, interface=7)
    options.save_to = 'my.pcap'
    options.packet_limit = 100
    try:
        assert(options.generate() == "-i 7 -I -c 00 -w my.pcap")
    except AssertionError:
        print ("Test failed, please check source code in %s" % __file__)
        raise
    print "All Tests Passed!"

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='UAV DATA Capture Tool')
    parser.add_argument('--monitor', '-I', default=True, action='store_true')
    parser.add_argument('--file', '-w', metavar='<output file for captured data>')
    parser.add_argument('--packet_count', '-c',metavar='<packet upper limit for capturing>')
    parser.add_argument('--other', '-o', metavar='<other>', nargs='*', default=[])

    args = parser.parse_args()
    options = CaptureOptions(monitor_mod=args.monitor,
                             interface=find_wifi_interface(),
                             save_to=args.file,
                             packet_limit=args.packet_count,
                             other=' '.join(args.other),
                             )
    option_tag = options.generate()
    print option_tag
    cmd = get_cmd([option_tag])
    subprocess.call(cmd.split())
