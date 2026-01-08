from pydull.parser import parse
from pydull.interpreter import run_fn

def test_constructor():
    s = """
    fn main() {
        Suc(Suc(Zero))
    }
    """
    ast = parse(s)
    value = run_fn("main", [], ast)
    assert(str(value) == "Suc(Suc(Zero))")

def test_fn():
    s = """
    fn foo(x) {
        Suc(Suc(x))
    }

    fn main() {
        foo(foo(Zero))
    }
    """
    ast = parse(s)
    value = run_fn("main", [], ast)
    assert(str(value) == "Suc(Suc(Suc(Suc(Zero))))")
