import subprocess
import re

ALL_INTERFACE = "wireshark -D"
CAPTURE_CMD = "wireshark -I"

def find_wifi():
    ls = subprocess.Popen(ALL_INTERFACE.split(), stdout=subprocess.PIPE)
    lines = ls.stdout.readlines()
    interface = None
    for line in lines:
        if 'Wi-Fi' in line:
            interface = re.search(r'\d+', line).group()
    return interface


def get_cmd(options=None):
    global CAPTURE_CMD
    interface = find_wifi()
    cmd = CAPTURE_CMD + ' -i ' + interface
    if options:
        for option in options:
            cmd += option
    return cmd


def capture():
    option_file = ' -w my.pcap -c 100'
    cmd = get_cmd([option_file])
    subprocess.call(cmd.split())

capture()
