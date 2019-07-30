
import heapq
import copy
import random
class EightPuzzle(object):

    def __init__(self, board):
        self.board = board

    def __init__(self):
        self.board = [[1,2,3],[4,5,6],[7,8,0]]

    def scramble(self,n):
        self.board=[[1,2,3],[4,5,6],[7,8,0]]
        for i in range(n):
            move=random.choice(self.moves(self.board))
            cpy=self.copy(self.board)
            self.board=self.perform_move(cpy,move)

    def copy(self,board):
        return copy.deepcopy(board)

    def game_over(self, board):
        if board==((1,2,3),(4,5,6),(7,8,0)):
            return True
        return False

    def manhattan_dist(self, num, curr_coord):
        exp_coord = {
            0: (2, 2),
            1: (0, 0),
            2: (0, 1),
            3: (0, 2),
            4: (1, 0),
            5: (1, 1),
            6: (1, 2),
            7: (2, 0),
            8: (2, 1)
        }
        return abs(curr_coord[0] - exp_coord.get(num)[0]) + abs(curr_coord[1] - exp_coord.get(num)[1])

    def heuristic(self, board):
        total_dist = 0
        for row in range(len(board)):
            for col in range(len(board[0])):
                total_dist += self.manhattan_dist(board[row][col], (row, col))
        return total_dist

    def moves(self, board):
        empty=self.find(board,0)
        ret = []
        # move down
        if empty[0] - 1 >= 0:
            ret.append(((1, 0),board[empty[0]-1][empty[1]],'down'))
        # move up
        if empty[0] + 1 <= 2:
            ret.append(((-1, 0),board[empty[0]+1][empty[1]],'up'))
        # move right
        if empty[1] - 1 >= 0:
            ret.append(((0, 1),board[empty[0]][empty[1]-1],'right'))
        # move left
        if empty[1] + 1 <= 2:
            ret.append(((0, -1),board[empty[0]][empty[1]+1],'left'))
        # format: (direction of the move, # of the tile moved)
        return ret


    def find(self,board,num):
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j]==num:
                    return i,j
        return -1,-1

    def perform_move(self, board, move):
        empty=self.find(board,0)
        num_moved=move[1]
        direction=move[0]
        ret = []
        for row in board:
            ret.append(list(row))
        ret[empty[0]][empty[1]]=num_moved
        ret[empty[0]-direction[0]][empty[1]-direction[1]]=0
        return self.board_to_tuple(ret)


    def board_to_tuple(self, board):
        ret = []
        for row in board:
            ret.append(tuple(row))
        return tuple(ret)


    def find_soln(self):
        d = dict() #keep the parent edges, pointing from child to parent
        s = dict() #nodes already visited, keep the one with least cost
        q = []
        heapq.heapify(q)
        hscore=self.heuristic(self.board)
        t=(hscore,self.board_to_tuple(self.board),0,(None,None,None))
        heapq.heappush(q,t)
        d[t]=None
        lastmove = None
        while len(q)!=0:
            # format of temp: h_score, board, g_score, move
            temp = heapq.heappop(q)
            g=temp[2]
            if temp[1] in s and s[temp[1]]<=temp[2]:
                continue
            elif self.game_over(temp[1]):
                lastmove=temp
                break
            else:
                s[temp[1]]=temp[2]
                for move in self.moves(temp[1]):
                    boardcpy=self.copy(temp[1])
                    boardcpy=self.perform_move(boardcpy,move)
                    h=self.heuristic(boardcpy)
                    t=(g+1+h,boardcpy,g+1,move)
                    d[t]=temp
                    heapq.heappush(q,t)
        if lastmove is None:
            return None
        res = []
        while lastmove is not None:
            res.append(lastmove[3][1:])
            lastmove = d.get(lastmove)
        res.reverse()
        # format: (# of the tile moved, direction)
        return res[1:]



m=[[0,1,3],[4,2,5],[7,8,6]]
p=EightPuzzle()
p.scramble(100)
print(p.board)
sol=p.find_soln()
print(sol)
print(len(sol))
