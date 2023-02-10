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

from Re import *
from File import File, getoseol, run_command
cwd = File('.')


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
#created at 2023/02/02 09:05:56                           #
###########DO NOT EDIT LINES ABOVE!!#######################
###########WRITE YOUR CODE BELOW###########################

r = ReT.LINE_BEGIN + ReT2.INT + '.py' + ReT.LINE_END
for f in File('./py/history').files:
    m = r.exec(f.name)
    if not m:
        print('skip ', f.name)
    else:
        print('remove ', f.name, f.path)
        #run_command(['rm',  f.path])






