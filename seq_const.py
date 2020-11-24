import multiprocessing

FROM_LIST = "fromList"
FROM_ARRAY = "fromArray"
SINGLETON = "singleton"
TABULATE = "tabulate"
EMPTY = "empty"
SHARED_ARRAY = "shared_array"
GRANULAR =  10000
NUM_PROCESSORS = multiprocessing.cpu_count()