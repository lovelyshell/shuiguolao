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
#created at 2023/02/07 02:10:00                           #
###########DO NOT EDIT LINES ABOVE!!#######################
###########WRITE YOUR CODE BELOW###########################

L1 = Re('09azAZ', fmt='crange') | Re('-', fmt='cenum') 
L1 = L1.repeat(1, Re.REPEAT_MAX)

prefix = CSeq('http') + CEnum('s').repeat(0,1) + '://'
print(prefix.regex)

suffix = CSeq('com') | 'org' | 'me' | 'cc'
L2 = (L1 + '.')
r = prefix + (L1 + '.').least(0) + L1.name('jack') + '.' + suffix
#domain.repeat()

m = r.exec('https://doc.magic-digit.com')
print(r.regex, m.group('jack'), m.group())


r = CSeq('.') + (~CEnum('/')).least(1) + '.sw' + CRange('az')
print(r.regex)

pig = CSeq('m') +ReT.ANY + 'j'
r = pig.name('foo') + ReT.ANY.least(0) + (Re.Ref('foo')+'z').name('foo2')
print(r.regex)
m = r.exec('mdj! mdjzj! mdjzjj!')
print( m, m.group('foo'), m.group('foo2'))
