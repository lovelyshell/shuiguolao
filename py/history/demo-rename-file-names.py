#!/usr/bin/python3
#shuiguolao version: 0.1
import sys
import os
import time
from pathlib import Path
from functools import cmp_to_key

exec_py_p = Path(__file__)
exec_dir_p = exec_py_p.parent.resolve()
exec_parent_p = exec_dir_p.parent
lab_file_p = exec_parent_p.joinpath('File')
lab_re_p = exec_parent_p.joinpath('Re')
sys.path.append(lab_file_p.as_posix())
sys.path.append(lab_re_p.as_posix())

from File import File, getoseol, run_command
cwd = File('.')
from Re import *

#py_run_timestamp_s = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())
py_run_timestamp_s = time.strftime('%H:%M:%S', time.localtime())
print(f'****************run {py_run_timestamp_s}************')
################shuiguolao version 0.1#####################
#shortcut:                                                #
#<C-N>    browse history, down                            #
#<C-P>    browse history, up                              #
#<C-S>-r  save and run file in main window                #
#<C-S>-R  save and (as root) run file in main window      #
#<C-S>-n  create a new file                               #
#created at 2023/01/31 08:56:22                           #
###########DO NOT EDIT LINES ABOVE!!#######################
###########WRITE YOUR CODE BELOW###########################
'''
https://www.v2ex.com/t/542658
求助：批处理怎样批量删除文件名前缀？
删去从起始到一个字符的全部字符
例如
1^文件(1).txt
2^文件(2).txt
……
30^文件(30).txt
修改为
文件(1).txt
文件(2).txt
……
文件(30).txt
'''

#change this value to help test
OP = 2

NR= 30
#import  subprocess
def do_create():
    for i in range(0, NR):
        name = f'{i}^文件({i}).txt'
        run_command(['touch', name])
        #subprocess.Popen(['touch', name], shell=False)
        

import shutil
def do_rename():
    for f in cwd.files:
        segs = f.name.split('^')
        if len(segs) == 2:
            newname = segs[1]
            shutil.move(f.name, newname)

def do_delete():
    trash_path = os.path.expanduser('~/.garbage')
    #subprocess.Popen(['mkdir', garbage_dir], shell=True)
    run_command(['mkdir', trash_path])
    u = ReT.UINT
    print(u.s)
    reg = Re('文件(') + ReT.UINT + ').txt'
    print(reg.s)
    for f in cwd.files:
        m = reg.exec(f.name)
        if m:
            print('delete file', f.name)
            run_command(['mv', f.name, trash_path])
            


if OP == 0:
    do_create()
elif OP == 1:
    do_rename()
elif OP == 2:
    do_delete()
else:
    pass








