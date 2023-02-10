#!/usr/bin/python3
import shutil
import sys
import os
import time
import datetime
from pathlib import Path

def check_python_version(min_v):
    try:
        version_text = sys.version
        version_s = version_text.split(' ')[0]
        v_segs = version_s.split('.') 
        v_s = v_segs[0] + '.' + v_segs[1]
        v = float(v_s)
        #print(v)
        if v < min_v:
            print('require python version', min_v, 'current', v)
            print("let 'python3' on your machine point to a higher version binary, or directly modify the first line of 'shuiguolao.py'.")
            sys.exit(-1)
    except Exception as e:
        print(e)
        print('can not probe python version, but continue..')

def get_python_bin():
    with open(__file__) as this_f:
        firstline = this_f.readline()
        python_bin = firstline.split('!')[-1]
        python_bin = python_bin.strip()
    return python_bin

try:
    check_python_version(3.6)
    exec_py_p = Path(__file__).resolve()
    exec_dir_p = exec_py_p.parent.parent
    #print(exec_py_p)
    cfg_history_p = exec_dir_p.joinpath('history')
    sample_p = exec_dir_p.joinpath('sample.py')
    sgl_vimrc_p = exec_dir_p.joinpath('shuiguolao.vimrc')
    #print(cfg_history_p.as_posix())
    #print(sample_p.as_posix())

    curr_time = int(time.time())
    xf_name = f'{curr_time}.py'
    xf_p = cfg_history_p.joinpath(xf_name)
    xf_path = xf_p.as_posix()
    #cmd_args = ['vim', xf_path];
    #cmd_s = ''.join(cmd_args)

    #copy sample file to xf, inserting 'created time'
    #we can't perform a simple replacement but walk line by line to make safe
    '''
    xf = open(xf_p, 'w')
    with open(sample_p, 'r') as sample_f:
        sample_lines = sample_f.readlines()
        scope = -1 
        for l in range(len(sample_lines)):
            line = sample_lines[l]
            if line.find('###shuiguolao') != -1 or line.find('###DO NOT EDIT') !=-1:
                scope += 1
            if scope > 0:
                break
            if scope == 0 and line.find('created at') != -1:
                now_s = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())
                #print('now_s', now_s)
                good_line = line.replace('xxxx/xx/xx xx:xx:xx', now_s)
                sample_lines[l] = good_line
                break
    xf.writelines(sample_lines)
    xf.close()
    '''

    #TODO execute from other commands
    #cmd_s = f'vim -u NONE -S ./vimrc {xf_path}'
    sgl_vimrc_path = sgl_vimrc_p.as_posix()
    #print(sgl_vimrc_path)
    #cmd_s = f'vim  -S {sgl_vimrc_path} {xf_path}'
    cmd_s = f'vim   -S {sgl_vimrc_path} pshuiguolao'
    #print(cmd_s)
    os.system(cmd_s)
    #proc = subprocess.Popen(cmd_args, stdout = subprocess.PIPE, stderr = subprocess.PIPE, bufsize=64*1024, shell=True)

    '''
    if not xf_p.exists():
        print('input nothing') 
        sys.exit(0)
    '''

    #drop file if no user code
    '''
    with open(xf_p, 'r') as xf:
        xf_lines = xf.readlines()
        
        in_user_code = False
        no_user_code = True
        for l in range(len(xf_lines)):
            line = xf_lines[l]
            if(line.find('WRITE YOUR CODE BELOW') != -1):
                in_user_code = True
                continue
            if in_user_code:
                s = line.strip().replace('\t', '')
                if s:
                    no_user_code = False
                    break
    if no_user_code:
        print(f"empty input, drop file '{xf_p.name}' ..")
        os.remove(xf_p)
    else:
        python_bin = get_python_bin()
        run_py_cmd = f'{python_bin} {xf_path}'
        #comment this two lines, for currently NO 'run-on-quit'
        #print(run_py_cmd)
        #os.system(run_py_cmd)
    '''

except Exception as e:
    traceback.print_exc()
    print('quit')







