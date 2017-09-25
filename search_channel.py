import argparse
import subprocess
import time
from system_call import get_capture_cmd, find_wifi_interface
from capture import CaptureOptions

BASE_CMD = '/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport /usr/sbin/airport'
INFO_COMD = BASE_CMD + ' -I'
DISASSOCIATE_CMD = BASE_CMD + ' -z'
CHANNEL_CMD = BASE_CMD + ' -c'


def search_channel(channel, timeout, options, file_prefix):
    # print DISSACIATE_CMD.split()
    # print (CHANNEL_CMD+str(channel)).split()
    # return
    subprocess.call(DISASSOCIATE_CMD.split())
    subprocess.call((CHANNEL_CMD + str(channel)).split())
    subprocess.call(INFO_COMD.split())

    options.save_to = file_prefix + '_' + str(channel) + '.pcap'
    option_tag = options.generate()
    cmd = get_capture_cmd([option_tag])
    t = subprocess.Popen(cmd.split())
    time.sleep(timeout)
    t.terminate()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='UAV DATA Capture Tool')
    parser.add_argument('--monitor', '-I', default=True, action='store_true')
    parser.add_argument('--file', '-w', metavar='<output file for captured data>')
    parser.add_argument('--packet_count', '-c',metavar='<packet upper limit for capturing>')
    parser.add_argument('--other', '-o', metavar='<other>', nargs='*', default=[])
    parser.add_argument('--timeout', '-t', metavar='<timeout for each channel>', default=5)

    args = parser.parse_args()
    options = CaptureOptions(monitor_mod=args.monitor,
                             interface=find_wifi_interface(),
                             save_to=args.file,
                             packet_limit=args.packet_count,
                             other=' '.join(args.other),
                             )
    for i in range(1, 12, 1):
        search_channel(i, float(args.timeout), options, args.file)
