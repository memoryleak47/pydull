from rply import LexerGenerator, ParserGenerator
from rply.token import BaseBox

from pydull.dullast import *

lg = LexerGenerator()

lg.add('COMMA', r',')
lg.add('LPAREN', r'\(')
lg.add('RPAREN', r'\)')
lg.add('LBRACE', r'\{')
lg.add('RBRACE', r'\}')
lg.add('ARROW', r'=>')
lg.add('MATCH', r'match')
lg.add('FN', r'fn')
lg.add('LOWER_IDENTIFIER', r'[a-z_][a-zA-Z0-9_]*')
lg.add('UPPER_IDENTIFIER', r'[A-Z][a-zA-Z0-9_]*')

class DummyList(BaseBox):
    def __init__(self, l):
        self.l = l

def unpack_list(bb):
    assert isinstance(bb, DummyList)
    return bb.l

class DummyStr(BaseBox):
    def __init__(self, s):
        self.s = s

lg.ignore(r'\s+|#.*')

lexer = lg.build()

pg = ParserGenerator(
    ['COMMA', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'ARROW',
     'LOWER_IDENTIFIER', 'UPPER_IDENTIFIER', 'MATCH', 'FN'],
    precedence=[],
)

@pg.production('program : fn_defs')
def program(p):
    p0 = p[0]
    return Ast(unpack_list(p0))

@pg.production('fn_defs : fn_defs fn_def')
def fn_defs_multiple(p):
    return DummyList(unpack_list(p[0]) + [p[1]])

@pg.production('fn_defs : fn_def')
def fn_defs_single(p):
    return DummyList([p[0]])

@pg.production('fn_def : FN LOWER_IDENTIFIER argdecl LBRACE expr RBRACE')
def fn_def(p):
    return FnDef(p[1].getstr(), unpack_list(p[2]), p[4])

@pg.production('argdecl : LPAREN fn_args RPAREN')
def argdecl(p):
    return p[1]

@pg.production('argdecl : LPAREN RPAREN')
def argdecl_empty(p):
    return DummyList([])

@pg.production('fn_args : fn_args COMMA expr')
def fn_args_multiple(p):
    return DummyList(unpack_list(p[0]) + [p[2]])

@pg.production('fn_args : expr')
def fn_args_single(p):
    return DummyList([p[0]])

@pg.production('expr : match_expr')
def expr_match(p):
    return p[0]

@pg.production('match_expr : MATCH expr LBRACE match_arms RBRACE')
def match_expr(p):
    return Match(p[1], unpack_list(p[3]))

@pg.production('match_arms : match_arms match_arm')
def match_arms_multiple(p):
    return DummyList(unpack_list(p[0]) + [p[1]])

@pg.production('match_arms : match_arm')
def match_arms_single(p):
    return DummyList([p[0]])

@pg.production('match_arm : pattern ARROW expr COMMA')
def match_arm(p):
    p2 = p[2]
    assert(isinstance(p2, Expr))
    p0 = p[0]
    assert isinstance(p0, Pattern)
    return Arm(p0, p2)

@pg.production('pattern : LOWER_IDENTIFIER')
def pattern_var(p):
    return PatternVar(p[0].getstr())

@pg.production('pattern : UPPER_IDENTIFIER')
def pattern_data_no_vars(p):
    return PatternData(p[0].getstr(), [])

@pg.production('pattern : UPPER_IDENTIFIER LPAREN pattern_vars RPAREN')
def pattern_data(p):
    dl = p[2]
    return PatternData(p[0].getstr(), unpack_list(dl))

@pg.production('pattern_vars : pattern_vars COMMA pattern_var')
def pattern_vars_multiple(p):
    return DummyList(unpack_list(p[0]) + [p[2]])

@pg.production('pattern_vars : pattern_var')
def pattern_vars_single(p):
    return DummyList([p[0]])

@pg.production('pattern_var : LOWER_IDENTIFIER')
def pattern_var(p):
    return PatternVar(p[0].getstr())

@pg.production('expr : LOWER_IDENTIFIER LPAREN exprs RPAREN')
def expr_fn_call(p):
    dl = p[2]
    return FnCall(p[0].getstr(), unpack_list(dl))

@pg.production('expr : LOWER_IDENTIFIER LPAREN RPAREN')
def expr_fn_call_no_args(p):
    return FnCall(p[0].getstr(), [])

@pg.production('expr : LOWER_IDENTIFIER')
def expr_var(p):
    return Var(p[0].getstr())

@pg.production('expr : UPPER_IDENTIFIER LPAREN exprs RPAREN')
def expr_data_constr(p):
    return DataConstr(p[0].getstr(), unpack_list(p[2]))

@pg.production('expr : UPPER_IDENTIFIER')
def expr_data_constr_no_args(p):
    return DataConstr(p[0].getstr(), [])

@pg.production('exprs : exprs COMMA expr')
def exprs_multiple(p):
    return DummyList(unpack_list(p[0]) + [p[2]])

@pg.production('exprs : expr')
def exprs_single(p):
    return DummyList([p[0]])

parser = pg.build()

def parse(s):
    ast = parser.parse(lexer.lex(s))
    assert(isinstance(ast, Ast))
    return ast
