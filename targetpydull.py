from rpython.rlib import jit

from pydull.parser import parse
from pydull.interpreter import run

def main(args):
    for i in range(len(args)):
        if args[i] == "--jit":
            if len(args) == i + 1:
                print("missing argument after --jit")
                return 2
            jitarg = args[i + 1]
            del args[i:i+2]
            jit.set_user_param(None, jitarg)
            break
    if len(args) == 1:
        print("Give me moar arguments")
    filename = args[1]
    with open(filename) as f:
        ast = parse(f.read())
    value = run(ast)
    print(value)
    return 0

def target(*args):
    return main
