def is_valid(board, row, col, num):
    # 检查行是否有效
    if num in board[row]:
        return False
    
    # 检查列是否有效
    if num in [board[i][col] for i in range(9)]:
        return False
    
    # 检查3x3宫格是否有效
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    
    return True

def solve_sudoku(board):
    # 遍历数独板寻找空格
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:  # 找到空格
                # 尝试填入1-9的数字
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num  # 填入数字
                        if solve_sudoku(board):  # 递归求解
                            return True
                        board[row][col] = 0  # 回溯
                return False  # 无解
    return True  # 所有空格已填满

def print_board(board):
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            print(board[i][j] if board[i][j] != 0 else ".", end=" ")
        print()

# 示例用法
if __name__ == "__main__":
    # 0表示空格
    example_board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
    
    print("初始数独：")
    print_board(example_board)
    
    if solve_sudoku(example_board):
        print("\n解得的数独：")
        print_board(example_board)
    else:
        print("\n无解")