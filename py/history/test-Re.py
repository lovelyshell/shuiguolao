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
lab_file_p = exec_parent_p.joinpath('lib/File')
lab_re_p = exec_parent_p.joinpath('lib/Re')
sys.path.append(lab_file_p.as_posix())
sys.path.append(lab_re_p.as_posix())

from Re import *
from File import File, getoseol
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
#created at 2023/02/01 12:05:29                           #
###########DO NOT EDIT LINES ABOVE!!#######################
###########WRITE YOUR CODE BELOW###########################

#测试字符集排除
r = CRange('az') - CEnum('hijk')
m = r.exec('hijklmnopq')
print('字符集排除，输出应改为l:', r.s, m)










