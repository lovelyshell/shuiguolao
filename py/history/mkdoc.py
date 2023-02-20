#!/usr/bin/shuiguolao
#shuiguolao version: 0.1

from preload import *
################shuiguolao version 0.1#####################
#shortcut:                                                #
#<C-N>    browse history, down                            #
#<C-P>    browse history, up                              #
#<C-S>-r  save and run file in main window                #
#<C-S>-R  save and prepare to run file in main window     #
#<C-S>-N  create a new file                               #
#created at 2023/02/12 01:26:41                           #
###########DO NOT EDIT LINES ABOVE!!#######################
###########WRITE YOUR CODE BELOW###########################

import nodoc
from lxml import html
etree=html.etree

def remove_unlike(html_path):
    parser=etree.HTMLParser(encoding='utf-8')
    html = etree.parse(html_path, parser=parser)
    html_body = html.xpath('/html/body')[0]
    #print(html_body)
    childs = html_body.xpath('child::*')
    for i in range(0,4):
        node = childs[i]
        node.getparent().remove(node)
        print(node)
    #print(etree.SubElement(html_body, 1))
    #print('>>>>',etree.tostring(html_body))
    result = etree.tostring(html, pretty_print=True)  
    f = File('clean-'+html_path)
    f.writeraw(result)
    #print(result)

if __name__ == '__main__':
    for py_path in ['py/lib/File.py', 'py/lib/Re.py']:
        new_p = nodoc.nodoc(py_path)

        run_command(['pydoc3', '-w', new_p.as_posix()])
        html = new_p.stem + '.html'

        remove_unlike(html)






