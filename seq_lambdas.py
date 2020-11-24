import copy 
import math
from seq_const import *

def enum_lambda(arr, idx):
    return (idx, copy.deepcopy(arr[idx]))

def rev_lambda(arr, idx):
    return copy.deepcopy(arr[len(arr) - 1 - idx])

def subseq_lambda(arr, start_idx, cur_idx):
    return copy.deepcopy(arr[start_idx + cur_idx])

def append_lambda(arr1, arr2, idx):
    if idx >= len(arr1):
        return copy.deepcopy(arr2[idx - len(arr1)])
    return copy.deepcopy(arr1[idx])

def tabulate_lambda(f, arr, low, high):
    for i in range(low, high):
        arr[i] = f(i)

def add_lambda(x, y):
    return x + y

def filter_lambda(f, num):
    return 1 if f(num) else 0

def filterIdx_lambda(f, s1):
    return ArraySeq.filterIdx(f, s1)

def addIdx_lambda(start_idx, cur_idx):
    return start_idx + cur_idx

def update_lambda(arr, change, idx):
    pos, new_elem = change
    return arr[idx] if idx != pos else new_elem

def inject_lambda(S, pos, val, low, high):
    for i in range(low, high):
        S[pos[i]] = val[i] 

def subseq_lambda(result_arr, old_arr, start_idx, low, high):
    for i in range(start_idx + low, start_idx + high):
        result_arr[i - start_idx] = old_arr[i]

def map_lambda(f, arr, idx):
    return f(arr[idx])

def scanIncl_lambda(arr, f, b, partition_idx):
    n = len(arr)
    segment_len = math.ceil(n / NUM_PROCESSORS)
    low, high = partition_idx * segment_len, min(n,(partition_idx + 1) * segment_len)
    cur = b
    for i in range(low, high):
        cur = f(cur, arr[i])
    return cur

def fill_lambda(original_arr, result, pos, filter_arr_res, low, high):
    for i in range(low, high):
        if filter_arr_res[i] == 1:
            result[pos.arr[i]-1] = original_arr[i]

def fillIdx_lambda(original_arr, result, pos, filter_arr_res, low, high):
    for i in range(low, high):
        if filter_arr_res[i] == 1:
            result[pos.arr[i]-1] = i