# cat parrot.json | grep data.data > temp
def multiple_frames_packet():
    with open('temp', 'r') as lines:
        count_long_packet = 0
        data_byte_lists = []
        for count_total_packet, line in enumerate(lines):
            data_byte_list = line.lstrip("data.data\"\: ").rstrip("\",\n").split(":")
            data_byte_lists.append(data_byte_list)
            packet_size = len(line.lstrip("data.data\"\: ").rstrip("\",\n").split(":"))
            frame_size = int(line.lstrip("data.data\"\: ").rstrip("\",\n").split(":")[3], 16)
            if packet_size > frame_size:
                count_long_packet += 1
                #print data_byte_list

        print count_long_packet
        print count_total_packet
        return data_byte_lists


def count_each_frame_type(data_byte_lists):
    count_01 = 0
    count_02 = 0
    count_03 = 0
    count_04 = 0
    sizes_01 = []
    sizes_02 = []
    sizes_03 = []
    sizes_04 = []

    for data_byte_list in data_byte_lists:
        print data_byte_list
        if data_byte_list[0] == '01':
            count_01 += 1
            sizes_01.append(len(data_byte_list))
        if data_byte_list[0] == '02':
            count_02 += 1
            sizes_02.append(len(data_byte_list))
        if data_byte_list[0] == '03':
            count_03 += 1
            sizes_03.append(len(data_byte_list))
        if data_byte_list[0] == '04':
            count_04 += 1
            sizes_04.append(len(data_byte_list))

    print count_01, count_02, count_03, count_04
    ave_size_01 = sum(sizes_01) / float(len(sizes_01))
    ave_size_02 = sum(sizes_02) / float(len(sizes_02))
    ave_size_04 = sum(sizes_04) / float(len(sizes_04))
    print count_01, count_02, count_03, count_04
    print ave_size_01, ave_size_02, ave_size_04


if __name__ == "__main__":
    data_byte_list = multiple_frames_packet()
    count_each_frame_type(data_byte_list)
