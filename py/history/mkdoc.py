#!/usr/bin/shuiguolao
#shuiguolao version: 0.1

from preload import *
################shuiguolao version 0.1#####################
#shortcut:                                                #
#<C-N>    browse history, down                            #
#<C-P>    browse history, up                              #
#<C-S>-r  save and run file in main window                #
#<C-S>-R  save and prepare to run file in main window     #
#<C-S>-N  create a new file                               #
#created at 2023/02/12 01:26:41                           #
###########DO NOT EDIT LINES ABOVE!!#######################
###########WRITE YOUR CODE BELOW###########################


import nodoc

if __name__ == '__main__':
    for py_path in ['py/lib/File.py', 'py/lib/Re.py']:
        new_p = nodoc.nodoc(py_path)
        run_command(['pydoc3', '-w', new_p.as_posix()])






