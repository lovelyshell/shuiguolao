import sys
import os
import time
from pathlib import Path
from functools import cmp_to_key

from File import *
from Re import *
#from File import File,  Trash
cwd = File('.')


#py_run_timestamp_s = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())
sgl_run_timestamp_s = time.strftime('%H:%M:%S', time.localtime())
