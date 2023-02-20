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
#created at 2023/02/19 11:10:36             #
####DO NOT EDIT LINES ABOVE!!################
####WRITE YOUR CODE BELOW####################

for g in os.usergroups.list:
    if 'amily' in g.members:
        print(g)

os.usergroups.remove('xx')
os.users.add('xx')
uxx = os.users.get('xx')
gxx = os.usergroups.get(uxx.gid)
print(gxx)
gxx.remove(uxx)
gxx = os.usergroups.get(uxx.gid)

print(gxx)













