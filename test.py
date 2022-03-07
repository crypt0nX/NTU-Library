import util

chaoxing = util.CX("19552609060", "wrEX9kenCotqw")
#chaoxing = util.CX("13952563221", "G7Uwb3-8Xe.B_b2i")
chaoxing.get_wx()
from multiprocessing.dummy import Pool as ThreadPool

list = [1, 2]


def testFunc(time):
    print(time)


def mutil(user, name):
    pool = ThreadPool()
    pool.map(testFunc, list)
    pool.close()
    pool.join()


mutil(1, 2)
