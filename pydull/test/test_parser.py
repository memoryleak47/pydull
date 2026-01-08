from pydull.parser import parser, lexer

def test_simple_constructor_in_function():
    s = """\
fn make_suc(x) {
    Suc(x)
}"""
    ast = parser.parse(lexer.lex(s))
    assert len(ast) == 1
    fn_def = ast[0]
    assert fn_def.name == 'make_suc'
    assert len(fn_def.args) == 1
    assert fn_def.args[0].name == 'x'

s = """\
fn add(x, y) {
    match x {
        Suc(z) => Suc(add(z, y)),
        Zero => y,
    }
}

fn mul(x, y) {
    match x {
        Zero => Zero,
        Suc(xx) => add(y, mul(xx, y)),
    }
}

fn one() {
    Suc(Zero)
}

fn factorial(x) {
    match x {
        Zero => one(),
        Suc(xx) => mul(x, factorial(xx)),
    }
}
"""

def test_parser():
    ast = parser.parse(lexer.lex(s))
    import pdb; pdb.set_trace()
    assert len(ast) == 4
    assert ast[0].name == 'add'
    assert ast[1].name == 'mul'
    assert ast[2].name == 'one'
    assert ast[3].name == 'factorial'