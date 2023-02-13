import sys

from terminal import *


#print(sys.argv)
# run the other file
if sys.argv[1].endswith('.py'): # if .py run right away
    filename = sys.argv[1]
    with open(filename, "rb") as source_file:
        code = compile(source_file.read(), filename, "exec")
    #print('exec', filename)
    del sys.argv[0]
    exec(code, globals(), locals())
