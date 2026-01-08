from pydull.dullast import *

class Value:
    def __init__(self, dcname, args):
        self.dcname = dcname
        self.args = args

    def __repr__(self):
        return "Value(%r, %r)" % (self.dcname, self.args)

    def __str__(self):
        s = self.dcname
        if len(self.args) == 0: return s
        s += "("
        s += ", ".join(str(a) for a in self.args)
        s += ")"
        return s

def find_func(name, ast):
    for f in ast.fns:
        if f.name == name:
            return f
    raise "oh no"

def eval_expr(expr, sigma, ast):
    if isinstance(expr, DataConstr):
        return Value(expr.name, [eval_expr(x, sigma, ast) for x in expr.exprs])
    if isinstance(expr, Var):
        return sigma[expr.name]
    if isinstance(expr, FnCall):
        return run_fn(expr.name, [eval_expr(x, sigma, ast) for x in expr.exprs], ast)
    if isinstance(expr, Match):
        v = eval_expr(expr.head, sigma, ast)
        arm = None
        for arm in expr.arms:
            pattern = arm.pattern
            if isinstance(pattern, PatternVar):
                sigma = sigma.copy()
                sigma[pattern.name] = v
                break
            elif isinstance(pattern, PatternData) and pattern.name == v.dcname:
                sigma = sigma.copy()
                for a, b in zip(pattern.vars, v.args):
                    sigma[a.name] = b
                break
        return eval_expr(arm.result, sigma, ast)
    raise "oh noes"

def run_fn(fnname, args, ast):
    f = find_func(fnname, ast)

    sigma = dict()
    for a, b in zip(args, f.args):
        sigma[b.name] = a
    return eval_expr(f.expr, sigma, ast)

def run(ast):
    v = run_fn("main", [], ast)
    print(v)
