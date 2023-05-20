#Nhóm 21
#Phan Xuân Huynh-N20DCCN023
#Phan Văn Lục-N20DCCN037
#Áp dụng thuật toán A* giải quyết bài toán 8 ô chữ

import heapq
import copy
from colorama import Fore, Back, Style

class Puzzle:
    # Khởi tạo trạng thái bắt đầu của trò chơi
    def __init__(self, state, parent, move, depth, cost):
        self.state = state
        self.parent = parent
        self.move = move
        self.depth = depth
        self.cost = cost

        # Đặt mục tiêu của trò chơi
        if self.state:
            self.goal = [[1, 2, 3], [8, 0, 4], [7, 6, 5]]
            self.m = len(self.state)
            self.n = len(self.state[0])

    def __eq__(self, other):
    # So sánh 2 trạng thái
        return self.state == other.state

    def __lt__(self, other):
    # Sắp xếp theo giá trị cost
        return self.cost < other.cost

    def __str__(self):
    # Chuyển đổi trạng thái thành chuỗi
        return str(self.state)

    def expand(self):
        # Tìm vị trí của số 0
        children = []
        x, y = self.find(0)

        # Khởi tạo các bước di chuyển có thể có
        moves = [(x, y-1, 'Up'), (x, y+1, 'Down'), (x-1, y, 'Left'), (x+1, y, 'Right')]

        # Di chuyển số 0 và tạo ra các trạng thái mới
        for m in moves:
            child = self.move_blank(m[0], m[1], m[2])
            if child is not None:
                children.append(child)
        return children

    def move_blank(self, row, col, move):
        # Di chuyển số 0 và tạo ra trạng thái mới
        if row >= 0 and col >= 0 and row < self.m and col < self.n:
            new_state = copy.deepcopy(self.state)
            x, y = self.find(0)
            new_state[row][col], new_state[x][y] = new_state[x][y], new_state[row][col]
            return Puzzle(new_state, self, move, self.depth + 1, 0)

    def find(self, value):
        # Tìm vị trí của 1 số trong trò chơi
        for i in range(0, self.m):
            for j in range(0, self.n):
                if self.state[i][j] == value:
                    return i, j

    def h(self):
        # Tính giá trị heuristic (heuristic là giá trị ước lượng tối thiểu đến mục tiêu)
        return sum([1 if self.state[i][j] != self.goal[i][j] else 0 for i in range(0, self.m) for j in range(0, self.n)])

    def f(self):
        # Tính giá trị f = g + h (g là độ sâu của trạng thái)
        return self.depth + self.h()

def taciAstar(start, goal):
    # Tạo node bắt đầu với trạng thái và chi phí là 0
    start_node = Puzzle(start, None, None, 0, 0)
    start_node.cost = start_node.f()
    # Tạo hàng đợi ưu tiên với node bắt đầu
    priority_queue = []
    heapq.heappush(priority_queue, start_node)
    # Danh sách các node đã duyệt qua
    closed_list = []
    while priority_queue:
        # Lấy node ưu tiên ra khỏi hàng đợi
        current_node = heapq.heappop(priority_queue)
        # Nếu node hiện tại đang ở trạng thái đích, trả về đường đi từ bắt đầu đến đích
        if current_node.state == goal:
            path = []
            while current_node.parent:
                path.append((current_node.move, current_node.state))
                current_node = current_node.parent
            path.reverse()
            return path
        # Thêm node hiện tại vào danh sách các node đã duyệt qua
        closed_list.append(current_node)
        children = current_node.expand()
        for child in children:
            # Nếu node con đã duyệt qua rồi, bỏ qua
            if child in closed_list:
                continue
            child.cost = child.f()
            # Nếu node con đã có trong hàng đợi và có cost nhỏ hơn, cập nhật cost của node con trong hàng đợi
            if child in priority_queue:
                for n in priority_queue:
                    if n == child and n.cost > child.cost:
                        priority_queue.remove(n)
                        heapq.heappush(priority_queue, child)
                        break
            # Nếu node con chưa có trong hàng đợi, thêm vào hàng đợi
            else:
                heapq.heappush(priority_queue, child)
    return None

# Hàm vẽ bảng trạng thái hiện tại
def draw_board(board):
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                print(Fore.WHITE + Back.RED + ' x ' + Style.RESET_ALL, end=' ')
            else:
                print(Fore.BLACK + Back.WHITE + f' {board[i][j]} ' + Style.RESET_ALL, end=' ')
        print()
    print("\n")


def main():
    # Đọc file
    with open('BaiGK/taci.txt', 'r') as file:
        lines = file.readlines()
        start = []
        goal = []
        for i in range(1, 4): #Lấy trạng thái bắt đầu từ file
            start.append([int(x) if x != 'x' else 0 for x in lines[i].split()])
        for i in range(5, 8): #Lấy trạng thái đích từ file
            goal.append([int(x) if x != 'x' else 0 for x in lines[i].split()])
    # Vẽ trạng thái đầu và đích
    print("Start state:")
    draw_board(start)
    print("Goal state:")
    draw_board(goal)
    
    path = taciAstar(start, goal)
    if path is not None:
        print("Solution found in", len(path), "moves:")
        for move in path:
            # print("Move", move[0])
#             print('''
# ||
# \/
#             ''')
            draw_board(move[1])
    else:
        print("No solution found")

if __name__ == '__main__':
    main()
