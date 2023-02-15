#############turtorial############
#预查 https://www.cnblogs.com/silence-gtx/p/15046027.html
#预查 https://www.jianshu.com/p/8bf162425d83%20
#https://github.com/ziishaned/learn-regex

#RE_REPEAT_MAX = 0xffffffff-1







#escape for square quote
# -不用转义，因为它总是出现在中间位置







import re


























































class Re():
    REPEAT_MAX = 0xffffffff -1




    #不考虑括号








                




























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









    #返回两个标准括号化的regex









    














             





    




        



    








    



    


























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









