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
lib_p = exec_parent_p.joinpath('lib')
lab_file_p = lib_p.joinpath('File')
lab_re_p = lib_p.joinpath('Re')
sys.path.append(lab_file_p.as_posix())
sys.path.append(lab_re_p.as_posix())

from Re import *
from File import File, getoseol, Trash
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
#created at 2023/02/02 11:35:47                           #
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

r = CSeq('.sw') + CRange('az')
re_vi_mess = ReT.LINE_BEGIN + '.' + ReT.LANY.least(1) + Re.Assert(r) 
print(re_vi_mess.regex)
m = re_vi_mess.exec('.xx.txt.swp')
print(m)

re_history= ReT.LINE_BEGIN + ReT2.INT +  (CSeq('.py')|'.js') + ReT.LINE_END
def clear_one(f, rinfo):
    rm = False
    go_on = True
    #清除python缓存
    if f.name == '__pycache__':
        rm = True
        go_on = False
    elif f.isFile():
        if re_vi_mess.exec(f.name): 
            rm = True
        elif re_history.exec(f.name):
            if f.parent.name == 'history':
                rm = True
    else:
        pass
    if rm:
        Trash.add(f.path)
    return go_on
            

File.R(sys.argv[1], clear_one)
'''
def clear_vim_mess():
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
'''






