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
    #user shouldn't construct one by hand ?
    def __init__(self):
        self.name =None
        self.uid=None
        self._entry = None

    def drop_cache(self):
        self._entry = None

    @property
    def entry(self):
        if not self._entry:
            self._entry = pwd.getpwnam(self.name)
        return self._entry

    @property
    def gid(self):
        return self.entry.pw_gid
    @property
    def passwd(self):
        return self.entry.pw_passwd
    @property
    def shell(self):
        return self.entry.pw_shell
    @property
    def home(self):
        return self.entry.pw_dir

    @staticmethod
    def from_pw(el):
        u = User()
        u.name=el.pw_name 
        u.uid=el.pw_uid 
        u._entry = el
        return u

    def __repr__(self):
        return f'User: {self.name} {self.uid} {self.home} {self.shell} {self.passwd}'

    @property
    def group(self):
        return os.usergroups.get(self.gid)

    @group.setter
    def group(self, g):
        param_type_check(g, [UserGroup])
        sh_command(['sudo', 'usermod', '-g', g.name, self.name]) 
        self.drop_cache()

    @property
    def secondary_groups(self):
        lst = []
        for g in os.usergroups.list:
            if self.name in g.members:
                lst.append(g)
        return lst

    @secondary_groups.setter
    def secondary_groups(self, lst):
        G = []
        for g in lst:
            param_type_check(g, [str,  User])
            gname = g.name if type(g) == User else g
            G.append(gname) 
        G = ','.join(G)
        sh_command(['usermod', '-G', G])

class UserGroup():
    def __init__(self):
        self.name=None
        self.gid=None
        self._gr_entry = None

    @property
    def gr_entry(self):
        if not self._gr_entry:
            self._gr_entry = grp.getgrgid(self.gid)
        return self._gr_entry

    def drop_cache(self):
        self._gr_entry = None

    @property
    def members(self):
        return self.gr_entry.gr_mem

    @property
    def passwd(self):
        return self.gr_entry.gr_passwd

    @property
    def users(self):
        lst = []
        for u in self.members:
            user = os.users.get(u)
            lst.append(user)
        return lst

    @staticmethod
    def from_grp(el):
        g = UserGroup()
        g._gr_entry = el
        g.name = el.gr_name
        g.gid = el.gr_gid
        return g

    def remove(self, u):
        param_type_check(u, [int, str, User])
        if type(u) == int:
            uname = os.users.get(u)
        elif type(u) == str:
            uname = u
        elif type(u) == User:
            uname = u.name
        else:
            assert False

        members = self.members
        members.remove(uname)
        G_s = ','.join(self.members)
        code = sh_command(['sudo', 'usermod', uname, '-G', G_s])
        self.drop_cache()
        return True if code == 0 else False
            
    def add(self, u):
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
        code = sh_command(['sudo', 'usermod', uname, '-aG', self.name])    
        self.drop_cache()
        return True if code == 0 else False

    def __repr__(self):
        g = self
        s= f"UserGroup: {g.name} {g.gid} {g.members} {g.passwd}"
        return s

class UserGroupTable():
    def __init__(self):
        pass

    @property 
    def list(self):
        arr = grp.getgrall()
        lst = []
        for el in arr:
            g = UserGroup.from_grp(el)
            lst.append(g)
        return lst

    def get(self, g):
        param_type_check(g, [int, str])
        if type(g) == int:
            fn = grp.getgrgid
        elif type(g) == str:
            fn = grp.getgrnam
        else:
            raise TypeError(g)
        try:
            el = fn(g)
            ret = UserGroup.from_grp(el)
        except KeyError:
            ret = None
        return ret

    def add(self, gname, **kw):
        '''
        if self.get(name):
        self.groups.add()
        '''
        if self.get(gname):
            raise ExistError(gname)
        code = sh_command(['sudo', 'groupadd', gname])
        return None if code != 0 else self.get(gname)

    def remove(self, g):
        param_type_check(g, [UserGroup, str])
        gname = g.name if type(g) == UserGroup else g
        code = sh_command(['sudo', 'groupdel', gname])
        return True if code == 0 else False

class UserTable():
    @property
    def list(self):
        arr=pwd.getpwall()
        users = []
        for el in arr:
            user = User.from_pw(el)
            users.append(user)
        return users

    def add(self, name, **kw):
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
        if os.usergroups.get(name):
            print(f'Note! group {name} already exists')
            arglist += ['-g', name]
        #print(arglist)
        code = sh_command(arglist)
        return None if code != 0 else os.users.get(name)
        
    def remove(self, u, **kw):
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
        if type(u) == int:
            item = pwd.getpwuid(u)
        elif type(u) == str:
            item = pwd.getpwnam(u)
        else:
            raise TypeError(u)
        return User.from_pw(item)


os.users = UserTable()
os.usergroups = UserGroupTable()







        


