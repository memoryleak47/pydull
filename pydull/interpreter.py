from pydull.dullast import *
from rpython.rlib import jit

def get_printable_location(f, ast):
    return f.name

driver = jit.JitDriver(get_printable_location=get_printable_location, reds="auto", greens=["f", "ast"], is_recursive=True)

class Value:
    def __init__(self, dcname, args):
        self.dcname = dcname
        self.args = args

    def __repr__(self):
        return "Value(%r, %r)" % (self.dcname, self.args)

    def to_str(self):
        s = self.dcname
        if len(self.args) == 0: return s
        s += "("
        s += ", ".join([a.to_str() for a in self.args])
        s += ")"
        return s

    __str__ = to_str

@jit.elidable
def find_func(name, ast):
    for f in ast.fns:
        if f.name == name:
            return f
    raise KeyError()

@jit.unroll_safe
def eval_expr(expr, sigma, ast):
    if isinstance(expr, DataConstr):
        return Value(expr.name, [eval_expr(x, sigma, ast) for x in expr.exprs])
    if isinstance(expr, Var):
        return sigma[expr.name]
    if isinstance(expr, FnCall):
        return run_fn(expr.name, [eval_expr(x, sigma, ast) for x in expr.exprs], ast)
    if isinstance(expr, Match):
        v = eval_expr(expr.head, sigma, ast)
        for arm in expr.arms:
            pattern = arm.pattern
            if isinstance(pattern, PatternVar):
                sigma = sigma.copy()
                sigma[pattern.name] = v
            elif isinstance(pattern, PatternData) and pattern.name == v.dcname:
                sigma = sigma.copy()
                for i, a in enumerate(pattern.vars):
                    b = v.args[i]
                    sigma[a.name] = b
            else: continue
            return eval_expr(arm.result, sigma, ast)
    raise ValueError()

@jit.unroll_safe
def run_fn(fnname, args, ast):
    f = find_func(fnname, ast)

    sigma = {}
    for i, a in enumerate(args):
        b = f.args[i]
        sigma[b.name] = a
    driver.jit_merge_point(f=f, ast=ast)
    return eval_expr(f.expr, sigma, ast)

def run(ast):
    v = run_fn("main", [], ast)
    print(v.to_str())
