from parenlab import *


def get_test_seq(s):
    return Seq.fromArray([c for c in s])

def test():
    test1 = get_test_seq("(())")
    test2 = get_test_seq("()")
    test3 = get_test_seq("(")
    test4 = get_test_seq("()(())")
    test5 = get_test_seq("()((())())(())")
    test6 = get_test_seq("()()(()()()")
    test7 = get_test_seq("((()")
    test8 = get_test_seq("(())")

    assert MPD(test1) == 2
    assert MPD(test2) == 0
    assert MPD(test3) == 0
    assert MPD(test4) == 2
    assert MPD(test5) == 6
    assert MPD(test6) == 0
    assert MPD(test7) == 0
    assert MPD(test8) == 2

if __name__ == "__main__":
    test()