import os
import pwd
import grp
from utils import *
from error import *
'''
主组：

也叫初始组，是用户登录系统时的组，规则如下：
创建新用户时，若未明确指定该用户所属的主组，会默认创建一个与用户名相同的组，作为该用户的主组
用户创建文件时，文件的所属权限组就是当前用户的主组
使用useradd命令时用-g参数可以指定主组，则不会默认创建同名的主组
用户有且只能所属一个主组
用户的主组不能被删除
用户不能直接被移出主组，但可以更换主组
用户被删除时它的主组若没有其他所属用户，则会自动删除该主组
附加组
登录后可切换的其他组，规则如下：
使用useradd命令时用-G参数可以指定附加组
用户可以所属零个或多个附加组
用户的附加组和主组可相同
附加组可以直接被删除而无需关心是否所属于用户
附加组可以新增和移除任意个所属用户
用户被删除时所属附属组不会受影响
'''

#useradd userdel usermod
#groupadd groupdel groupmod

class User():
    has_setters = ['uid', 'group']
    use_setters = False





            
    #user shouldn't construct one by hand ?
    def __init__(self, name, **kw):
        self.name =name
        self.kw = kw
        self._entry = None

    def save(self):
        '''
        Save a new constructed user to database.
        '''
        kw = self.kw
        name = self.name
        passwd = kw['passwd'] if 'passwd' in kw else None
        home = kw['home'] if 'home' in kw else ('/home/'+name)
        shell = kw['shell'] if 'shell' in kw else '/bin/sh'
        #groups = kw['groups'] if 'groups' in kw else None
        uid = kw['uid'] if 'uid' in kw else None
        #g = kw['g'] if 'g' in kw else None

        arglist = ['sudo', 'useradd', name]
        if uid:
            arglist += ['-u', str(uid)]
        if shell:
            arglist += ['-s', shell]
        if home:
            arglist += ['-d', home]
        if UserGroup(name).exists():
            print(f'Note! group {name} already exists')
            arglist += ['-g', name]
        #print(arglist)
        code = sh_command(arglist)
        if code != 0:
            raise Exception(f"create user {name} failed")
        self.drop_cache()

    def exists(self):
        '''
        : If this user exists.
        '''
        try:
            abc = self.entry
        except :
            return False
        return True


















    @property
    def uid(self):
        ''': int
        '''
        return self.entry.pw_uid
    @property
    def gid(self):
        '''
        @getter int
        @setter Accept a gid and set user's primary group
        '''
        return self.entry.pw_gid
    @property
    def passwd(self):
        ''': This field was abandoned by linux.
        '''
        return self.entry.pw_passwd
    @property
    def shell(self):
        ''': str
        '''
        return self.entry.pw_shell
    @property
    def home(self):
        ''': str
        '''
        return self.entry.pw_dir






    @property
    def group(self):
        '''
        @getter Return the primary group of this user. Their relationship is built on gid.
        @setter Accept a UserGroup object and set user's primary group.
        '''
        return os.usergroups.get(self.gid)

    @staticmethod
    def setters(on=None):
        '''
        : Turn on/off setters. Off when class User initialized.
        : When @on None, do nothing but return all setters avaliable.
        '''
        if on == None:
            return User.has_setters
        elif on:
            User.use_setters = True
        else:
            User.use_setters = False
            







    @group.setter
    def group(self, g):
        param_type_check(g, [UserGroup])
        self.setg(g.name)

    @gid.setter
    def gid(self, g):
        param_type_check(g, [int])
        self.setg(g)

    @property
    def secondary_groups(self):
        '''
        : List<UserGroup>
        : Collect all groups containing this user, return as a list.
        : Such group is called secondary or supplementary group on linux.
        '''
        lst = []
        for g in os.usergroups.list:
            if self.name in g.members:
                lst.append(g)
        return lst

    @secondary_groups.setter
    def secondary_groups(self, lst):
        '''
        : Set secondary groups for a user.
        : Equalivant to usermod -G [lst]
        @param lst List
         the list element can be str or User object, or mixed.
        '''
        G = []
        for g in lst:
            param_type_check(g, [str,  User])
            gname = g.name if type(g) == User else g
            G.append(gname) 
        G = ','.join(G)
        sh_command(['usermod', '-G', G])

    def join(self, g):
        '''
        : Join in group 'g', and the latter will become a so-called secondary 
        : or supplementary group for this user.
        @param g UserGroup
        '''
        return g.add(self)

    def quit(self, g):
        '''
        : Quit from group 'g' which is so-called a secondary or supplementary
        : group for this user.
        @param g UserGroup
        '''
        return g.remove(self) 


class UserGroup():
    def __init__(self, name, **kw):
        self.kw = kw
        self.name=name
        self._entry = None

    def exists(self):
        '''
        : If this usergroup exists
        '''
        try:
            abc = self.entry
        except:
            return False
        return True

    def save(self):
        '''
        Save a new constructed user to database.
        '''
        code = sh_command(['sudo', 'groupadd', self.name])
        if code != 0:
            raise Exception(f"Create usergroup '{gname}' failed!")


















    @property
    def gid(self):
        '''
        : int
        '''
        return self.entry.gr_gid

    @property
    def members(self):
        '''
        : list<str>
        '''
        return self.entry.gr_mem

    @property
    def passwd(self):
        '''
        : this field has been abandoned by linux
        '''
        return self.entry.gr_passwd

    @property
    def users(self):
        '''
        : Return a list of users that join() this usergroup.
        '''
        lst = []
        for u in self.members:
            user = os.users.get(u)
            lst.append(user)
        return lst

    def remove(self, u):
        '''
        : Equalivant to u.quit(self)
        @param u User|str|int
         can be a User object, user name, or uid
        '''
        param_type_check(u, [int, str, User])
        if type(u) == int:
            uname = os.users.get(u)
        elif type(u) == str:
            uname = u
        elif type(u) == User:
            uname = u.name
        else:
            assert False

        '''
        members = self.members
        members.remove(uname)
        G_s = ','.join(members)
        '''
        code = sh_command(['sudo', 'gpasswd', '-d', uname, self.name])
        self.drop_cache()
        return True if code == 0 else False
            
    def add(self, u):
        '''
        : Equalivant to u.join(self)
        @param u User|str|int
         can be a User object, user name, or uid
        '''
        param_type_check(u, [int, str, User])
        if type(u) == int:
            uname = os.users.get(u)
        elif type(u) == str:
            uname = u
        elif type(u) == User:
            uname = u.name
        else:
            assert False

        #必须是-aG,不能是-Ga
        #this line works, but comment to use another command gpass
        #code = sh_command(['sudo', 'usermod', uname, '-aG', self.name])    
        code = sh_command(['sudo', 'gpasswd', '-a', uname, self.name])    
        self.drop_cache()
        return True if code == 0 else False







class UserGroupTable():
    def __init__(self):
        pass

    @property 
    def list(self):
        '''
        : List<UserGroup>
        @getter all usergroups on this computer.
        '''
        arr = grp.getgrall()
        lst = []
        for el in arr:
            g = UserGroup(el.gr_name)
            lst.append(g)
        return lst

    def get(self, g):
        '''
        : Find a usergroup by gid or group name.
        @param g int|str
        @return UserGroup|None
        '''
        param_type_check(g, [int, str])
        if type(g) == int:
            group = UserGroup(None, gid=g)
        elif type(g) == str:
            group = UserGroup(g)
        else:
            raise TypeError(g)
        return group if group.exists() else None

    def add(self, name, **kw):
        '''
        : Create a new usergroup named @name.
        @param name str
        @return UserGroup
        '''
        g = UserGroup(name, **kw)
        if g.exists():
            if 'exists_ok' in kw and kw['exists_ok']:
                return g
        try:
            g.save()
        except Exception as e:
            print(e)
            return None
        return g

    def remove(self, g):
        '''
        : Remove a usergroup.
        @param g UserGroup|str
         can be an UserGroup object or group name.
        '''
        param_type_check(g, [UserGroup, str])
        gname = g.name if type(g) == UserGroup else g
        code = sh_command(['sudo', 'groupdel', gname])
        return True if code == 0 else False

class UserTable():
    @property
    def list(self):
        '''
        : List<User>
        @getter all users on this computer.
        '''
        arr=pwd.getpwall()
        users = []
        for el in arr:
            user = User(el.pw_name)
            users.append(user)
        return users

    def add(self, name, **kw):
        '''
        : Create a new user named @name.
        @param name str
        @return User
        '''
        user = User(name, **kw)
        if user.exists():
            if 'exists_ok' in kw and kw['exists_ok']:
                return user
        try:
            user.save()
        except Exception as e:
            print(e)
            return None
        return user
        
    def remove(self, u, **kw):
        '''
        : Remove a user.
        @param u User|str
         can be an User object or user name.
        '''
        param_type_check(u, [str, User])
        force = kw['force'] if 'force' in kw else False
        rmfs = kw['rmfs'] if 'rmfs' in kw else False
        uname = u if type(u) == str else u.name
        arglist = ['sudo', 'userdel', uname]
        if rmfs:
            arglist += ['-r']
        if force:
            arglist += ['-f']
        code = sh_command(arglist)
        return None if code != 0 else True

    def get(self, u):
        '''
        : Find a user by uid or user name.
        @param u int|str
        @return User|None
        '''
        param_type_check(u, [str,int])
        uname = None
        if type(u) == int:
            user = User(None, gid=u)
        elif type(u) == str:
            user = User(u)
        else:
            raise TypeError(u)
        return user if user.exists() else None


os.users = UserTable()
os.usergroups = UserGroupTable()







        


