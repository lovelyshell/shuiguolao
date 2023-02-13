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
lib_file_p = lib_p.joinpath('File')
lib_re_p = lib_p.joinpath('Re')
sys.path.append(lib_file_p.as_posix())
sys.path.append(lib_re_p.as_posix())

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
#<C-S>-R  save and prepare to run file in main window     #
#<C-S>-N  create a new file                               #
#created at 2023/02/03 10:40:39                           #
###########DO NOT EDIT LINES ABOVE!!#######################
###########WRITE YOUR CODE BELOW###########################

#删除掉所有以##NODOC打头的块，生成前缀为pydoc-的中间文件，供pydoc3调用。

assert len(sys.argv) == 2
src_path = sys.argv[1]
src_f = File(src_path)

def indent_width(s):
    w = 0
    for i in range(len(s)):
        if s[i] == '\t':
            w += 8
        elif s[i] == ' ':
            w += 1
        else:
            break
    return w

#re_undoc = ReT.LINE_BEGIN + CSeq('##NODOC') + ReT.LINE_END + ReT.ANY.least(1) + 
def Nodoc(filepath):
    lines = src_f.readlines()
    in_nodoc = False
    block_indent = 0
    in_block = False
    is_modified = False
    for i in range(len(lines)):
        line = lines[i]
        #skip empty line
        if len(line.strip()) == 0:
            continue
        w = indent_width(line)

        while 1:
            if not in_nodoc:
                if line.strip() == '##NODOC':    
                    block_indent = w
                    in_nodoc = True
            #一开始是在NODOC里的
            else:
                #block未开始不考虑状态变化
                if not in_block:
                    if line.strip().startswith('class ') or line.strip().startswith('def '):
                        in_block = True

                #临界状态 回到初始化
                elif w <= block_indent:
                    #print('>>>', w, block_indent, line)
                    in_nodoc = False
                    in_block = False
                    continue
            if in_nodoc:
                print(line)
                lines[i] = ''
                is_modified = True
            break


    if is_modified:
        new_p = src_f.p.with_name('pydoc-'+src_f.name)
        f2 = File(new_p)
        print(f2.name)
        f2.writelines(lines)









