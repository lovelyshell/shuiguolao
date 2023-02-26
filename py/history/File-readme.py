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
#created at 2023/02/21 17:15:31             #
####DO NOT EDIT LINES ABOVE!!################
####WRITE YOUR CODE BELOW####################

'''
File提供隐藏了文件的读写细节，你可以更方便的操作文件
'''
sf=File('/bin/sh')
df=File('.')
ff=File('./LICENSE')
print(sf.type, df.type, ff.type)


#Example 1: Find most recently modified file
files = File('.').files
files.sort(key = lambda f:f.mtime)
print(files[-1], files)

    
     





