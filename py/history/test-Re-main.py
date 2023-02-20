#!/usr/bin/python3
#shuiguolao version: 0.1
from preload import *
################shuiguolao version 0.1#####################
#shortcut:                                                #
#<C-N>    browse history, down                            #
#<C-P>    browse history, up                              #
#<C-S>-r  save and run file in main window                #
#<C-S>-R  save and (as root) run file in main window      #
#<C-S>-n  create a new file                               #
#created at 2023/02/01 12:05:29                           #
###########DO NOT EDIT LINES ABOVE!!#######################
###########WRITE YOUR CODE BELOW###########################
print('打印基本pattern:')
print(CRange('09').regex)
print(CEnum('hello').regex)

print('测试转义:')
print(CRange('.(').regex)
print(CEnum('.(').regex)

'''
print('测试字符集排除')
r = CRange('az') - CEnum('hijk')
m = r.exec('hijklmnopq')
print('输出期望为l:', r.s, m)
'''


print('测试\b\B')
r = Re.AssertNot(ReT.LINE_BEGIN) + ReT.WORD_BOUNDARY + 'ok'
m = r.exec('okok, oka, ok')
print(r.regex, m)
r = Re('163') + ReT.NOT_WORD_BOUNDARY
m = r.exec('163.com 1634 ')
print(r.regex, m)


print('匹配邮箱')
r = ReT.WORD_BOUNDARY +  ReT.WORD.repeat(1,16) + '@' + (CSeq('163')|'qq'|'sina') + '.com'

text = 'bad:@163.com bad:x@111.com bad:longlonglonglonglonglonglonglonglonglong_name_123@qq.com bad:x@163.com'
m = r.exec(text)
print(r.regex, m)


'''
作业3:提取出文本中所有的英文单词以及数字
熟悉基于Python的服务端应用开发，掌握至少一种Python服务端框架(Flask/Django/FastAPI等),薪水100000
# 输出结果：['Python', 'Python', 'Flask', 'Django', 'FastAPI', '100000']
'''
text = "熟悉基于Python的服务端应用开发，掌握至少一种Python服务端框架(Flask/Django/FastAPI等),薪水100000"
#result = re.findall("[a-zA-Z0-9]+",str)
r = (ReT2.INT | ReT.ALPHA.repeat(1,99999).name('word')).name('all')
matchs = r.exec(text, 'g')
print(r.regex)
for m in matchs:
    print(m, m.group('word'), m.group('all'))

#(CEnum('+-').rep(0,1) + ReT2.INT )

'''
现有字符串“mSurface=Surface(name=com.[[letter]]bbk.launcher2/com.[[bbk]].launcher2.Launcher)”。如何提取出 letter 和 bbk? 我的正则表达式是“\[{2}(\w+)\]{2}”，提取出来的是[letter]和[bbk]，多了一对中括号，请问该如何写这个正则表达式
'''
text = "mSurface=Surface(name=com.[[letter]]bbk.launcher2/com.[[bbk]].launcher2.Launcher)"
r = Re.Assert('[[')+ReT2.WORD.name('word')+ Re.Assert("]]")
matchs = r.exec(text, 'g')
for m in matchs:
    print(m.group('word'))


text='some words before#yyyy#zzzz##aaaa#some words after'
x = ReT.LANY.least(1)
r = ReT.LINE_BEGIN + x.name('before')+'#'+x+'#'+x+'##'+x+'#'+x.name('after') + ReT.LINE_END
m = r.exec(text)
print(m, '>>>', m.group('before'), '>>>', m.group('after') )

print('测试{}*+?')
print(CEnum('abc').repeat(0,1))
print(CRange('09az').least(1))
print( CSeq('jack').least(0))
print(CRange('mn').repeat(9,9))
print(CSeq('jw').repeat(3,4))

print('测试大小写')
r = CSeq('is')
m = r.exec('Iss his long HiStory', 'gi')
print(m)





