import gdb
import re
import os
import sys


def get_list_of_function():
    functions = gdb.execute('info functions name',to_string=True).split("\n")
    functions = functions[1:-1]
    functions = list(filter(lambda x: len(x) and not ("File" in x),functions))
    print(functions)
    for name in functions:
        print(name)
        print(re.findall(" \*{0,2}([A-Za-z0-9_]*?)\(",name))
        re.findall(" \\*?([\W\w]*?)\(",name).pop()

    name_functions = [re.findall(" \*?([\W\w]*?)\(",name).pop() for name in functions]
    return name_functions

def load_data(dict_str,desp):

    all_inst = gdb.execute('x /{}i $rip'.format(desp),to_string=True).split("\n")
    dump_data_instr = all_inst[-2] 
    dict_str['ins_addr'] = re.findall("(0x[\W\w]*?) ",dump_data_instr)[0]
    dict_str['ins_data'] = re.findall("\t([\W\w]*?)$",dump_data_instr)[0]
    opcode = list(filter(lambda x: "=>" in x , gdb.execute('disassemble /r {}'.format(dict_str['ins_addr']),to_string=True).split("\n")))[0]
    print(gdb.execute('disassemble /r {}'.format(dict_str['ins_addr']),to_string=True).split("\n")) 
    #print(opcode)
    dict_str['opcode'] = re.findall("\:\t([a-fA-F0-9 ]*?)\t",opcode)[0]

def get_conditional_jump_lines(dis_str):
    list_dis_str = dis_str.split("\n")
    return list(filter(lambda x: len(re.findall("\:\t7|\:\t0[Ff]8",x)),list_dis_str))

def get_all_break_point_address(list_name_func):
    all_address = []

    for name_fun in list_name_func:
        all_address += get_break_point_address(name_fun)

    return all_address

def get_break_point_address(name_func):

    try:
        dis_str = gdb.execute('disassemble /r {}'.format(name_func),to_string=True)
    except:
        return []
    list_ints = get_conditional_jump_lines(dis_str)
    #print(list_ints)
    list_addrs = [(name_func+re.findall("<([\W\w]*?)>",instr)[0]) for instr in list_ints]
    return list_addrs

def extra_data(desp):
    ins_information = {}
    load_data(ins_information,desp)
    return ins_information

def add_break_points(list_break_points):
    

    for break_address in list_break_points:
        gdb.execute('break * {}'.format(break_address))


val = '0'
gdb.execute('set disassembly-flavor intel')
gdb.execute('set confirm off')
gdb.execute('file jump_line_detect.o')

print(gdb.execute('info functions',to_string=True).split("\n"))

gdb.execute('break * main')
gdb.execute('r')

#list_func = get_list_of_function()
#list_break_points = get_all_break_point_address(list_func)
#add_break_points(list_break_points)
#print(list_break_points)

f = open("out.log","w")
count = 0



while val != '1' :

    data = extra_data(1)
    #print(data)
    #input()
    if len(re.findall("^7|^0[Ff]8",data["opcode"])) :
        f.write(str(data)+"\n")
        data = extra_data(2)
        f.write(str(data)+"\n")
        gdb.execute('si')
        data = extra_data(1)
        f.write(str(data)+"\n")
        sys.stderr.write(str(count)+"\n")
        count += 1
    elif int(data['ins_addr'],16) == 0x0000555555555172:
        break

    else:
        gdb.execute('si')


gdb.execute('quit')
