import sys
import os
import time
from pathlib import Path
from functools import cmp_to_key

exec_py_p = Path(__file__)
exec_dir_p = exec_py_p.parent.resolve()
#exec_parent_p = exec_dir_p.parent
lib_p = exec_dir_p.joinpath('lib')
lib_file_p = lib_p.joinpath('File')
lib_re_p = lib_p.joinpath('Re')
sys.path.append(exec_dir_p.joinpath('history/'))
sys.path.append(lib_file_p.as_posix())
sys.path.append(lib_re_p.as_posix())

from Re import *
from File import *
cwd = File('.')


#py_run_timestamp_s = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())
sgl_run_timestamp_s = time.strftime('%H:%M:%S', time.localtime())
