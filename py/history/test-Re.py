#!/usr/bin/shuiguolao
#shuiguolao version: 0.1

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
r = CRange('az') +Re.AssertNot( CEnum('hijk'))
m = r.exec('hijklmnopq')
print('字符集排除，输出应改为l:', r.regex, m)










