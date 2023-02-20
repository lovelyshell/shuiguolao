#!/usr/bin/shuiguolao

from preload import *

if __name__ == '__main__':
    print(f'************run \
    {sgl_run_timestamp_s}\
    *************')
##########shuiguolao version 0.1#############
#shortcut:                                  #
#<C-N>    browse history, down              #
#<C-P>    browse history, up                #
#<C-S>-r  save and run file                 #
#<C-S>-R  save and prepare to run file      #
#<C-S>-N  create a new file                 #
#created at 2023/02/18 05:01:25             #
####DO NOT EDIT LINES ABOVE!!################
####WRITE YOUR CODE BELOW####################

print(current.dir)

x, y, z = 1, 2, 3

def abc(o):
    param_type_check(o, [int, str])
    e=VarError(o)
    print(e)

abc(File)







