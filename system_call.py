import subprocess
import re
import time

ALL_INTERFACE = "tshark -D "
CAPTURE_CMD = "tshark "     # tailed with an empty char to be safe, ex: tshark + option


def find_wifi_interface():
    ls = subprocess.Popen(ALL_INTERFACE.split(), stdout=subprocess.PIPE)
    lines = ls.stdout.readlines()
    interface = None
    for line in lines:
        if 'Wi-Fi' in line:
            interface = re.search(r'\d+', line).group()
    return interface


def get_capture_cmd(options=None):
    global CAPTURE_CMD
    cmd = CAPTURE_CMD
    if options:
        for option in options:
            cmd += option
    return cmd


def test():
    option_file = [" -w my.pcap -c 1000", " wlan host 28:f0:76:1c:3e:c4"]
    cmd = get_capture_cmd(option_file)
    t = subprocess.Popen(cmd.split(), shell=True)
    time.sleep(3)
    # t.terminate()

if __name__ == "__main__":
    test()
