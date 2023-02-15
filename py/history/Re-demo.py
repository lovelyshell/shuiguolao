#!/usr/bin/shuiguolao
#shuiguolao version: 0.1
print(f'****************run {sgl_run_timestamp_s}************')
################shuiguolao version 0.1#####################
#shortcut:                                                #
#<C-N>    browse history, down                            #
#<C-P>    browse history, up                              #
#<C-S>-r  save and run file in main window                #
#<C-S>-R  save and prepare to run file in main window     #
#<C-S>-N  create a new file                               #
#created at 2023/02/07 02:10:00                           #
###########DO NOT EDIT LINES ABOVE!!#######################
###########WRITE YOUR CODE BELOW###########################

L1 = Re('09azAZ', fmt='crange') | Re('-', fmt='cenum') 
L1 = L1.repeat(1, Re.REPEAT_MAX)

prefix = CSeq('http') + CEnum('s').repeat(0,1) + '://'
print(prefix.regex)

suffix = CSeq('com') | 'org' | 'me' | 'cc'
L2 = (L1 + '.')
r = prefix + (L1 + '.').least(0) + L1.name('jack') + '.' + suffix
#domain.repeat()

m = r.exec('https://doc.magic-digit.com')
print(r.regex, m.group('jack'), m.group())


r = CSeq('.') + (~CEnum('/')).least(1) + '.sw' + CRange('az')
print(r.regex)

pig = CSeq('m') +ReT.ANY + 'j'
r = pig.name('foo') + ReT.ANY.least(0) + (Re.Ref('foo')+'z').name('foo2')
print(r.regex)
m = r.exec('mdj! mdjzj! mdjzjj!')
print( m, m.group('foo'), m.group('foo2'))
