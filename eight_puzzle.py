import copy, heapq, random

class EightPuzzle(object):

    def __init__(self, board):
        self.board = board

    def get_board(self):
        return self.board

    def copy(self, board):
        return copy.deepcopy(board)

    def game_over(self, board):
        if board == ((1, 2, 3), (4, 5, 6), (7, 8, 0)):
            return True
        return False

    def manhattan_dist(self, num, curr_coord):
        exp_coord = {
            1: (0, 0),
            2: (0, 1),
            3: (0, 2),
            4: (1, 0),
            5: (1, 1),
            6: (1, 2),
            7: (2, 0),
            8: (2, 1),
            0: (2, 2)
        }
        return abs(curr_coord[0] - exp_coord.get(num)[0]) + abs(curr_coord[1] - exp_coord.get(num)[1])

    def heuristic(self, board):
        total_dist = 0
        for row in range(len(board)):
            for col in range(len(board[0])):
                total_dist += self.manhattan_dist(board[row][col], (row, col))
        return total_dist

    def find(self, board, num):
        for row in range(len(board)):
            for col in range(len(board[0])):
                if board[row][col] == num:
                    return row, col
        return -1, -1

    def moves(self, board):
        empty = self.find(board, 0)
        moves = []
        # move down
        if empty[0] - 1 >= 0:
            moves.append(((1, 0), board[empty[0] - 1][empty[1]], "down"))
        # move up
        if empty[0] + 1 <= 2:
            moves.append(((-1, 0), board[empty[0] + 1][empty[1]], "up"))
        # move right
        if empty[1] - 1 >= 0:
            moves.append(((0, 1), board[empty[0]][empty[1] - 1], "right"))
        # move left
        if empty[1] + 1 <= 2:
            moves.append(((0, -1), board[empty[0]][empty[1] + 1], "left"))
        # format: (direction of the move, # of the tile moved)
        return moves

    def board_to_tuple(self, board):
        ret = []
        for row in board:
            ret.append(tuple(row))
        return tuple(ret)
        
    def perform_move(self, board, move):
        empty = self.find(board, 0)
        num_moved = move[1]
        direction = move[0]
        ret = []
        for row in board:
            ret.append(list(row))
        ret[empty[0]][empty[1]] = num_moved
        ret[empty[0] - direction[0]][empty[1] - direction[1]] = 0
        return self.board_to_tuple(ret)

    def scramble(self, n):
        for i in range(n):
            move = random.choice(self.moves(self.board))
            cpy = self.copy(self.board)
            self.board = self.perform_move(cpy, move)

    def find_soln(self):
        pred = dict() # keep the parent edges, pointing from child to parent
        g_scores = dict() # keys represent nodes (board) already visited, values are g_scores, keep the one with the least cost
        queue = []
        heapq.heapify(queue)
        h_score = self.heuristic(self.board)
        head = (h_score, self.board_to_tuple(self.board), 0, (None, None, None))
        heapq.heappush(queue, head)
        pred[head] = None
        last_move = None
        while len(queue) > 0:
            # format of curr: h_score, board, g_score, move
            curr = heapq.heappop(queue)
            g_score = curr[2]
            if curr[1] in g_scores and g_scores[curr[1]] <= curr[2]:
                continue
            elif self.game_over(curr[1]):
                last_move = curr
                break
            else:
                g_scores[curr[1]] = curr[2]
                for move in self.moves(curr[1]):
                    boardcpy = self.copy(curr[1])
                    boardcpy = self.perform_move(boardcpy, move)
                    h_score = self.heuristic(boardcpy)
                    successor = (g_score + 1 + h_score, boardcpy, g_score + 1, move)
                    pred[successor] = curr
                    heapq.heappush(queue, successor)
        if last_move is None:
            return None
        commands = []
        while last_move is not None:
            commands.append(last_move[3][1:])
            last_move = pred.get(last_move)
        commands.reverse()
        # format: (# of the tile moved, direction)
        return commands[1:]

'''
game = EightPuzzle([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
game.scramble(100)
commands = game.find_soln()
print(game.get_board())
print(len(commands))
print(commands)
'''