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
#<C-S>-R  save and prepare to run file in main window     #
#<C-S>-N  create a new file                               #
#created at 2023/02/02 11:35:22                           #
###########DO NOT EDIT LINES ABOVE!!#######################
###########WRITE YOUR CODE BELOW###########################
'''
.shuiguolao.py.swm	  
 .shuiguolao.py.swn	  
 .shuiguolao.py.swo	 
 .shuiguolao.py.swp
'''

argv = sys.argv
if len(argv) < 2:
    print('need explictly specify directory path to clean')
    sys.exit()

endpat = CSeq('.sw') + CEnum('mnop')
r = ReT.LINE_BEGIN + CSeq('.') + ReT.ANY.least(1) + Re.Assert(endpat) + ReT.LINE_END
print(sys.argv)

print(r.s)
d = File(argv[1])
for f in d.files:
    m = r.exec(f.name)
    if m:
        print('delete', f.name)
        run_command(['rm', f.path])






