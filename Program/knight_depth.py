import queue
import copy
import numpy as np

mapSize = 5
nc = 0


class Board:
    def __init__(self, board, x, y, depth, goal):
        self.board = board
        self.knight_x = x
        self.knight_y = y
        self.depth = depth
        self.goal = goal

    def movable(self, x, y):
        knight_x = self.knight_x + x
        knight_y = self.knight_y + y
        return knight_x >= 0 and knight_x < mapSize and knight_y >= 0 and knight_y < mapSize and self.board[knight_y][knight_x] == 0

    def tryMove(self, x, y):
        global OPEN, CONSIDERED, solved, nc
        if (self.movable(x, y)):
            board_next = copy.copy(self.board)
            knight_x = self.knight_x+x
            knight_y = self.knight_y+y
            board_next[self.knight_y][self.knight_x] = 1
            board_next[knight_y][knight_x] = 2
            if (self.isnotCONSIDERED(board_next)):
                B_next = Board(board_next, knight_x, knight_y,
                               self.depth+1, self.goal)
                OPEN.put(B_next)
                CONSIDERED.append(board_next)
                nc += 1
                board_test = copy.copy(board_next)
                board_test[knight_y][knight_x] = 1
                if ((board_test == self.goal).all()):
                    solved = True

    def isnotCONSIDERED(self, board):
        return self.notin(board) and self.notin(np.rot90(board)) and self.notin(np.rot90(board, 2)) and self.notin(np.rot90(board, 3)) and self.notin(np.flipud(board)) and self.notin(np.fliplr(board)) and self.notin(np.fliplr(np.rot90(board))) and self.notin(np.flipud(np.rot90(board)))

    def notin(self, board):
        for b in CONSIDERED:
            if ((board == b).all()):
                return False
        return True


OPEN = queue.LifoQueue()
CONSIDERED = []
solved = False


def setInitBoard(center):
    board_init = np.zeros((mapSize, mapSize), dtype="int8")
    board_init[center][center] = 2
    return board_init


def setGoalBoard():
    board_goal = np.ones((mapSize, mapSize), dtype="int8")
    return board_goal


def execute(B_init):
    global OPEN, CONSIDERED, nc
    OPEN.put(B_init)
    while (not OPEN.empty()):
        b = OPEN.get()
        printBoard(b.board)
        expand(b)
        if (solved):
            return nc
    return -1


def expand(b):
    CONSIDERED.clear()
    b.tryMove(-2, -1)
    b.tryMove(-1, -2)
    b.tryMove(-2, 1)
    b.tryMove(-1, 2)
    b.tryMove(2, -1)
    b.tryMove(1, -2)
    b.tryMove(2, 1)
    b.tryMove(1, 2)


def printBoard(b):
    for y in range(mapSize):
        for x in range(mapSize):
            print(b[y][x], end='')
            print(' ', end='')
        print("\n")
    print(str(nc) + "\n")


def main():
    center = (mapSize - 1) // 2
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
