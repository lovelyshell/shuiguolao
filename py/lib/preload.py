import sys
import os
import time
from pathlib import Path
from functools import cmp_to_key
from User import *
from utils import *

from File import *
from Re import *
#from File import File,  Trash
cwd = File('.')

class SysCurrent():
    def __init__(self):
        self._dir = None
        self._user = None

    @property
    def dir(self):
        if not self._dir:
            self._dir = File('.') 
        return self._dir

    @property
    def user(self):
        import getpass
        if not self._user:
            u = getpass.getuser()
            self._user = os.users.get(u)
        return self._user

current = SysCurrent()

'''
SGL_LOCAL_LIB = Path(Path(__file__).parent.absolute())
SGL_LOCAL = Path(SGL_LOCAL_LIB.parent)
'''
try:
    SGL_ROOT = Path(os.getenv('SGL_ROOT'))
    Trash = SimpleTrash(SGL_ROOT.joinpath('.shuiguolao-trash'))
except:
    perror('Trash initialization skipped')

#py_run_timestamp_s = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())
sgl_run_timestamp_s = time.strftime('%H:%M:%S', time.localtime())
