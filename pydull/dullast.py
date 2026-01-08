from rply.token import BaseBox

class FnDef(BaseBox):
    _immutable_fields_ = ["name", "args[*]", "expr"]
    def __init__(self, name, args, expr):
        assert isinstance(name, str)
        self.name = name
        assert isinstance(args, list)
        vars = []
        for var in args:
            assert isinstance(var, Var)
            vars.append(var)
        self.args = vars
        self.expr = expr
    
    def __repr__(self):
        return "FnDef(%r, %r, %r)" % (self.name, self.args, self.expr)

class Expr(BaseBox):
    pass

class Match(Expr):
    _immutable_fields_ = ["head", "arms[*]"]
    def __init__(self, head, arms):
        self.head = head
        x = []
        for arm in arms:
            assert isinstance(arm, Arm)
            x.append(arm)
        self.arms = x
    
    def __repr__(self):
        return "Match(%r, %r)" % (self.head, self.arms)

class DataConstr(Expr):
    _immutable_fields_ = ["name", "exprs[*]"]
    def __init__(self, name, exprs):
        self.name = name
        self.exprs = exprs
    
    def __repr__(self):
        return "DataConstr(%r, %r)" % (self.name, self.exprs)

class FnCall(Expr):
    _immutable_fields_ = ["name", "exprs[*]"]
    def __init__(self, name, exprs):
        self.name = name
        self.exprs = exprs
    
    def __repr__(self):
        return "FnCall(%r, %r)" % (self.name, self.exprs)

class Var(Expr):
    _immutable_fields_ = ["name"]
    def __init__(self, name):
        assert isinstance(name, str)
        self.name = name
    
    def __repr__(self):
        return "Var(%r)" % self.name

class Pattern(BaseBox):
    pass

class PatternVar(Pattern):
    _immutable_fields_ = ["name"]
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return "PatternVar(%r)" % self.name

class PatternData(Pattern):
    _immutable_fields_ = ["name", "vars[*]"]
    def __init__(self, name, vars):
        self.name = name
        l = []
        for v in vars:
            assert isinstance(v, PatternVar)
            l.append(v)
        self.vars = l
    
    def __repr__(self):
        return "PatternData(%r, %r)" % (self.name, self.vars)

class Arm(BaseBox):
    _immutable_fields_ = ["pattern", "result"]
    def __init__(self, pattern, result):
        assert isinstance(pattern, Pattern)
        self.pattern = pattern
        self.result = result
    
    def __repr__(self):
        return "Arm(%r, %r)" % (self.pattern, self.result)

class Ast(BaseBox):
    _immutable_fields_ = ["fns[*]"]
    def __init__(self, fns):
        fns2 = []
        for x in fns:
            assert(isinstance(x, FnDef))
            fns2.append(x)
        self.fns = fns2
    
    def __repr__(self):
        return "Ast(%r)" % self.fns
