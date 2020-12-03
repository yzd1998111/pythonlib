from multiprocessing import Process, Value, Array, Pool, Queue
from ctypes import Structure
from seq_lambdas import *
from seq_const import * 
from structs import *
import ctypes
import sys
import math
import functools
import copy



class ArraySeq(object):
    def __init__(self, init_method = "", *args):
        self.arr = None

        if init_method == FROM_LIST:
            assert len(args) == 1
            self._fromList(args[0])
        elif init_method == FROM_ARRAY:
            assert len(args) == 1
            self._fromArray(args[0])
        elif init_method == SINGLETON:
            assert len(args) == 1 
            self._singleton(args[0]) 
        elif init_method == TABULATE:
            assert len(args) == 2 or len(args) == 3 or len(args) == 4
            self._tabulate(*args)
        elif init_method == SHARED_ARRAY:
            self.arr = args[0]
        elif init_method == EMPTY:
            assert len(args) == 0  
            self._empty() 

    @classmethod
    def nth(cls, S, idx):
        return S._nth(idx)

    def _nth(self, idx):
        if idx >= len(self.arr):
            raise Exception("Index out of bound")
        return self.arr[idx]

    @classmethod
    def length(cls, S):
        return S._length()

    def _length(self):
        return len(self.arr)

    @classmethod
    def empty(cls):
        return ArraySeq(EMPTY)

    def _empty(self):
        self.arr = Array("i", 0, lock=False)

    @classmethod
    def singleton(cls, x):
        return ArraySeq(SINGLETON, x)

    def _singleton(self, x):
        seq_type = ctypes.c_wchar_p if isinstance(x, str) else "i"
        self.arr = Array(seq_type, 1, lock=False)
        self.arr[0] = x

    @classmethod
    def toList(cls, S):
        return S._toList()
    
    def _toList(self):
        dummy_node = ListNode(-1)
        prev_node = dummy_node
        
        for elem in self.arr:
            new_node = ListNode(copy.deepcopy(elem))
            prev_node.next = new_node
            prev_node = new_node
        return dummy_node.next 

    @classmethod
    def fromList(cls, head_node):
        return ArraySeq(FROM_LIST, head_node)
    
    def _fromList(self, head_node):
        cur_node = head_node
        cnt = 0
        while cur_node != None:
            cur_node = cur_node.next
            cnt += 1
        cur_node = head_node
        if cnt == 0:
            raise Exception("Cannot create Seq from empty list")

        seq_type = ctypes.c_wchar_p if isinstance(head_node.val, str) else "i"
        self.arr = Array(seq_type, cnt, lock=False)

        i = 0
        while cur_node != None:
            self.arr[i] = cur_node.val 
            cur_node = cur_node.next
            i += 1

    @classmethod
    def fromArray(cls, arr):
        return ArraySeq(FROM_ARRAY, arr)

    def _fromArray(self, arr):
        if len(arr) == 0:
            raise Exception("Cannot create Seq from empty array")

        seq_type = ctypes.c_wchar_p if isinstance(arr[0], str) else "i"
        self.arr = Array(seq_type, arr, lock=False)

    @classmethod
    def toArray(cls, S):
        return S._toArray()
    
    def _toArray(self):
        arr = []
        for num in self.arr:
            arr.append(num)
        return arr  

    @classmethod
    def tabulate(cls, f, n, force_sequential=False, force_parallel=False):
        return ArraySeq(TABULATE, f, n, force_sequential, force_parallel)

    def _tabulate(self, f, n, force_sequential=False, force_parallel=False):
        seq_type = ctypes.c_wchar_p if isinstance(f(0), str) else "i"

        if (n < GRANULAR or force_sequential) and not force_parallel:
            self.arr = Array(seq_type, [f(i) for i in range(n)], lock=False)
        else:
            result_shared = Array(seq_type, n, lock=False)
            segment_len = math.ceil(n / NUM_PROCESSORS)
            processes = []
            for i in range(NUM_PROCESSORS):
                p = Process(target=functools.partial(tabulate_lambda, f, result_shared), args=(segment_len * i, min((i + 1) * segment_len, n)))
                p.start()
                processes.append(p)

            for p in processes:
                p.join()
            self.arr = result_shared

    @classmethod
    def rev(cls, S):
        return S._rev()

    def _rev(self):
        return ArraySeq(TABULATE, functools.partial(rev_lambda, self.arr), len(self.arr))

    @classmethod
    def append(cls, AB):
        A, B = AB
        return A._append(B)

    def _append(self, other):
        return ArraySeq(TABULATE, functools.partial(append_lambda, self.arr, other.arr), len(self.arr) + len(other.arr))

    @classmethod
    def map(cls, f, S):
        return S._map(f)

    def _map(self, f):
        return ArraySeq(TABULATE, functools.partial(map_lambda, f, self.arr), len(self.arr))

    @classmethod
    def update(cls, S, change):
        return S._update(change)

    def _update(self, change):
        pos, elem = ArraySeq.singleton(change[0]), ArraySeq.singleton(change[1])
        if not (change[0] >= 0 and change[0] < len(self.arr)):
            raise Exception("Index out of bound")
        return ArraySeq.inject(self, pos, elem)
 
    @classmethod
    def inject(cls, S, inject_pos, inject_val):
        return S._inject(inject_pos, inject_val)

    def _inject(self, inject_pos, inject_val):
        assert inject_val._length() == inject_pos._length()
        n = inject_val._length()
        seq_type = ctypes.c_wchar_p if isinstance(inject_val.arr[0], str) else "i"
        
        if n == 0:
            raise Exception("Injection sequence cannot be empty")
        elif any([(num < 0 or num >= len(self.arr)) for num in inject_pos]):
            raise Exception("Index out of bound")
        elif n < GRANULAR:
            result_shared = Array(seq_type, len(self.arr), lock=False)
            for i, num in enumerate(self.arr):
                result_shared[i] = num
            for pos, val in zip(inject_pos.arr, inject_val.arr):
                result_shared[pos] = val 
            return ArraySeq(SHARED_ARRAY, result_shared)

        processes = []
        
        segment_len = math.ceil(n / NUM_PROCESSORS)
        

        result_shared = Array(seq_type, ArraySeq.toArray(self), lock=False)
        for i in range(NUM_PROCESSORS):
            p = Process(target=inject_lambda, args=(result_shared, inject_pos.arr, inject_val.arr, segment_len * i, min((i + 1) * segment_len, n)))
            p.start()
            processes.append(p)

        for p in processes:
            p.join()
        return ArraySeq(SHARED_ARRAY, result_shared)

    @classmethod
    def subseq(cls, S, start_and_length):
        return S._subseq(start_and_length)

    def _subseq(self, start_and_length):
        start_idx, n = start_and_length
        if not (1 <= n <= len(self.arr)) or not (0 <= start_idx < len(self.arr)) or not((start_idx + n) <= len(self.arr)):
            raise Exception("Index out of bound")

        if n < GRANULAR:
            return ArraySeq(SHARED_ARRAY, self.arr[start_idx:start_idx+n])
        
        segment_len = math.ceil(n / NUM_PROCESSORS)
        processes = []

        seq_type = ctypes.c_wchar_p if isinstance(self.arr[0], str) else "i"
        result_shared = Array(seq_type, n, lock=False)

        for i in range(NUM_PROCESSORS):
            p = Process(target=subseq_lambda, args=(result_shared, self.arr, start_idx, segment_len * i, min((i + 1) * segment_len, n)))
            p.start()
            processes.append(p)

        for p in processes:
            p.join()

        return ArraySeq(SHARED_ARRAY, result_shared)

    @classmethod
    def take(cls, S, n):
        return S._take(n)

    def _take(self, n):
        return self._subseq((0, n))

    @classmethod
    def drop(cls, S, n):
        return S._drop(n)

    def _drop(self, n):
        return self._subseq((n, len(self.arr)-n))

    @classmethod
    def filter(cls, f, S, force_sequential=False):
        if S._length() == 0:
            return ArraySeq.empty()
        return S._filter(f, force_sequential)

    def _filter(self, f, force_sequential=False):
        n = len(self.arr)
        processes = []

        if n < GRANULAR or force_sequential:
            return self._filter_sequential(f)

        arr_form = ArraySeq.toArray(self)
        
        with Pool(16) as pool:
            ans = pool.map(functools.partial(filter_lambda, f), arr_form)
        
        arr_seq_form = ArraySeq(FROM_ARRAY, ans)
        pref_sum = ArraySeq.scanIncl(add_lambda, 0, arr_seq_form)

        seq_type = ctypes.c_wchar_p if isinstance(self.arr[0], str) else "i"
        result = Array(seq_type, pref_sum.arr[-1],lock=False)

        segment_len = math.ceil(n / NUM_PROCESSORS)

        for i in range(NUM_PROCESSORS):
            p = Process(target=fill_lambda, args=(self.arr, result, pref_sum, ans, i * segment_len, min((i + 1) * segment_len, n)))
            p.start()
            processes.append(p)

        for p in processes:
            p.join()

        res_seq = ArraySeq(FROM_ARRAY, result)
        return res_seq

    def _filter_sequential(self, f):
        res = []
        for num in self:
            if f(num):
                res.append(num)

        seq_type = ctypes.c_wchar_p if isinstance(self.arr[0], str) else "i"
        res_shared_form = Array(seq_type, res, lock=False)
        filtered_seq = ArraySeq(FROM_ARRAY, res_shared_form)
        return filtered_seq

    @classmethod
    def filterIdx(cls, f, S, force_sequential=False):
        if S._length() == 0:
            return ArraySeq.empty()
        return S._filterIdx(f, force_sequential)

    def _filterIdx_sequential(self, f):
        res = []
        for i, num in enumerate(self):
            if f(num):
                res.append(i)

        seq_type = ctypes.c_wchar_p if isinstance(self.arr[0], str) else "i"
        res_shared_form = Array(seq_type, res, lock=False)
        filtered_seq = ArraySeq(FROM_ARRAY, res_shared_form)
        return filtered_seq

    def _filterIdx(self, f, force_sequential=False):
        n = len(self.arr)
        processes = []

        if n < GRANULAR or force_sequential:
            return self._filterIdx_sequential(f)

        arr_form = ArraySeq.toArray(self)
        
        with Pool(16) as pool:
            ans = pool.map(functools.partial(filter_lambda, f), arr_form)
        
        arr_seq_form = ArraySeq(FROM_ARRAY, ans)
        pref_sum = ArraySeq.scanIncl(add_lambda, 0, arr_seq_form)

        seq_type = ctypes.c_wchar_p if isinstance(self.arr[0], str) else "i"
        result = Array(seq_type, pref_sum.arr[-1],lock=False)
        segment_len = math.ceil(n / NUM_PROCESSORS)

        for i in range(NUM_PROCESSORS):
            p = Process(target=fillIdx_lambda, args=(self.arr, result, pref_sum, ans, i * segment_len, min((i + 1) * segment_len, n)))
            p.start()
            processes.append(p)

        for p in processes:
            p.join()

        res_seq = ArraySeq(FROM_ARRAY, result)
        return res_seq

    @classmethod
    def scanIncl(cls, f, b, S, force_sequential=False):
        if S._length() == 0:
            return ArraySeq.empty()

        seq_type = ctypes.c_wchar_p if isinstance(f(b, S.arr[0]), str) else "i"
        prefs = Array(seq_type, len(S.arr), lock=False)

        array_native = ArraySeq.toArray(S)
        if len(S.arr) < GRANULAR or force_sequential:
            S._scanIncl_sequential(prefs, array_native, f, b, 0, len(S.arr)) 
        else:
            S._scanIncl_parallel(prefs, array_native, f, b, 0, len(S.arr))
        return ArraySeq(SHARED_ARRAY, prefs)

    def _scanIncl_sequential(self, prefs, array_native, f, b, low, high):
        cur = b
        for i in range(low, high):
            prefs[i] = f(cur, array_native[i])
            cur = prefs[i]

    def _scanIncl_parallel(self, prefs, array_native, f, b, low, high):
        if (high - low) <= GRANULAR:
            self._scanIncl_sequential(prefs, array_native, f, b, low, high)
        else:
            processes = []
            n = high - low
            segment_len = math.ceil(n / NUM_PROCESSORS)

            partial_sums = ArraySeq.tabulate(functools.partial(scanIncl_lambda,array_native, f, b), NUM_PROCESSORS, force_parallel=True)
            middle_scan_result = ArraySeq.scanIncl(f, b, partial_sums)
   
            for i in range(NUM_PROCESSORS):
                p = Process(target=self._scanIncl_sequential, args=(prefs, array_native, f, middle_scan_result.arr[i-1] if i > 0 else 0, i * segment_len, min((i + 1) * segment_len, high)))
                p.start()
                processes.append(p)

            for p in processes:
                p.join()

    @classmethod
    def splitMid(cls, S):
        return S._splitMid()

    def _splitMid(self):
        n = self._length()
        if n == 0:
            return ArraySeq.empty()
        elif n == 0:
            return ArraySeq.singleton(self.arr[0])
        else:
            mid = math.ceil(n / 2)
            l, r = ArraySeq.take(self, mid), ArraySeq.drop(self, mid)
            return (l, r)

    def __repr__(self):
        return ",".join(map(str,self.arr))

    def __iter__(self):
        self.n = 0
        return self 

    def __next__(self):
        if self.n < len(self.arr):
            self.n += 1
            return self.arr[self.n-1]
        else:
            raise StopIteration
