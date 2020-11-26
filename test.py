from ArraySequence import ArraySeq as Seq
from test_helper import *
import time


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print(f"{method.__name__} takes total time: {te-ts}")
        return result
    return timed


def test_length():
    tmp_list = create_list(100)
    arr_seq1 = Seq.fromList(tmp_list)
    assert(Seq.length(arr_seq1) == 100)


def test_nth():
    list1 = Seq.singleton(2)
    assert(Seq.nth(list1, 0) == 2)


def test_empty():
    lis_emp = Seq.empty()
    assert(len(lis_emp.arr) == 0)


def test_singleton():
    list1 = Seq.singleton(3)
    assert(len(list1.arr) == 1 and list1.arr[0] == 3)


def test_toList():
    tmp_list = create_list(5)
    arr_seq1 = Seq.fromList(tmp_list)
    seq_list_node = Seq.toList(arr_seq1)

    for i, val in enumerate(arr_seq1):
        assert val == seq_list_node.val
        seq_list_node = seq_list_node.next


def test_fromList():
    tmp_list = create_list(100)
    arr_seq1 = Seq.fromList(tmp_list)
    for i, val in enumerate(arr_seq1.arr):
        assert val == i


def test_toArray():
    tmp_arr = [1,3,5,4,1]
    arr_seq1 = Seq.fromArray(tmp_arr)
    tmp_arr2 = Seq.toArray(arr_seq1)

    assert len(tmp_arr) == Seq.length(arr_seq1)
    for val1, val2 in zip(tmp_arr, tmp_arr2):
        assert val1 == val2


def test_fromArray():
    tmp_arr = [1,3,5,4,1]
    arr_seq1 = Seq.fromArray(tmp_arr)

    assert len(tmp_arr) == Seq.length(arr_seq1)
    for i in range(len(tmp_arr)):
        assert tmp_arr[i] == Seq.nth(arr_seq1,i)


def test_fromStringArray():
    tmp_arr = ["abc", "cde"]
    arr_seq1 = Seq.fromArray(tmp_arr)

    for i, elem in enumerate(arr_seq1):
        assert elem == tmp_arr[i]

@timeit
def test_tabulate_parallel():
    arr_seq1 = Seq.tabulate(plus_one, 20000)
    for i, val in enumerate(arr_seq1):
        assert val == (i + 1)


@timeit
def test_tabulate_sequential():
    arr_seq1 = Seq.tabulate(plus_one, 20000, force_sequential=True)
    for i, val in enumerate(arr_seq1):
        assert val == (i + 1)


@timeit
def test_rev():
    arr_seq1 = Seq.tabulate(mult_two, 20)
    final_seq = Seq.rev(arr_seq1)
    for i in range(Seq.length(final_seq)):
        assert Seq.nth(final_seq, i) == Seq.nth(arr_seq1, Seq.length(arr_seq1) - 1 - i)
    return 


@timeit
def test_append():
    arr_seq1 = Seq.tabulate(mult_two, 20)
    arr_seq2 = Seq.tabulate(plus_one, 20)
    final_seq = Seq.append((arr_seq1, arr_seq2))
    for i in range(Seq.length(final_seq)):
        if i < Seq.length(arr_seq1):
            assert Seq.nth(arr_seq1, i) == Seq.nth(final_seq, i)
        else:
            assert Seq.nth(arr_seq2, i - Seq.length(arr_seq1)) == Seq.nth(final_seq, i)
    return 


@timeit
def test_filter_sequential():
    arr_seq1 = Seq.tabulate(plus_one, 20000)
    final_seq = Seq.filter(is_odd, arr_seq1, force_sequential=True)

    for i, val in enumerate(final_seq):
        assert val == (i * 2 + 1)


@timeit
def test_filter_parallel():
    arr_seq1 = Seq.tabulate(plus_one, 20000)
    final_seq = Seq.filter(is_odd, arr_seq1)
  
    for i, val in enumerate(final_seq):
        assert val == (i * 2 + 1)


@timeit
def test_filterIdx_sequential():
    arr_seq1 = Seq.tabulate(plus_one, 20000)
    final_seq = Seq.filterIdx(is_odd, arr_seq1, force_sequential=True)
    for i, val in enumerate(final_seq):
        assert val == (i * 2)


@timeit
def test_filterIdx_parallel():
    arr_seq1 = Seq.tabulate(plus_one, 20000)
    final_seq = Seq.filterIdx(is_odd, arr_seq1)
    for i, val in enumerate(final_seq):
        assert val == (i * 2)


def test_map():
    arr_seq1 = Seq.tabulate(mult_two, 5)
    final_seq = Seq.map(plus_one, arr_seq1)
    for i, val in enumerate(final_seq):
        assert val == (i * 2 + 1)


def test_subseq():
    arr_seq1 = Seq.tabulate(mult_two, 20)
    final_seq = Seq.subseq(arr_seq1, (5, 5))

    assert Seq.length(final_seq) == 5
    for i, num in enumerate(final_seq):
        assert num == (i + 5) * 2


def test_take():
    arr_seq1 = Seq.tabulate(mult_two, 20)
    final_seq = Seq.take(arr_seq1, 5)

    assert Seq.length(final_seq) == 5
    for i, num in enumerate(final_seq):
        assert num == i * 2


def test_drop():
    arr_seq1 = Seq.tabulate(mult_two, 20)
    final_seq = Seq.drop(arr_seq1, 15)

    assert Seq.length(final_seq) == 5

    for i, num in enumerate(final_seq):
        assert num == (15 + i) * 2


def test_update():
    arr_seq1 = Seq.tabulate(mult_two, 10)
    change = (5, -1)
    final_seq = Seq.update(arr_seq1, change)

    for i, elem in enumerate(final_seq):
        if i == 5:
            assert elem == -1
        else:
            assert elem == Seq.nth(arr_seq1, i)
    return 


def test_inject():
    arr_seq1 = Seq.tabulate(mult_two, 100000)
    inject_pos = Seq.fromList(create_list_from_arr([i for i in range(100000)]))
    inject_val = Seq.fromList(create_list_from_arr([-i for i in range(100000)]))
    final_seq = Seq.inject(arr_seq1, inject_pos, inject_val)

    for i, val in enumerate(final_seq):
        assert i == -val
    return 


@timeit 
def test_scanIncl_sequential():
    arr_seq1 = Seq.tabulate(mult_two, 10001)
    result = Seq.scanIncl(add_lambda,0, arr_seq1, force_sequential=True)
    cur = 0

    for i, num in enumerate(result):
        cur += i * 2
        assert num == cur 


@timeit 
def test_scanIncl_parallel():
    arr_seq1 = Seq.tabulate(mult_two, 10001)
    result = Seq.scanIncl(add_lambda,0, arr_seq1)
    cur = 0

    for i, num in enumerate(result):
        cur += i * 2
        assert num == cur 
        

def test():
    test_nth()
    test_length()
    test_empty()
    test_singleton()
    test_toList()
    test_fromList()
    test_toArray()
    test_fromArray()
    test_fromStringArray()

    test_rev()
    test_append()
    test_map()
    test_update()
    test_inject()    
    test_subseq()
    test_take()
    test_drop()

    test_tabulate_sequential()
    test_tabulate_parallel()
    test_filter_sequential()
    test_filter_parallel()
    test_filterIdx_sequential()
    test_filterIdx_parallel()
    test_scanIncl_sequential()
    test_scanIncl_parallel()
    

    print("All tests passed!")


if __name__ == "__main__":
    test()