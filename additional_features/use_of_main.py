# Suppose this is foo.py.

print("before import")
import math

print("before function_a")
def function_a():
    print("Function A")

print("before function_b")
def function_b():
    print("Function B {}".format(math.sqrt(100)))
print("before function_main")

def main():
    print("_&_" * 11)
    print("Main")
    function_a()
    function_b()
    print("_&_" * 11)
print("before __name__ guard")

if __name__ == '__main__':
    function_a()
    function_b()
    main()
print("after __name__ guard")