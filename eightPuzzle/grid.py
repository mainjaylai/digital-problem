class Grid(object):
    # 代表移动的方向类
    direction = {
        "up": [-1, 0],
        "down": [1, 0],
        "left": [0, -1],
        "right": [0, 1]
    }

    def __init__(self, scene, moves):
        """
        @param scene: 代表现在场面上的数字信息，为二维数组，0代表空
        @param moves: 代表从原始状态到此状态的移动步数，为数组，初始为'【#】'
        """
        self.scene = scene
        self.moves = moves

        # fn代表启发式函数的值
        self.fn = 0
        N = len(scene)
        for i in range(N):
            flag = True
            for j in range(N):
                if scene[i][j] == 0:
                    # 空格的位置信息
                    self.zero_x = i
                    self.zero_y = j
                    flag = False
                    break
            if not flag:
                break

    def move(self, movement, flag=True):
        """
        移动函数
        @param movement:代表下一步移动的方向 
        @param flag: 表示是否要加入到步数中去，打乱情况不需要加入到步数中
        @return: 
        """
        # 当前位置状态移动
        self.scene[self.zero_x][self.zero_y] = \
            self.scene[self.zero_x + Grid.direction[movement][0]][self.zero_y + Grid.direction[movement][1]]
        self.scene[self.zero_x + Grid.direction[movement][0]][self.zero_y + Grid.direction[movement][1]] = 0

        # 更新空块的位置信息
        self.zero_x = self.zero_x + Grid.direction[movement][0]
        self.zero_y = self.zero_y + Grid.direction[movement][1]
        if flag:
            self.moves.append(movement)

    def moveable(self):
        """
        表示当前状态下一步可移动的方向集合
        @return: list方向集合
        """
        N = len(self.scene)
        movement = ["up", "down", "left", "right"]

        # 这里我用了一个小技巧，如果上一步是相反的方向就不需要做，使用了剪枝技巧
        if self.zero_y == N - 1 or self.moves[len(self.moves) - 1] == "left":
            movement.remove("right")
        if self.zero_y == 0 or self.moves[len(self.moves) - 1] == "right":
            movement.remove("left")
        if self.zero_x == N - 1 or self.moves[len(self.moves) - 1] == "up":
            movement.remove("down")
        if self.zero_x == 0 or self.moves[len(self.moves) - 1] == "down":
            movement.remove("up")
        return movement

    def heuristicFunc1_manhattan_dis(self, end_state):
        """
        第一个启发式函数，g(n)为每一个网格点的曼哈顿距离之和，h(n)为深度
        @param end_state: 代表目标状态的网格布局，为二维数组
        @return:
        """
        dist = 0
        cur_state = self.scene
        N = len(cur_state)
        for i in range(N):
            for j in range(N):
                if cur_state[i][j] == end_state[i][j]:
                    continue
                num = cur_state[i][j]
                if num == 0:
                    x = N - 1
                    y = N - 1
                else:
                    x = num / N  # 理论横坐标
                    y = num - N * x - 1  # 理论的纵坐标
                dist += (abs(x - i) + abs(y - j))
        self.fn = dist + len(self.moves) - 1

    def heuristicFunc2_Reverse(self, end_target):
        """
        第二个启发式函数，h(n)为逆序数之差的三倍加上不同位置的数目之和，h(n)为深度
        @param end_target:
        @return:
        """
        different_counts = 0
        source_reverse_counts = 0
        N = len(end_target)
        arr = []
        for i in range(N):
            for j in range(N):
                if self.scene[i][j] != end_target[i][j]:
                    different_counts += 1
                arr.append(self.scene[i][j])
        for i in range(N * N - 1):
            for j in range(i, N * N):
                if arr[i] > arr[j]:
                    source_reverse_counts += 1
        self.fn = source_reverse_counts * 3 + different_counts + len(self.moves) - 1

    def __lt__(self, other):
        """
        用于堆的比较，返回距离最小的
        @param other:
        @return:
        """
        return self.fn < other.fn

    def __eq__(self, other):
        """
        相等的判断
        @param other:
        @return:
        """
        return self.hash_value == other.hash_value

    def __ne__(self, other):
        """
        不等的判断
        @param other:
        @return:
        """
        return not self.__eq__(other)
