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
#created at 2023/02/20 12:17:01             #
####DO NOT EDIT LINES ABOVE!!################
####WRITE YOUR CODE BELOW####################



lst = []
for f in File('/home/amily/.shuiguolao-trash/').files:
    if f.name.endswith('.py'):
        lst.append(f)
        
'''
lst.sort(lambda)
print(lst)
'''
lst.sort(key=lambda el: el.mtime)
print(lst)



