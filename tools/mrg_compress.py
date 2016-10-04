#!/usr/bin/env python
#
# MRG compressor
# comes with ABSOLUTELY NO WARRANTY.
#
# Copyright (C) 2016 RadioTB
#
# Portions Copyright (C) 2016 RadioTB
#
# MRG files extraction utility
# For more information, see Specifications/mzp_format.md

import os
import sys
import struct


FILE_LIST = 'allscr.list'
INPUT_FILE_NAME = 'allscr.mrg'
output_dir = os.path.splitext(INPUT_FILE_NAME)[0] + '-unpacked'


class ArchiveEntry:
    def __init__(self, sector_offset, real_offset, sector_size_upper_boundary, real_size, number_of_entries):
        self.sector_offset = sector_offset
        self.real_offset = real_offset
        self.sector_size_upper_boundary = sector_size_upper_boundary
        self.real_size = real_size
        self.size = real_size - (((sector_size_upper_boundary - 1) // 0x20) * 0x10000)
        data_start_offset = 6 + 2 + number_of_entries * 8
        self.offset = real_offset - self.sector_offset * 0x800

    
    

list_file = open(os.path.join(output_dir, FILE_LIST), 'r')
filenames = []
filenames = list_file.readlines()
list_file.close()


entries = []
number_of_entries = len(filenames)
real_offset = 0
previous_size = 0

buf = 0

temp_file = open("allscr.tmp", 'wb')
for i in range(number_of_entries):
    
    real_size = os.path.getsize(os.path.join(output_dir, filenames[i]))
    sector_offset = real_offset // 0x800
    sector_size_upper_boundary = (real_size // 0x800) + 1
    entries.append(ArchiveEntry(sector_offset=sector_offset, real_offset=real_offset, sector_size_upper_boundary=sector_size_upper_boundary, real_size=real_size, number_of_entries=number_of_entries))
    
    src_file = open(os.path.join(output_dir, filenames[i]), 'rb')
    file_data = src_file.read(real_size)
    src_file.close()
    temp_file.write(file_data)

    real_offset = real_offset + real_size
    
    
temp_file.close();


head = open("head.tmp", 'wb')
head.write(bytes("mrgd00", 'ASCII'))
head.write(struct.pack('<H', number_of_entries))
for k in range(number_of_entries):
    head.write(struct.pack('<HHHH',entries[k].sector_offset, entries[k].offset, entries[k].sector_size_upper_boundary, entries[k].size))
head.close()


head = open("head.tmp", 'rb')
head_size = os.path.getsize("head.tmp")
data = open("allscr.tmp", 'rb')
data_size = os.path.getsize("allscr.tmp")
out_file = open("allscr.test", 'wb')

file_data = head.read(head_size)
out_file.write(file_data)
file_data = data.read(data_size)
out_file.write(file_data)

head.close()
data.close()
out_file.close()
