import pytest
import py_compile

# Simple tests
# ----------------------------------------------------
def test():
    try:
        py_compile.compile("app.py", doraise=True)
        assert True
    except py_compile.PyCompileError:
        print("Compilation failed!")
        assert False
