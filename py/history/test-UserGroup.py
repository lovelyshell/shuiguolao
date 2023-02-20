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
#created at 2023/02/20 00:56:21             #
####DO NOT EDIT LINES ABOVE!!################
####WRITE YOUR CODE BELOW####################

#1
print('>>>List all users:')
for u in os.users.list:
    print(u)


#2
print('>>>List all usergroups:')
for g in os.usergroups.list:
    print(g)

#3
print(">>>Create a user named 'xx'")
uxx=os.users.add('xx', exists_ok=1)
print(uxx)
print(uxx.group)
ucur=current.user
uxx.group = ucur.group
print(">>>Modify xx's primary group :")
print(uxx)
print(uxx.group)
os.users.remove(uxx)
print(uxx)
print('>>>Remove user xx')


#4
print(">>>Create a user named 'yy'")
uyy = os.users.add('yy')
print('>>>Add current user to its group:')
gyy=uyy.group
gyy.add(current.user)
print(gyy)
print(current.user.secondary_groups)
print(">>>Remove this user from gyy:")
gyy.remove(current.user)
print(gyy)
print("remove user 'yy'")
os.users.remove('yy')


print(">>>Create a usergroup named 'zz':")
gzz = os.usergroups.add('zz')
print(gzz)
print(">>>Add current user to it:")
gzz.add(current.user)
print(gzz)
print(">>>Remove group gzz:")
os.usergroups.remove('zz')
print(os.usergroups.get('zz'))







