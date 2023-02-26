##NODOC
import subprocess
import sys
#pass argument to operation system directly, shell syntax not supported
def run_command(argv):
    p = subprocess.Popen(argv, shell=False) 
    return p.returncode

def sh_command(argv):
    cmd_s = ''
    for arg in argv:
        arg_s = str(arg)
        cmd_s += f'"{arg_s}" '
    return subprocess.call(cmd_s, shell=True)

def perror(s):
    print(s, file=sys.stderr,flush=True)  
