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
#created at 2023/02/20 17:00:38             #
####DO NOT EDIT LINES ABOVE!!################
####WRITE YOUR CODE BELOW####################

# Create a new user

uxx = User('xx')
uxx.save()
uxx

# Or like this:
os.users.add('yy')

# Find a user
os.users.get('xx')
# Or like this:
uyy = User('yy')
uyy

# The way for creating and finding UserGroup is similar:
usbfs = UserGroup('usbfs')
usbfs.save()
UserGroup('usbfs')
# Or like this:
vbox = os.usergroups.add('vboxusers')
os.usergroups.get('vboxusers')

# Let current user join in usbfs
import getpass
myname = getpass.getuser()
me = User(myname)
me.join(usbfs)
usbfs.members
# Then quit
me.quit(usbfs)
usbfs.members

# Let all users join in vboxusers
for u in os.users.list:
    u.join(vbox)

vbox.members
# Then quit
for u in os.users.list:
    u.quit(vbox)

vbox.members

# Clear our footprint 
os.usergroups.remove(usbfs)
os.usergroups.remove(vbox)
os.users.remove(uxx)
os.users.remove(uyy)










