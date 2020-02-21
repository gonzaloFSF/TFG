import gdb
import re
import os
import sys


def load_data(dict_str,desp):

    try:

        all_inst = gdb.execute('x /{}i $rip'.format(desp),to_string=True).split("\n")

    except Exception as e:
        dict_str['opcode'] = None
        return

    dump_data_instr = all_inst[-2]
    #print(dump_data_instr)
    dict_str['ins_addr'] = re.findall("(0x[a-fA-F0-9]+)",dump_data_instr)[0]
    dict_str['ins_data'] = re.findall("\t([\W\w]*?)$",dump_data_instr)[0]
    #print("A",dict_str)
    #print(gdb.execute('disassemble /r {},{}+0x1'.format(dict_str['ins_addr'],dict_str['ins_addr']),to_string=True))
    opcode = gdb.execute('disassemble /r {},{}+0x1'.format(dict_str['ins_addr'],dict_str['ins_addr']),to_string=True)
    dict_str['opcode'] = re.findall("\:\t([a-fA-F0-9 ]*?)\t",opcode)[0]
    #print("D",dict_str)


def extra_data(desp):
    ins_information = {}
    load_data(ins_information,desp)
    return ins_information




gdb.execute('set disassembly-flavor intel')
gdb.execute('set confirm off')
gdb.execute('file jump_line_detect.o')
gdb.execute('break * main')
gdb.execute('r')


f = open("traza.log","w")
count = 0



while True:

    data = extra_data(1)

    if data['opcode'] == None:
        break

    if len(re.findall("^7|^0[Ff]8",data["opcode"])):

        f.write(str(data)+"\n")
        data = extra_data(2)
        f.write(str(data)+"\n")
        gdb.execute('si')
        data = extra_data(1)
        f.write(str(data)+"\n")
        sys.stderr.write(str(count)+"\n")
        count += 1

    else:

        gdb.execute('si')


gdb.execute('quit')
