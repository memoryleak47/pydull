from pydull.parser import parse
from pydull.interpreter import run

def main(args):
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
