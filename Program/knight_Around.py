import copy
import numpy as np
import heapq

mapSize = 5
nc = 0
inf = float('inf')


class Board:
    def __init__(self, board, x, y, depth, goal):
        self.board = board
        self.knight_x = x
        self.knight_y = y
        self.depth = depth
        self.goal = goal

    def movable(self, x, y):
        knight_x = (self.knight_x + x) % mapSize
        knight_y = self.knight_y + y
        return knight_y >= 0 and knight_y < mapSize and self.board[knight_y][knight_x] == 0

    def tryMove(self, x, y):
        global OPEN, CONSIDERED, solved, nc
        if (self.movable(x, y)):
            board_next = copy.copy(self.board)
            knight_x = (self.knight_x+x) % mapSize
            knight_y = self.knight_y+y
            board_next[self.knight_y][self.knight_x] = 1
            board_next[knight_y][knight_x] = 2
            if (self.isnotCONSIDERED(board_next)):
                if (abs(x) == 2):
                    B_next = Board(board_next, knight_x,
                                   knight_y, self.depth+1, self.goal)
                else:
                    B_next = Board(board_next, knight_x,
                                   knight_y, self.depth+1, self.goal)
                heapq.heappush(OPEN, [B_next.cost(), nc, B_next])
                CONSIDERED.append(board_next)
                nc += 1
                board_test = copy.copy(board_next)
                board_test[knight_y][knight_x] = 1
                if ((board_test == self.goal).all() and B_next.checkMate()):
                    solved = True

    def isnotCONSIDERED(self, board):
        board90 = np.rot90(board)
        return self.notin(board) and self.notin(np.rot90(board90)) and self.notin(np.flipud(board)) and self.notin(np.fliplr(board))

    def notin(self, board):
        for b in CONSIDERED:
            if ((board == b).all()):
                return False
        return True

    def cost(self):
        access = 0
        penalty = 0
        if (self.movable(-1, -2)):
            access += 1
        if (self.movable(1, -2)):
            access += 1
        if (self.movable(2, -1)):
            access += 1
        if (self.movable(2, 1)):
            access += 1
        if (self.movable(1, 2)):
            access += 1
        if (self.movable(-1, 2)):
            access += 1
        if (self.movable(-2, 1)):
            access += 1
        if (self.movable(-2, -1)):
            access += 1
        if (not access or penalty >= 2):
            return inf
        return 10*access + self.depth

    def checkMate(self):
        center = (mapSize-1)//2
        return (self.knight_x == (center-2)%mapSize and self.knight_y == center-1) or (self.knight_x == (center-1)%mapSize and self.knight_y == center-2) or (self.knight_x == (center-1)%mapSize and self.knight_y == center+2) or (self.knight_x == (center-2)%mapSize and self.knight_y == center+1) or (self.knight_x == (center+1)%mapSize and self.knight_y == center-2) or (self.knight_x == (center+2)%mapSize and self.knight_y == center-1) or (self.knight_x == (center+1)%mapSize and self.knight_y == center+2) or (self.knight_x == (center+2)%mapSize and self.knight_y == center+1)


def setInitBoard(center):
    board_init = np.zeros((mapSize, mapSize), dtype="int8")
    board_init[center][center] = 2
    return board_init


def setGoalBoard():
    board_goal = np.ones((mapSize, mapSize), dtype="int8")
    return board_goal


OPEN = []
CONSIDERED = []
solved = False


def execute(B_init):
    global OPEN, CONSIDERED, nc
    heapq.heappush(OPEN, [0, 0, B_init])
    CONSIDERED.append(B_init.board)
    while (len(OPEN)):
        element = heapq.heappop(OPEN)
        B = element[2]
        printBoard(B.board)
        expand(B)
        if (solved):
            return nc
    return -1


def expand(b):
    CONSIDERED.clear()
    b.tryMove(-1, -2)
    b.tryMove(1, -2)
    b.tryMove(2, -1)
    b.tryMove(2, 1)
    b.tryMove(1, 2)
    b.tryMove(-1, 2)
    b.tryMove(-2, 1)
    b.tryMove(-2, -1)


def printBoard(b):
    for y in range(mapSize):
        for x in range(mapSize):
            print(b[y][x], end='')
            print(' ', end='')
        print("\n")
    print(str(nc) + "\n")


def main():
    center = (mapSize-1)//2
    board_init = setInitBoard(center)
    board_goal = setGoalBoard()
    B_init = Board(board_init, center, center, 0, board_goal)
    execute(B_init)
    if (solved):
        printBoard(board_goal)
        print("solved!!")
        print(str(nc) + " pattern were considered")
    else:
        print("failed...")


if __name__ == "__main__":
    main()
