from structs import *
from ArraySequence import ArraySeq as Seq


def create_list(n):
    assert(n > 0)
    dummy_node = ListNode(-1)
    prev_node = dummy_node
    for i in range(n):
        new_node = ListNode(i)
        prev_node.next = new_node
        prev_node = new_node
    return dummy_node.next

def create_list_from_arr(arr):
    dummy_node = ListNode(-1)
    prev_node = dummy_node
    for i, num in enumerate(arr):
        new_node = ListNode(num)
        prev_node.next = new_node
        prev_node = new_node
    return dummy_node.next


def plus_one(x):
    for i in range(20000):
        continue
    return x + 1

def add_lambda(x, y):
    for i in range(20000):
        continue
    return x + y

def mult_two(x):
    return x * 2

def construct_seq(x):
    return Seq.singleton(x)

def is_odd(x):
    for i in range(20000):
        continue
    return x % 2 == 1

def combine(x1x2):
    return x1x2[0] + x1x2[1]