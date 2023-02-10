#############turtorial############
#预查 https://www.cnblogs.com/silence-gtx/p/15046027.html
#预查 https://www.jianshu.com/p/8bf162425d83%20
#https://github.com/ziishaned/learn-regex

#RE_REPEAT_MAX = 0xffffffff-1
##NODOC
def str_escape(s, cs):
    for c in s:
        if c in cs:
            s = s.replace(c, f'\\{c}' )
    return s

#escape for square quote
# -不用转义，因为它总是出现在中间位置
##NODOC
def escape_sqq(s):
    return str_escape(s, ']^')
##NODOC
def escape_lookaround(s):
    return str_escape(s, ')')

import re
##NODOC
class SetOp():
    def __init__(self, name, level):
        self.name = name
        self.level = level
    def __str__(self):
        return (f'[{self.name}] {self.level}')

##NODOC
class SetOps():
    REF  = SetOp('ref', 20)
    NAME = SetOp('name', 20)
    ASSERT = SetOp('assert', 20)
    ASSERT_NOT = SetOp('assert_not', 20)
    REGEX = SetOp('regex', 9)   #未知操作，则认为是同or的优先级(目前最低)
    CSET = SetOp('cset', 20)   #[$%*]
    #CENUM = SetOp('cenum', 20)   #[$%*]
    CCOMP = SetOp('ccomp', 20)    #[^sd]
    CONCAT = SetOp('concat', 10)     #p[ae]t
    OR = SetOp('or', 9)      #abc|bcd
    REPEAT = SetOp('repeat', 11)    #abc(bd)?
    #(?=www.).+  (?=a.)()
    #SUB = SetOp('sub', 15)  #本质是连接

    def OP2(op, S1, S2):
        if S1.op.level < op.level:
            regex1 = f'({S1.regex})'
        if S2.op.level < op.level:
            regex2 = f'({S2.regex})'

        if op.name == 'concat':
            regex = f'{regex1}{regex2}'
        elif op.name == 'or':
            regex = f'{regex1}|{regex2}' 
        else:
            raise TypeError('unknown operation type')
        S = S(regex, fmt='regex')
        S.op = op

    def OP1(op, S1):
        if S1.op.level < op.level:
            regex1 = f'[^]'
        if op.name == 'reverse':
            regex = f'[^{regex}]'
        elif op.name == 'range':
            regex = f

##NODOC
class PatternFmt():
    #character enumeration
    CENUM = 'cenum'
    #character range
    CRANGE = 'crange'
    #character sequence
    CSEQ = 'cseq'
    #regular expression
    REGEX = 'regex'

class Re():
    REPEAT_MAX = 0xffffffff -1
    ##NODOC
    def As(obj):
        return obj if type(obj) == Re else Re(obj)

    #不考虑括号
    ##NODOC
    def crange2re(pattern):
        re = '' 
        for i in range(0, len(pattern), 2):
            c1 = pattern[i]
            c2 = pattern[i+1]
            re += f'{c1}-{c2}'
        return escape_sqq(re)
                
    ##NODOC
    def CComp(S):
        if S.op.name == 'cset':
            inner = S.regex[1:-1]
            regex = f'[^{inner}]'
            op = SetOps.CCOMP
        #负负得正
        elif S.op.name == 'ccomp':
            inner = S.regex[2:-1]
            regex = f'[{inner}]'
            op = SetOps.CSET
        else:
            raise TypeError(f'{S.regex}, reverse operation can be only applied on "crange,cenum"')
        newS = Re(regex, fmt='regex')
        newS.op = op
        return newS

        '''
        if S.fmt == 'crange':
            regex = Re.crange2re(S.pattern)
            regex = f'[^{regex}]'
        elif S.fmt == 'cenum':
            regex = escape_sqq(S.pattern)
            regex = f'[^{regex}]'
        else:
            raise TypeError(f'{S.regex}, reverse operation can be only applied on "crange,cenum"')
        '''

    '''
    def Complement(S, fullS, isc):
        if not isc:
            XS = Set.AssertNot(S)
            regex = XS.regex + fullS.regex
            op = SetOps.CONCAT  #SUB?正则里的sub也只是拼接
        else:
            op = SetOps.NOT
            if S.fmt == 'crange':
                regex = Set.crange2re(S.pattern, True)
            elif S.fmt == 'cenum':
                regex = '[^{self.pattern}]' 
            else:
                raise TypeError(f'{S.regex}, reverse operation can be only applied on "crange,cenum"')
        newS = S(regex, fmt='regex')
        newS.op = op
        return newS

    def __sub__(self, exp):
        asrtNot = Re.AssertNot(exp)
        return asrtNot + self
    '''

    #TODO handle name
    ##NODOC
    def Copy(A, B):
        B.pattern = A.pattern
        B.fmt = A.fmt
        B.regex = A.regex
        B.op = A.op

    def Assert(S):
        '''
        lookahead assertion. Equalilavant to (?=S.regex)
        @param S Re
         assertion content.
        '''
        S = Re.As(S)
        s = S.regex
        s2 = f'(?={s})'
        newS = Re(s2, fmt=PatternFmt.REGEX)
        newS.op = SetOps.ASSERT
        return newS

    def AssertNot(S):
        '''
        negative lookahead assertion. Equalilavant to (?!S.regex)
        @param S Re
         assertion content.
        '''
        S = Re.As(S)
        regex = f'(?!{S.regex})'
        newS = Re(regex, fmt=PatternFmt.REGEX)
        newS.op = SetOps.ASSERT_NOT
        return newS


    def __init__(self, pattern, **kw):
        '''
        : Constructure of a regular expression object.
        @param pattern str
        A string used to describe the match pattern.
        @param fmt str
        Specify the syntax you used just now in 'pattern'. 4 options provided:
        'cseq'(default): character sequence
        'cenum': character enumeration.
        'crange': character range.
        'regex': regular expression
        The former 3 options provide a foolish way to write your pattern, but 
        easy to use:
        Examples                                    regex equivalents
        r = Re('az',    fmt='cseq')        ==>         'az'
        r = Re('az',    fmt = 'cenum')     ==>         '[az]'
        r = Re('az',    fmt='crange')      ==>         '[a-z]'
        r = Re('az09',  fmt = 'crange')     ==>       '[a-z0-9]'
        r = Re('^-()',  fmt='cseq')        ==>         '\^\-\(\)'
        r = Re('^-()',  fmt='cenum')       ==>         '[\^\-()]'
        r = Re('^-()',  fmt='crange')       ==>         '[\^-\-(-)]'
        
        '''
        fmt = kw['fmt'] if 'fmt' in kw else PatternFmt.CSEQ
        self._name = None

        op = None
        if type(pattern) == Re:
            Re.Copy(pattern, self)
        elif type(pattern) == str:
            if fmt == PatternFmt.REGEX:
                regex = pattern
                op = SetOps.REGEX
            elif fmt == PatternFmt.CRANGE:
                es = Re.crange2re(pattern)
                regex = f'[{es}]'
                op = SetOps.CSET
            elif fmt == PatternFmt.CENUM:
                es = escape_sqq(pattern)
                regex = f'[{es}]'
                op = SetOps.CSET
            elif fmt == PatternFmt.CSEQ:
                es = re.escape(pattern)
                regex = es
                op = SetOps.CONCAT
            object.__setattr__(self, 'regex', regex)
            object.__setattr__(self, 'pattern', pattern)
            object.__setattr__(self, 'fmt', fmt)
            object.__setattr__(self, 'op', op)
        else:
            raise TypeError(f'unspecified type of argument {pattern}')

    def copy(self):
        return Re(self)         

    ##NODOC
    def OP1(op, S):
        if S.op.level < op.level:
            regex = f'({S.regex})'
        else:
            regex = S.regex
        return regex

    #返回两个标准括号化的regex
    ##NODOC
    def OP2(op, S1, S2):
        regex = [S1.regex, S2.regex]
        Sets = [S1, S2]
        for i in range(0,2):
            S = Sets[i] 
            if S.op.level < op.level:
                regex[i] = f'({S.regex})'
        return regex[0], regex[1]
    
    ##NODOC
    def OR(S1, S2):
        #对字符集的并集,优化pattern
        n = 0
        for S in [S1,S2]:
            if S.op.name == 'cset':
                n = n+1
        #print('n is ', n)
        if n == 2:
            regex = S1.regex[1:-1] + S2.regex[1:-1]
            regex = f'[{regex}]'
            newS = Re(regex, fmt='regex')
            newS.op = SetOps.CSET
            return newS
             
        rs = Re.OP2(SetOps.OR, S1, S2)
        regex = f'{rs[0]}|{rs[1]}'
        newS =  re2Re(regex)
        newS.op = SetOps.OR
        return newS
    
    ##NODOC
    def __invert__(self):
        S = Re.CComp(self) 
        return S
        
    ##NODOC
    def __or__(self, obj2):
        return Re.OR(self, Re.As(obj2))
    
    ##NODOC
    def CONCAT(S1, S2):
        rs = Re.OP2(SetOps.CONCAT, S1, S2)
        regex = f'{rs[0]}{rs[1]}'
        newS = re2Re(regex)
        newS.op = SetOps.CONCAT
        #print(regex)
        return newS
    
    ##NODOC
    def __add__(self, obj2):
        return Re.CONCAT(self, Re.As(obj2))
    
    ##NODOC
    def rep_s(_min, _max, greedy):
        if _min == 0 and _max == 1:
            s = '?'
        elif _min == 1 and _max == Re.REPEAT_MAX:
            s = '+'
        elif _min == 0 and _max == Re.REPEAT_MAX:
            s = '*'
        else:
            s_min = str(_min)
            s_max =  '' if _max == Re.REPEAT_MAX else str(_max)
            if _min != _max:    
                s = f'{{{s_min},{s_max}}}'
            else:
                s = f'{{{s_min}}}'
        if greedy == 0:
            s += '?'
        elif greedy == 1:
            pass
        elif greedy == 2:
            s += '+'
        else:
            raise ValueError('parameter "greedy" can only be 0,1,2')
        return s


    def repeat(self, _min, _max=None, **args):
        '''
        @param _max int
         When None, _max keeps same as _min.
         Use Re.REPEAT_MAX to express an unlimited number, or use least() 
        '''
        greedy = 1 if 'greedy' not in args else args['greedy']
            
        if _max == None:
            _max = _min
        ps = Re.OP1(SetOps.REPEAT, self)
        rep_s = Re.rep_s(_min, _max, greedy)
        regex = ps  + rep_s
        newS =  re2Re(regex)
        newS.op = SetOps.REPEAT
        return newS
    
    def least(self, _min, **kw):
        '''
        Equivalents to repeat(_min, Re.REPEAT_MAX).
        '''
        return self.repeat(_min, _max=Re.REPEAT_MAX, **kw)
    
    ##NODOC
    def setname(self, _name):
        s = f'(?P<{_name}>{self.regex})'
        self.pattern = s
        self.fmt = 'regex'
        self.regex = s
        self._name = _name
        self.op = SetOps.NAME

    def name(self, _name=None):
        '''
        return a new Re object decorated as a named capture group,
        which can be refered later using re.Match.group('_name').
        '''
        if _name != None:
            r2 = self.copy()
            r2.setname(_name)
            return r2
        else:
            #return self._name
            raise ValueError('parameter name can not None')

    @staticmethod
    def Ref(_name):
        '''
        Creating a a new Re object representing a backrefence to a named group.
        @param  _name str
         The name of the refered group.
        '''
        s = f'(?P={_name})'
        newS = re2Re(s)
        newS.op = SetOps.REF
        return newS
    
    def exec(self, text, flags=''):
        '''
        Search pattern in text, return a re.Match object, None if not. But:
        @param flags str
         If 'g' in flags, global matching will be performed, and return 
        an array of re.Match objects, empty if not.
         If 'i' in flags, perform case-intensitive matching.
        '''
        regex = self.regex
        re_flags = re.I if 'i' in flags else 0
        if flags and 'g' in flags:
            matchs = []
            it = re.finditer(regex, text, re_flags)
            for m in it:
                matchs.append(m)
            return matchs
        else:
            m = re.search(regex, text, re_flags)
            return m

    #def calculate():
    ##NODOC
    def __str__(self):
        return f'fmt: {self.fmt},    pattern: {self.pattern},    regex:{self.regex},    op:{self.op}'

def CEnum(s):
    return Re(s, fmt=PatternFmt.CENUM)

def CRange(s):
    return Re(s, fmt=PatternFmt.CRANGE)

def CSeq(s):
    return Re(s, fmt=PatternFmt.CSEQ)

def re2Re(s):
    return Re(s, fmt=PatternFmt.REGEX)

def SRegex(s):
    return re2Re(s)

#Regex Template
class SetTemplate():
    dicts = [
        #character set
        {
                'ALPHA': r'[a-zA-Z]',
                'ALNUM': r'[a-zA-Z0-9]',
                'DIGIT': r'\d',     'd':r'\d',
                'NOT_DIGIT': r'\D', 'd':r'\D',
                'SPACE': r'\s',     's': r'\s',
                'NOT_SPACE': r'\S', 'S': r'\S',
                'LANY': r'.',       'DOT': r'.',
                'ANY': '([\n]|.)',
                'NEWLINE': r'[\n]',
                'WORD': r'\w',

                #anchor(location)
                'LINE_BEGIN': r'^',
                'LINE_END': r'$',
                'WORD_BOUNDARY': r'\b',         'b':r'\b',
                'NOT_WORD_BOUNDARY': r'\B',     'B':r'\B',
                },
            {
                #csequence
                'WORD': r'\w+',
                'INT': r'\d+',
                'FLOAT': r'\d+\.\d+',
            }
            ]

    def __init__(self, i):
        self.i = i

    def __getattr__(self, key):
        ret = None
        _dict = SetTemplate.dicts[self.i]
        if key in _dict:
            s = _dict[key]
            S = re2Re(s)
            S.op = SetOps.CONCAT    #TODO dangerous here
            ret = S
        else:
            raise NameError(f'can not find "{key}" in ReTemplate')
        return ret


#模板分组是为了好记，字符集正则往ReT里找，序列正则往ReT2里扎。
ReT = SetTemplate(0)
ReT2 = SetTemplate(1)









