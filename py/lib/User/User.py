class User():
    def __init__(name, **kw):
        self.name = name
        self.passwd = kw['passwd'] if 'passwd' in kw else ''
        self.home = kw['home'] if 'home' in kw else ''
        self.shell = kw['shell'] if 'shell' in kw else '/bin/sh'

