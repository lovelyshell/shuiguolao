import varname

class VarError(Exception):
    def __init__(self, variable):
        self.var_value = str(variable)
        self.var_name = varname.getpass(variable)


class ExistError(Exception):
    def __init__(self, badobj):
        self.badobj = badobj

    def __str__(self):
        obj_s = str(self.badobj) 
        return f"'{obj_s}' alreadly exists"


class NotFoundError(Exception):
    def __init__(self, badobj):
        self.badobj = badobj

    def __str__(self):
        obj_s = str(self.badobj) 
        return f"'{obj_s}' not found"

class ParamTypeError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

def shorter_type(type_s):
    return type_s.split("'")[-2]

def param_type_check(param, allowed_types):
    ok = False
    type_lst = []
    for t in allowed_types:
        if type(param) == t:
            ok = True
        type_lst.append(shorter_type(str(t)))
    if ok:
        return True
    pass_name =  varname.getpass(param)
    expect_s = '|'.join(type_lst)
    got_s = str(param)
    message = f"[{pass_name}] illegal type, got {got_s}, expect <{expect_s}>."
    raise ParamTypeError(message)

