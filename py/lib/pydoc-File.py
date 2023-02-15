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












































































'''
def bytes2str_smart(raw, encodings = None):
    return raw.decode(encoding = 'utf8')
'''









'''
def check_file_type(f, fn_name):
    fn_key = 'is'+ fn_name
    fn = getattr(File, fn_key) 
    if not fn(f):
        raise TypeError(f'"{f.path}", wrong file type, want {fn_name} ')
'''










         











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








































































    @property
    def type(self):
        ''': str
        : file type. one of the following:
          'directory' 'character' 'block' 'file' 'fifo' 'sockect' 'port' 'whiteout' 'link'
        '''
        return self.getFileType()






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
        



















        
































    



















        
        







        


















                    










