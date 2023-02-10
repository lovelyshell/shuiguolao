# -*- coding: utf8 -*-
#目前提供只读的接口，所有修改文件的api都在测试，修改还涉及到cache的问题

import sys
import os
import time
import traceback
import datetime
import tempfile
import stat
from pathlib import Path
import shutil

##NODOC
#pass argument to operation system directly, shell syntax not supported
def run_command(argv):
    import subprocess
    subprocess.Popen(argv, shell=False) 


##NODOC
def rawset(it, key, value):
    object.__setattr__(it, key, value)

##NODOC
def rawget(it, key):
    try:
        value =  object.__getattribute__(it, key)
        return value
    except Exception as e:
        print('within rawget:',e)
        print(traceback.format_exc())   #seems print_exc not work here..
        raise

##NODOC
#https://stackoverflow.com/questions/8299386/modifying-a-symlink-in-python/55742015#55742015
#TODO modify, can only modify symbol files
def symlink_to(target, link_name, overwrite=False):
    '''
    Create a symbolic link named link_name pointing to target.
    If link_name exists then FileExistsError is raised, unless overwrite=True.
    When trying to overwrite a directory, IsADirectoryError is raised.
    '''

    if not overwrite:
        os.symlink(target, link_name)
        return

    # os.replace() may fail if files are on different filesystems
    link_dir = os.path.dirname(link_name)

    # Create link to target with temporary filename
    while True:
        temp_link_name = tempfile.mktemp(dir=link_dir)

        # os.* functions mimic as closely as possible system functions
        # The POSIX symlink() returns EEXIST if link_name already exists
        # https://pubs.opengroup.org/onlinepubs/9699919799/functions/symlink.html
        try:
            os.symlink(target, temp_link_name)
            break
        except FileExistsError:
            pass

    # Replace link_name with temp_link_name
    try:
        # Pre-empt os.replace on a directory with a nicer message
        if not os.path.islink(link_name) and os.path.isdir(link_name):
            raise IsADirectoryError(f"Cannot symlink over existing directory: '{link_name}'")
        os.replace(temp_link_name, link_name)
    except:
        if os.path.islink(temp_link_name):
            os.remove(temp_link_name)
        raise

##NODOC
os_eol_dict = {   'mac':'\r', 
            'unix':'\n', 
            'linux':'\n', 
            'osx': '\n',
            'windows':'\r\n'}

##NODOC
def getoseol(osname=None):
    osname = osname.lower()
    eol = os.linesep if osname == None else os_eol_dict[osname]
    return eol

'''
def bytes2str_smart(raw, encodings = None):
    return raw.decode(encoding = 'utf8')
'''

##NODOC
def check_path_exists(pathlike, follow_symlinks=False):
    p = Path(pathlike)
    if p.is_symlink() and not follow_symlinks:
        return True
    else:
        return p.exists()

'''
def check_file_type(f, fn_name):
    fn_key = 'is'+ fn_name
    fn = getattr(File, fn_key) 
    if not fn(f):
        raise TypeError(f'"{f.path}", wrong file type, want {fn_name} ')
'''

##NODOC
def read_check(f, want_type):
    #sys.stderr.write(f'read_check {want_type} called')
    _path = rawget(f, '_p').as_posix()
    if not f.exists():
        raise Exception(f'{_path}, file not exists')

    if f.getFileType() != want_type:
        raise Exception(f'"{_path}", wrong file type, need type {want_type}, met {f.type} ')
         
    #print('read_check',want_type, 'check ok')

##NODOC
def write_check(f, want_type):
    #check exists but a different type
    if f.exists():
        f_type = f.getFileType()
        f_path = rawget(f, '_p')
        if f.getFileType() != want_type:
            raise Exception(f"dare not modify file '{f_path}', it exists but not the type '{want_type}', it is '{f_type}'")

has_follow_symlinks_impl = True
try:
    os.chmod('this_file_should_not_exit', 0o000, follow_symlinks=False)
except Exception as e:
    if type(e) == NotImplementedError:
        has_follow_symlinks_impl = False
    else:
        pass
        

class File():
    TYPE_DIR = 'directory'
    TYPE_CHR = 'character'
    TYPE_BLK = 'block'
    TYPE_REG = 'file'
    TYPE_FIFO = 'fifo'
    TYPE_SOCK = 'sockect'
    TYPE_PORT = 'port'
    TYPE_WHT = 'whiteout'
    TYPE_LINK = 'link'
    '''
    TypeNames = {TYPE_DIR:'directory', TYPE_CHR:'character', TYPE_BLK:'block',
            TYPE_REG:'file', TYPE_FIFO:'fifo', TYPE_SOCK:'sockect', 
            TYPE_PORT:'port', TYPE_WHT:'whiteout', TYPE_LINK:'link'}
    '''
    '''
    stat_fields = ['ino', 'gid', 'uid', 'mode', 'size', 'atime', 'ctime','mtime', 'dev', 'nlink', 'atime_ns', 'mtime_ns', 'ctime_ns',
                    'blocks', 'blksize', 'rdev', 'flags', 
                    'gen', 'birthtime', 'fstype', 'rsize', 'creator', 'type',
                    'file_attributes', 'reparse_tag' ]
    '''
    #所有的标志都是你在限制自己的权限，防止自己误操作。
    #不需要读时不读，不需要写时不写，不需要触碰到已存在内容时不碰。
    #另一组是功能，在写时，如果不存在则创建，如果存在则截断
    #这其实可以通过手动调用函数来实现
    #不考虑追加模式
    #def __init__(self, path, rw='rw', w_ex='ac', w_pos='', mode=511):
    ##NODOC
    def __init__(self, path, rw='rw'):
        object.__setattr__(self, '__lock_dict__', 0)
        object.__setattr__(self, '__is_destroy', False)
        org_p = Path(path)  #orgiinal p
        if  org_p.is_symlink():
            #we don't follow symbol link 
            p = org_p.parent.resolve().joinpath(org_p.name)  
        else:
            p = org_p.resolve()
        self._org_p = org_p
        self._p = p
        #self.p2 = os.path.normpath(path)
        #abs_p = p.resolve()
        #rel_p = abs_p.relative_to('.')
        #self.path = p.as_posix()
        #self.rpath = rel_p.as_posix()

        self._stat = None
        self._parent = None
        self._type = None

        #for directory type file
        self._target = None
        self._dict = None
        self._lines = None
        self._text = None
        self._raw = None
        self._link = None
        self.rw = rw
        #self.w_mode = mode
        #self.w_ex = w_ex

        object.__setattr__(self, '__lock_dict__', 1)

    ##NODOC
    def drop_data(self):
        self._dict = None

        self._lines = None
        self._raw = None
        self._text = None

        self._link = None
        self._target = None

    ##NODOC
    def drop_stat(self):
        self._stat = None

    @property
    def text(self):
        ''': str
        @getter readtext()
        : Avaliable when isFile()
        '''
        return self.readtext()

    @property
    def lines(self):
        ''': List[str]
        @getter readlines()
        : Avaliable when isFile()
        '''
        return self.readlines()

    @property
    def raw(self):
        ''': bytes
        @getter readraw()
        : Avaliable when isFile()
        '''
        return self.readraw()

    @property
    def link(self):
        ''': str
        @getter this.readlink()
        : Avaliable when isLink()
        '''
        return self.readlink()

    def writelink(self, target):
        '''
        :Make this symbol link point to target.
        @param target str
        '''
        write_check(self, 'link')
        symlink_to(target, self.path, overwrite = True)
        self._link = to

    def readlink(self):
        '''Return the path to which the symbolic link points.
        @return str
        '''
        try:
            #check_file_type(self, 'symlink')
            #print('read link called')
            if self._link == None:
                link = os.readlink(self.p)
                self._link = link
            return self._link
        except Exception as e:
            print('read link failed:', e)
            raise

    def readraw(self):
        '''Read and return the file's content as is.
        @return bytes
        : Avaliable when isFile()
        '''
        read_check(self, 'file')
        if 'r' not in self.rw:
            raise Exception(f'argument {self.rw} but attemp to read on it')
        if not self._raw:
            with open(self.p, mode='rb') as f:
                _bytes = f.read()
                _raw = bytearray(_bytes)
                self._raw = _raw
        return self._raw

    def writeraw(self, raw):
        '''Write bytes into this file as is.
        @param raw bytes
        '''
        write_check(self, 'file')
        if 'w' not in self.rw:
            raise Exception(f'argument {self.rw} but attemp to write on it')
        p = self.p
        _bytes = bytes(raw)
        self.drop_data()
        with open(self.p,  mode='wb') as f:
            f.write(_bytes)
        self._raw = raw

    def readtext(self, encoding='utf-8'):
        '''Read and return the decoded contents of file as a string.
        :Equivalent to this.readraw().decode(encoding)
        @param encoding str 
         The name of encoding used to decode file's content into string.
        @return str
        '''
        if self._text == None:
            raw = self.readraw()
            text = raw.decode(encoding=encoding)
            self._text = text
        return self._text

    def writetext(self, text, encoding='utf-8'):
        '''Encode text and write to file.
        :Equivalent to this.writeraw(text.encode(encoding))
        @param text str
        @param encoding str 
         The name of encoding used to encode string into file's bytes. 
        '''
        _bytes = text.encode(encoding=encoding)
        self.writeraw(_bytes)
        self._text = text   #recovery this field for writeraw drop it

    #https://docs.python.org/3/library/functions.html#open
    def readlines(self,  eol=None, encoding='utf-8'):
        '''
        :Read and return a list of lines from the file. 
        :Equivalent to this.readtext(encoding).split(eol)
        @param eol str 
         The "end of line". specify the line separator to split text to lines.
         When None, use the OS line separator.
        @return List[str]
        '''
        #assert eol != '', 'empty eol not allowed'
        read_check(self,'file')
        if eol == None:
            eol = os.linesep
        if self._lines == None:
            text = self.readtext(encoding=encoding)
            lines = text.split(eol)
            self._lines = lines
        return self._lines.copy()

    def writelines(self, lines, eol=None, encoding='utf-8'):
        '''
        :Write a list of lines to the file. 
        :Equivalent to this.writetext( eol.join(lines) , encoding )
        @param lines List[str]
        @param eol str 
         The "end of line". Specify the line separator added at the line end on write.
         When None, use the OS line separator.
        '''
        write_check(self, 'file')
        #assert eol != '', 'empty eol not allowed'
        p = self.p
        if eol == None:
            eol = os.linesep
        text = eol.join(lines)     
        self.writetext(text)
        self._lines = lines     #recovery this field for writeraw drop it

    @property
    def org_path(self):
        ''': str 
        : The original path, got from File's constructor.
        '''
        return self._org_p.as_posix()

    @property
    def org_p(self):
        ''': pathlib.Path
        : The original path, got from File's constructor.
        '''
        return self._org_p

    @property
    def p(self):
        ''' pathlib.Path
        Path object, representing the absolute path of this file.
        '''
        return self._p

    @property
    def path(self):
        ''': str
        The absolute path of this file.
        '''
        return self.p.as_posix()

    @property
    def name(self):
        ''': str
        : file name
        '''
        return self.p.name

    @property
    def target(self):
        ''': File
        : A File object, representing the final target of the symbol link.
        : Available when isLink().
        '''
        if self._target == None:
            target = File(self.link)
            self._target = target
        return self._target

    ##NODOC
    def readStat(self):
        if not self._stat:
            self._stat = os.stat(self.p, follow_symlinks=False)
        return self._stat

    @property
    def stat(self):
        ''': os.stat_result
        : Obtained from os.stat().
        : You won't use it usually, because File library played some tricks so that all its attributes can be indexed directly on File.
        like:
        this.size       ==> this.stat.st_size
        this.atime      ==> this.stat.st_atime
        ...
        this.uid        ==> this.stat.st_uid
        '''
        return self.readStat()

    '''
    def __getattribute__(self, key):
        if rawget(self, '__is_destroy'):
            raise Exception(f'attemp to access a destroyed File object at ({key})')
        #print('getattribute found it', key)
        value = rawget(self, key)
        #print(f'__getattribute__ got {key}', value)
        return value
    '''

    ##NODOC
    def __getattr__(self, key):
        #capture 'type' before self.stat capture it
        #TODO can not find c name
        st_key = 'st_'+key
        #if st_key in File.TypeNames.stat_fields:
        try:
            got = getattr(self.stat, st_key, None)
            return got 
        except:
            _path = rawget(self, '_p').as_posix()
            raise AttributeError(f"'{_path}', 'File' object has no attribute or getter named '{key}'")

    ##NODOC
    def __setattr__(self, key, value):
        #print('setattr===>' , object.__getattribute__(self, '__is_destroy'), object.__getattribute__(self, '__dict__'))
        if rawget(self, '__is_destroy'):
            raise Exception(f'attemp to write on a destroyed File object, ({key}=>{value})')
        #print(f"attempt to set '{key}'-> {value}")
        if key=='mode':
            self.chmod(value)
        elif key == 'uid':
            self.chown(uid=value)
        elif key == 'gid':
            self.chown(gid=value)
        elif key == 'raw':
            self.writeraw(value)
        elif key == 'lines':
            self.writelines(value)
        elif key == 'text':
            self.writetext(value)
        elif key == 'link':
            self.writelink(value)
        #all setters checked, it should be an attribute?
        elif key in self.__dict__ or  not self.__lock_dict__:
            rawset(self, key, value)
        else:
            raise AttributeError(f"'File' object has no attribute or setter named '{key}'")

    ##NODOC
    def getFileType(self):
        if self._type:
            return f._type
        if not self.exists():
            return None
        m = self.readStat().st_mode
        if stat.S_ISDIR(m):
            t = File.TYPE_DIR
        elif stat.S_ISREG(m):
            t = File.TYPE_REG
        elif stat.S_ISCHR(m):
            t = File.TYPE_CHR
        elif stat.S_ISBLK(m):
            t = File.TYPE_BLK
        elif stat.S_ISFIFO(m):
            t = File.TYPE_FIFO
        elif stat.S_ISLNK(m):
            t = File.TYPE_LINK
        elif stat.S_ISSOCK(m):
            t = File.TYPE_SOCK
        elif stat.S_ISDOOR(m):
            t = File.TYPE_DOOR
        elif stat.S_ISPORT(m):
            t = File.TYPE_PORT
        elif stat.S_ISWHT(m):
            t = File.TYPE_WHT
        else:
            assert False, 'unspecified file type when parsing'
        #return File.TypeNames[t]
        return t

    @property
    def type(self):
        ''': str
        : file type. one of the following:
          'directory' 'character' 'block' 'file' 'fifo' 'sockect' 'port' 'whiteout' 'link'
        '''
        return self.getFileType()

    ##NODOC
    def invalidate(self):
        self._stat = None
        self._dict = None

    @property
    def dict(self):
        '''
        : Dict[str, File]
        : Collect all files under the directory, file name as key, corresponding File object as value.
        : Available when isDir().
        '''
        read_check(self, 'directory')
        p = self.p
        if self._dict == None:
            _dict = self._dict = dict()
            for sub_p in self.p.iterdir():
                sub_f = File(sub_p)
                _dict[sub_p.name] = sub_f
        return self._dict

    #类型: list(File) File对象数组，只能对目录类型的File访问

    @property
    def files(self):
        '''alias of "children"
        '''
        return self.children

    @property
    def children(self):
        '''
        : List[File]
        : An array of all File objects under the directory, equivalent to this.dict.values().
        : Available when isDir().
        '''
        return self.dict.values()


    @property
    def list(self):
        ''': List[str]
        : An array of all file names under the directory, equivalent to this.dict.keys()
        : Available when isDir()
        '''
        return self.dict.keys()

    @property
    def parent(self):
        ''': File 
        : A File object representing the parent directory.
        '''
        if not self._parent:
            parent = File(self.p.parent)
            self._parent = parent
        return self._parent

    def isDir(self, follow_symlinks=False):
        '''
        : If this is a directory.
        '''
        if self.isLink() and not follow_symlinks:
            return False
        return self.p.is_dir()

    def isFile(self, follow_symlinks=False):
        '''
        : If this is a regular file.
        '''
        if self.isLink() and not follow_symlinks:
            return False
        return self.p.is_file()

    def isLink(self):
        '''
        : If this is a symbol link.
        '''
        return self.p.is_symlink()

    def exists(self, follow_symlinks=False):
        '''
        : If this file exists.
        :return: boolean
        '''
        return check_path_exists(self.p, follow_symlinks=follow_symlinks)

    class RInfo():
        '''
        : File library use this structure to pass recursive context infomation 
          to user handler function as an argument. 
        : Attributes:
            .depth int
            Current recursive depth
        '''

        def __init__(self, depth):
            self.depth = depth
            pass

    ##NODOC
    #staticmethod
    def __R(df, fn, cur_depth, max_depth):
        for f in df.files:
            ret = fn(f, File.RInfo(cur_depth) )
            if ret == False:
                continue
            if f.isDir() and cur_depth != max_depth:
                File.__R(f, fn, cur_depth + 1, max_depth)

    @staticmethod
    def R(pathlike, fn, max_depth = 0xfffffffff, skip_zero=True):
        '''
        :Recursively walk through the directory 'pathlike', and perform operaton 'fn' on each node.
        :param: pathlike str|path.Path|File
         Path-like object, specify the directory to recurse into
        :param: fn function
         User function to execute on each node, which should be like:
         def foo(f:File, rinfo:File.RInfo)
         Argument 'f' indicates the File object of the node. 
         Argument 'rinfo' takes other travasal context infomation.
         A False return of 'fn' will tell R not recurse into that node.
        :param: max_depth int
         Maxium depth allowed to recurse into. Node 'pathlike' at 0, its 
         subfiles at 1, and so on. Function 'fn' is executed on one node before recursing into it.
        :param: skip_zero boolean
         Skip the 'fn' operation on node 'pathlike', whose depth is zero.
        '''
        if type(pathlike) == str or type(pathlike) == Path:
            f = File(pathlike)
        elif type(pathlike) == File:
            f = pathlike
        else:
            raise TypeError('@pathlike, invalid argument type, shall be str or File')
        #TODO remove 
        if not f.isDir():
            raise TypeError(f'{f.path} is not a directory')
            
        if not skip_zero:
            fn(f, File.RInfo(0))
        File.__R(f, fn, 1, max_depth)
        
    ##NODOC
    def follow_symlinks_impl_check(self, follow_symlinks, impl_error_level):
        if not follow_symlinks and not has_follow_symlinks_impl:
            if self.p.is_symlink():
                e = NotImplementedError(f"skip '{self.name}', for follow_symlinks not implemented on this platform")
                lvl = impl_error_level
                if lvl == 2:
                    raise e
                elif lvl == 1:
                    sys.stderr.write(str(e))
                elif lvl == 0:
                    pass
                else:
                    raise Exception('invalid value for impl_error_level')
                return False
            else:
                return True
        else:
            return True
        
    ##NODOC
    def chmod(self, mode, follow_symlinks=False, impl_error_level=1):
        print(f'you called chmod({mode})',)
        ok = self.follow_symlinks_impl_check(follow_symlinks, impl_error_level)
        if not ok:
            return
        os.chmod(self.path, mode, follow_symlinks=True)
        self._stat = None
        '''
        if not follow_symlinks and not has_follow_symlinks_impl:
            if self.p.is_symlink():
                e = NotImplementedError(f"chmod() skip '{self.name}', because follow_symlinks not implemented on this platform")
                lvl = impl_error_level
                if lvl == 2:
                    raise e
                elif lvl == 1:
                    sys.stderr.write(str(e))
                elif lvl == 0:
                    pass
                else:
                    raise Exception('invalid value for impl_error_level')
                return
            else:
                pass
        '''


    ##NODOC
    def chown(self, uid=-1, gid=-1, follow_symlinks=False):
        os.chown(self.path, uid=uid, gid=gid, follow_symlinks=follow_symlinks)
        self._stat = None
        #object.__setattr__(self, '_stat', None)
    
    ##NODOC
    def destroy(self):
        object.__setattr__(self, '__is_destroy', True)


    ##NODOC
    @staticmethod
    def Rename(f, new_name):
        new_p = f.p.parent.joinpath(new_name)
        f.p.rename(new_p)  
        new_f = File(new_p)
        #update parent node only if exists
        _parent = f._parent
        if _parent:
            if _parent._dict:
                del _parent.dict[f.name]
                _parent._dict[new_name] = new_f
                _parent._stat = None
        f.destroy()
        
        
##NODOC
class SimpleTrash():
    def __init__(self, path):
        p = Path(path)
        p = Path(p.expanduser())
        p.mkdir(0o777, False, True)
        self.p = p
        
    def add(self, filepath):
        fp = Path(filepath) 
        print(f'Trash add [{fp.as_posix()}]')

        dest = self.p.as_posix()
        for i in range(0,2):
            try:
                shutil.move(fp.as_posix(), dest)
                break
            except Exception as e:
                if i == 0:
                    #shutil很垃圾，只抛出个Error类型的错误，
                    #那就当作是重名，修正一次，不行算了
                    dest_p = self.p.joinpath(fp.name)
                    dest = dest_p.as_posix() + str(time.time())
                    continue
                else:
                    raise e
                    
##NODOC
Trash = SimpleTrash('~/.shuiguolao-trash')








