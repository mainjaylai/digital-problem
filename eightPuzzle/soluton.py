# 深度优先搜索
import copy
import os
import random
import time
from queue import Queue
from queue import PriorityQueue
import psutil as psutil
from eightPuzzle.grid import Grid


# 整合各种问题解决类
class Solve(object):

    def __init__(self, source, target):
        """
        初始化类
        @param source:源状态的二维数组
        @param target: 目标状态的二维数组
        """
        self.length = 15  # dfs的探索深度
        self.is_end = False  # 判断是否已经探索完毕
        self.target = target  # 目标状态，二维数组
        self.source = Grid(source, ["#"])  # 初始化目标状态，moves初始化为【"#"】
        self.grid_sets = set()  # 存储当前已经遍历的所有状态的集合，做到剪枝
        self.solve_moves = []  # 存储算法的解决方案
        self.start_time = time.time()  # 方便计算运行运行实践
        self.run_time = time.time()  # 存储算法运行时间
        self.counts = 0  # 存储当前搜索节点总个数
        self.memory = 0.0000  # 存储算法占用空间

    def mess_up(target):
        """
        打乱函数
        @return: 打乱的状态数组
        """
        mess = Grid(target, ["#"])
        times = 20
        for i in range(times):
            movements = mess.moveable()
            mess.move(random.choice(movements), flag=False)
        return mess.scene

    def DFS_search(self):
        """
        深度优先搜索函数
        @return:
        """
        source_copy = copy.deepcopy(self.source)
        self.clear()
        self.DFS(source_copy)

    def DFS(self, grid):
        # 如果是目标状态直接返回
        if str(grid.scene) == str(self.target):
            self.is_end = True
            self.solve_moves = grid.moves
            end_time = time.time()
            self.run_time = end_time - self.start_time
            self.memory = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024 / 1024
            return
        # 如果长度大于设定的长度，也返回
        if len(grid.moves) >= self.length or self.is_end:
            return
        self.counts += 1
        self.grid_sets.add(str(grid.scene))
        movements = grid.moveable()
        # 遍历所有可以执行方向
        for movement in movements:
            grid_copy = copy.deepcopy(grid)
            grid_copy.move(movement)
            if str(grid_copy.scene) in self.grid_sets:
                continue
            self.DFS(grid_copy)
        self.grid_sets.remove(str(grid.scene))

    def BFS_search(self):
        """
        宽度优先搜索
        @return:
        """
        queue = Queue()
        queue.put(copy.deepcopy(self.source))
        self.clear()
        while not queue.empty():
            grid = queue.get()
            # 判断是否等于最后目标
            if str(grid.scene) == str(self.target):
                self.solve_moves = grid.moves
                end_time = time.time()
                self.run_time = end_time - self.start_time
                self.memory = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024 / 1024
                break
            self.grid_sets.add(str(grid.scene))
            self.counts += 1
            movements = grid.moveable()
            for movement in movements:
                grid_copy = copy.deepcopy(grid)
                # 依次加入队列
                grid_copy.move(movement)
                if str(grid_copy.scene) in self.grid_sets:
                    continue
                queue.put(grid_copy)

    def A_search(self):
        """
        第一个启发式搜索函数
        @return:
        """
        source_copy = copy.deepcopy(self.source)
        source_copy.heuristicFunc1_manhattan_dis(self.target)
        # 新建优先队列
        q = PriorityQueue()
        q.put(source_copy)
        self.clear()
        self.grid_sets.add(str(source_copy.scene))
        while not q.empty():
            top = q.get()
            # 结束后直接输出路径
            if str(top.scene) == str(self.target):
                self.solve_moves = top.moves
                end_time = time.time()
                self.run_time = end_time - self.start_time
                self.memory = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024 / 1024
                print(self.solve_moves)
                break
            self.counts += 1
            self.grid_sets.add(str(top.scene))
            movements = top.moveable()
            for movement in movements:
                top_copy = copy.deepcopy(top)
                top_copy.move(movement)
                if str(top_copy.scene) in self.grid_sets:
                    continue
                # 计算其启发式函数
                top_copy.heuristicFunc1_manhattan_dis(self.target)
                q.put(top_copy)

    def B_search(self):
        """
        第二个启发式函数
        @return:
        """
        source_copy = copy.deepcopy(self.source)
        source_copy.heuristicFunc2_Reverse(self.target)
        # 新建优先队列
        q = PriorityQueue()
        q.put(source_copy)
        self.clear()
        self.grid_sets.add(str(source_copy.scene))
        while not q.empty():
            top = q.get()
            # 结束
            if str(top.scene) == str(self.target):
                self.solve_moves = top.moves
                end_time = time.time()
                self.run_time = end_time - self.start_time
                self.memory = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024 / 1024
                print(self.solve_moves)
                break
            self.counts += 1
            self.grid_sets.add(str(top.scene))
            movements = top.moveable()
            # 遍历所有可以遍历的
            for movement in movements:
                top_copy = copy.deepcopy(top)
                top_copy.move(movement)
                if str(top_copy.scene) in self.grid_sets:
                    continue
                top_copy.heuristicFunc2_Reverse(self.target)
                q.put(top_copy)

    def clear(self):
        self.is_end = False
        self.grid_sets.clear()
        self.counts = 0
        self.solve_moves = ['#']
        self.counts = 0
        self.memory = 0.0000
        self.run_time = time.time()
        self.start_time = time.time()


# if __name__ == '__main__':
#     counts = 50
#     target = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]
#     source = Solve.mess_up(copy.deepcopy(target))
#     solve = Solve(source, target)
#     sources = []
#     for i in range(counts):
#         source = Solve.mess_up(copy.deepcopy(target))
#         sources.append(source)
#     print(sources)
if __name__ == '__main__':
    print(0.013996734619140624 * 1024)
    # counts = 50
    # sum_time = 0.0000000
    # target = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]
    # sum_counts = 0
    # sum_memory = 0.0000
    # time_counts = 0
    # sources = [[[5, 1, 3, 4], [10, 2, 7, 8], [0, 6, 11, 12], [9, 13, 14, 15]],
    #            [[1, 2, 8, 3], [5, 6, 4, 0], [9, 10, 7, 12], [13, 14, 11, 15]],
    #            [[5, 1, 2, 3], [9, 7, 4, 8], [10, 6, 15, 11], [13, 14, 12, 0]],
    #            [[1, 2, 3, 4], [5, 6, 7, 8], [9, 14, 10, 15], [13, 12, 11, 0]],
    #            [[1, 2, 3, 4], [5, 6, 8, 0], [9, 14, 7, 12], [13, 11, 10, 15]],
    #            [[1, 2, 8, 3], [5, 7, 4, 0], [10, 6, 12, 15], [9, 13, 14, 11]],
    #            [[1, 2, 3, 4], [5, 6, 7, 0], [9, 10, 15, 8], [13, 14, 12, 11]],
    #            [[1, 2, 3, 4], [5, 6, 7, 8], [0, 10, 12, 15], [9, 13, 14, 11]],
    #            [[1, 3, 6, 4], [5, 0, 2, 8], [9, 11, 7, 12], [13, 10, 14, 15]],
    #            [[1, 2, 3, 4], [5, 6, 7, 8], [0, 10, 11, 12], [9, 13, 14, 15]],
    #            [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 0, 14, 15]],
    #            [[1, 3, 0, 7], [5, 2, 8, 4], [9, 6, 10, 12], [13, 14, 11, 15]],
    #            [[5, 1, 3, 4], [2, 7, 8, 0], [9, 6, 10, 12], [13, 14, 11, 15]],
    #            [[0, 2, 3, 4], [1, 5, 7, 8], [9, 6, 15, 11], [13, 10, 14, 12]],
    #            [[1, 2, 3, 4], [9, 5, 6, 8], [13, 10, 7, 12], [14, 0, 11, 15]],
    #            [[6, 1, 3, 4], [5, 2, 7, 8], [0, 10, 11, 12], [9, 13, 14, 15]],
    #            [[1, 2, 3, 4], [5, 6, 7, 8], [9, 11, 0, 12], [13, 10, 14, 15]],
    #            [[1, 3, 6, 4], [5, 2, 7, 8], [9, 10, 0, 12], [13, 14, 11, 15]],
    #            [[1, 2, 4, 7], [5, 10, 6, 3], [9, 14, 11, 8], [13, 0, 15, 12]],
    #            [[2, 5, 3, 4], [1, 0, 6, 7], [9, 10, 11, 8], [13, 14, 15, 12]],
    #            [[1, 2, 3, 4], [5, 6, 7, 8], [0, 9, 15, 11], [13, 10, 14, 12]],
    #            [[1, 2, 3, 4], [5, 6, 7, 0], [9, 11, 14, 8], [13, 10, 15, 12]],
    #            [[5, 1, 2, 4], [6, 0, 3, 8], [9, 10, 7, 11], [13, 14, 15, 12]],
    #            [[1, 6, 0, 3], [5, 8, 2, 4], [9, 10, 7, 12], [13, 14, 11, 15]],
    #            [[1, 6, 2, 3], [5, 10, 7, 4], [9, 11, 8, 12], [13, 14, 15, 0]],
    #            [[5, 1, 3, 4], [10, 2, 7, 8], [6, 15, 0, 11], [9, 13, 14, 12]],
    #            [[1, 6, 2, 4], [9, 5, 3, 7], [0, 10, 11, 8], [13, 14, 15, 12]],
    #            [[1, 2, 7, 3], [5, 0, 11, 4], [9, 6, 14, 8], [13, 15, 10, 12]],
    #            [[1, 2, 0, 3], [5, 6, 7, 4], [9, 10, 11, 8], [13, 14, 15, 12]],
    #            [[0, 1, 2, 4], [5, 6, 3, 8], [9, 10, 7, 12], [13, 14, 11, 15]],
    #            [[1, 2, 7, 3], [5, 10, 6, 4], [9, 14, 11, 8], [13, 0, 15, 12]],
    #            [[1, 2, 0, 3], [5, 6, 7, 4], [9, 10, 11, 8], [13, 14, 15, 12]],
    #            [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 15], [13, 0, 12, 14]],
    #            [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 0, 14, 15]],
    #            [[1, 2, 0, 7], [5, 6, 4, 3], [9, 10, 11, 8], [13, 14, 15, 12]],
    #            [[5, 1, 3, 4], [6, 9, 7, 8], [0, 2, 10, 12], [13, 14, 11, 15]],
    #            [[2, 3, 0, 4], [1, 6, 7, 8], [5, 9, 10, 12], [13, 14, 11, 15]],
    #            [[1, 2, 3, 4], [5, 11, 6, 8], [9, 7, 0, 12], [13, 10, 14, 15]],
    #            [[1, 2, 7, 3], [5, 6, 4, 0], [9, 10, 11, 8], [13, 14, 15, 12]],
    #            [[1, 2, 3, 4], [6, 0, 7, 8], [5, 9, 10, 11], [13, 14, 15, 12]],
    #            [[1, 2, 3, 4], [5, 6, 7, 8], [9, 15, 14, 11], [13, 0, 10, 12]],
    #            [[1, 2, 3, 4], [5, 10, 6, 7], [9, 11, 15, 8], [13, 14, 12, 0]],
    #            [[1, 2, 3, 4], [5, 0, 6, 7], [9, 10, 12, 11], [13, 14, 15, 8]],
    #            [[1, 2, 3, 4], [5, 0, 7, 8], [9, 6, 11, 12], [13, 10, 14, 15]],
    #            [[5, 2, 3, 4], [6, 1, 7, 0], [9, 10, 12, 8], [13, 14, 11, 15]],
    #            [[2, 6, 3, 4], [1, 10, 7, 8], [5, 13, 11, 12], [9, 0, 14, 15]],
    #            [[1, 2, 0, 4], [5, 7, 3, 8], [9, 6, 10, 12], [13, 14, 11, 15]],
    #            [[1, 2, 4, 7], [5, 6, 3, 8], [9, 10, 11, 12], [13, 0, 14, 15]],
    #            [[1, 2, 3, 4], [5, 6, 11, 0], [9, 10, 8, 7], [13, 14, 15, 12]],
    #            [[1, 2, 3, 4], [5, 6, 11, 7], [9, 10, 0, 8], [13, 14, 15, 12]]]
    # for source in sources:
    #     solve = Solve(source, target)
    #     solve.BFS_search()
    #     if solve.run_time < 100:
    #         time_counts += 1
    #         print("time: %f" % solve.run_time)
    #         sum_time += solve.run_time
    #     print("counts:%d" % solve.counts)
    #     sum_counts += solve.counts
    #     print(u'当前进程的内存使用：%.4f GB' % solve.memory)
    #     sum_memory += solve.memory
    #     print("sum_count: %d" % sum_counts)
    #     print("sum_time: %f" % sum_time)
    # print(sum_time / time_counts)
    # print(sum_counts / counts)
    # print(sum_memory / counts)

# 1.9786533763011296 DFS
# 16205.1
# 0.008366851806640626

# 2.4459443283081055 BFS
# 16386.34
# 0.042684326171875

# 0.007265257835388184 A*
# 39.7
# 0.008977737426757813

# 0.10634735107421875 b*
# 503.4
# 0.013996734619140624
#
