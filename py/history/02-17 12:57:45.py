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
#created at 2023/02/17 12:57:45             #
####DO NOT EDIT LINES ABOVE!!################
####WRITE YOUR CODE BELOW####################

'''
u = os.users.get('amily')
print(u)
os.users.add('xxx')
print(os.users.get('xxx'))
os.users.remove('xxx')
print(os.users.get('xxx'))
'''
#print(os.usergroups.get('amily'))
print(os.usergroups.list, '\n')



garr = []
for u in os.users.list:
    g = os.usergroups.get(u.gid)
    g.members.append(u)
    garr.append(g)

print(garr)



















