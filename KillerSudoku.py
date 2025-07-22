import time
from collections import defaultdict


class KillerSudokuSolver:
    def __init__(self, cages):
        """初始化求解器

        Args:
            cages: 笼子列表，每个笼子是一个字典，包含:
                'cells': 单元格坐标列表，如[(0,0), (0,1), ...]
                'total': 该笼子的目标总和
        """
        # 初始化9x9网格，全部填充0
        self.grid = [[0 for _ in range(9)] for _ in range(9)]

        # 用于跟踪行、列和3x3宫格中已使用的数字
        self.rows = [set() for _ in range(9)]
        self.cols = [set() for _ in range(9)]
        self.boxes = [set() for _ in range(9)]

        # 处理笼子信息
        self.cages = []
        self.cage_map = [[-1 for _ in range(9)] for _ in range(9)]  # 记录每个单元格所属笼子的索引

        # 为每个笼子添加状态跟踪
        for idx, cage in enumerate(cages):
            cage_dict = {
                'cells': cage['cells'],
                'total': cage['total'],
                'used': set(),  # 已使用的数字
                'current_sum': 0,  # 当前总和
                'remaining': len(cage['cells'])  # 剩余单元格数
            }
            self.cages.append(cage_dict)

            # 更新cage_map
            for (r, c) in cage['cells']:
                self.cage_map[r][c] = idx

    def min_max_sum(self, available_numbers, n):
        """计算n个不同数字的最小和与最大和

        Args:
            available_numbers: 可用的数字集合
            n: 需要选择的数字个数

        Returns:
            (min_sum, max_sum): 最小可能和和最大可能和
        """
        if n == 0:
            return (0, 0)

        # 将可用数字排序
        sorted_nums = sorted(available_numbers)

        # 最小和：取最小的n个数字
        min_sum = sum(sorted_nums[:n])

        # 最大和：取最大的n个数字
        max_sum = sum(sorted_nums[-n:])

        return (min_sum, max_sum)

    def is_valid(self, row, col, num):
        """检查在(row, col)放置数字num是否有效"""
        # 检查行和列约束
        if num in self.rows[row] or num in self.cols[col]:
            return False

        # 检查3x3宫格约束
        box_idx = (row // 3) * 3 + (col // 3)
        if num in self.boxes[box_idx]:
            return False

        # 检查笼子约束
        cage_idx = self.cage_map[row][col]
        cage = self.cages[cage_idx]

        # 检查数字是否已在笼子中使用
        if num in cage['used']:
            return False

        # 检查当前总和是否超过目标总和
        new_sum = cage['current_sum'] + num
        if new_sum > cage['total']:
            return False

        # 计算笼子剩余信息
        remaining_cells = cage['remaining'] - 1  # 放置后剩余的单元格数

        # 如果还有剩余单元格
        if remaining_cells > 0:
            # 计算剩余所需总和
            remaining_total = cage['total'] - new_sum

            # 可用的数字（排除笼子中已使用的数字和当前数字）
            available_nums = set(range(1, 10)) - cage['used'] - {num}

            # 计算剩余数字的最小和与最大和
            min_possible, max_possible = self.min_max_sum(available_nums, remaining_cells)

            # 检查剩余总和是否在可能范围内
            if remaining_total < min_possible or remaining_total > max_possible:
                return False

        # 所有检查通过，有效
        return True

    def solve(self, idx=0):
        """递归求解杀手数独

        Args:
            idx: 当前处理的单元格索引(0-80)

        Returns:
            bool: 是否找到解
        """
        # 所有单元格已处理，求解成功
        if idx == 81:
            return True

        row, col = divmod(idx, 9)

        # 如果单元格已有值，跳过（在杀手数独中通常不会出现）
        if self.grid[row][col] != 0:
            return self.solve(idx + 1)

        # 获取单元格所属的笼子
        cage_idx = self.cage_map[row][col]
        cage = self.cages[cage_idx]
        box_idx = (row // 3) * 3 + (col // 3)

        # 尝试1-9的数字
        for num in range(1, 10):
            if self.is_valid(row, col, num):
                # 放置数字
                self.grid[row][col] = num
                self.rows[row].add(num)
                self.cols[col].add(num)
                self.boxes[box_idx].add(num)

                # 更新笼子状态
                cage['used'].add(num)
                cage['current_sum'] += num
                cage['remaining'] -= 1

                # 递归处理下一个单元格
                if self.solve(idx + 1):
                    return True

                # 回溯：移除数字
                self.grid[row][col] = 0
                self.rows[row].remove(num)
                self.cols[col].remove(num)
                self.boxes[box_idx].remove(num)

                # 恢复笼子状态
                cage['used'].remove(num)
                cage['current_sum'] -= num
                cage['remaining'] += 1

        # 所有数字尝试失败
        return False

    def print_grid(self):
        """打印数独网格"""
        horizontal_line = "+-------+-------+-------+"

        for i, row in enumerate(self.grid):
            if i % 3 == 0:
                print(horizontal_line)

            # 格式化每行输出
            row_str = "| "
            for j, num in enumerate(row):
                row_str += (str(num) if num != 0 else ".")
                if (j + 1) % 3 == 0:
                    row_str += " | "
                else:
                    row_str += " "
            print(row_str)

        print(horizontal_line)


# 示例：steam 杀手数独游戏 困难难度 99关
# 笼子定义：每个笼子包含单元格列表和目标总和
def get_sample_puzzle():
    cages = [
        {'cells': [(0, 0), (0, 1), (0, 2),(0, 3),(0, 4),(1, 0),(1, 1)], 'total': 37},
        {'cells': [(0, 5), (0, 6), (1, 5)], 'total': 17},
        {'cells': [(0, 7), (1, 6), (1, 7)], 'total': 17},
        {'cells': [(0, 8), (1, 8)], 'total': 12},
        {'cells': [(1, 2), (2, 2)], 'total': 14},
        {'cells': [(1, 3), (2, 3), (2, 4),(2, 5)], 'total': 22},
        {'cells': [(2, 0), (3, 0),(4, 0),(5, 0)], 'total': 24},
        {'cells': [(2, 1), (2, 2)], 'total': 11},
        {'cells': [(6, 2), (6, 3)], 'total': 8},
        {'cells': [(7, 2), (7, 3), (7, 4),(7, 5),(8, 4),(8, 5)], 'total': 28},
        {'cells': [(2, 3), (3, 3), (4, 3),(5, 3),(3, 4),(3, 5)], 'total': 36},
        {'cells': [(4, 1), (4, 2)], 'total': 3},
        {'cells': [(4, 4), (4, 5)], 'total': 9},
        {'cells': [(4, 6), (5, 6), (5, 5),(6, 5),(6, 6),(6, 7)], 'total': 22},
        {'cells': [(6, 0), (7, 0), (6, 1),(6, 2),(5, 1),(5, 2)], 'total': 30},
        {'cells': [(6, 3), (6, 4), (5, 4),(7, 4),(8, 4)], 'total': 27},
        {'cells': [(6, 6), (7, 6)], 'total': 5},
        {'cells': [(6, 7), (6, 8), (7, 6),(7, 8)], 'total': 22},
        {'cells': [(8, 0), (8, 1), (8, 2),(8, 3),(7, 1),(7, 2),(7, 3)], 'total': 34},
        {'cells': [(8, 5), (8, 6), (8, 7),(8, 8)], 'total': 21},
    ]
    return cages


if __name__ == "__main__":
    # 获取示例谜题
    cages = get_sample_puzzle()

    # 创建求解器
    solver = KillerSudokuSolver(cages)

    print("开始求解杀手数独...")
    start_time = time.time()

    # 尝试求解
    if solver.solve():
        print("\n求解成功! 耗时: {:.2f}秒".format(time.time() - start_time))
        print("\n杀手数独解决方案:")
        solver.print_grid()
    else:
        print("无解")