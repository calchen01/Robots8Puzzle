class EightTileGame(object):

    def __init__(self, board):
        self.board = board

    def copy(self):
        return copy.deepcopy(self)

    def game_over(self):
        if (self.board[0] == [0, 1, 2]) and (self.board[1] == [3, 4, 5]) and (self.board[2] == [6, 7, 8]):
            return True
        return False

    def manhattan_dist(num, curr_coord):
        exp_coord = {
            0: (0, 0),
            1: (0, 1),
            2: (0, 2),
            3: (1, 0),
            4: (1, 1),
            5: (1, 2),
            6: (2, 0),
            7: (2, 1),
            8: (2, 2)
        }
        return abs(curr_coord[0] - exp_coord.get(num)[0]) + abs(curr_coord[1] - exp_coord.get(num)[1])

    def heuristic(self):
        total_dist = 0
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                total_dist += manhattan_dist(self.board[row][col], (row, col))
        return total_dist

    def neighbors(curr_coord):
        ret = []
        if curr[0] - 1 >= 0:
            ret.append((curr[0] - 1, curr[1]))
        if curr[0] + 1 <= 2:
            ret.append((curr[0] + 1, curr[1]))
        if curr[1] - 1 >= 0:
            ret.append((curr[0], curr[1] - 1))
        if curr[1] + 1 <= 2:
            ret.append((curr[0], curr[1] + 1))
        return ret

    def is_legal_move(self, tile_to_move_coord):
        for neighbor in neighbors(tile_to_move_coord):
            if self.board[neighbor[0]][neighbor[1]] == 0:
                return True
        return False

    def legal_moves(self):
        ret = []
        for row in range(2):
            for col in range(2):
                if self.is_legal_move((row, col)):
                    ret.append((row, col))
        return ret

    def perform_move(self, tile_to_move_coord):
        if self.is_legal_move(tile_to_move_coord):
            for neighbor in neighbors(tile_to_move_coord):
                if self.board[neighbor[0]][neighbor[1]] == 0:
                    self.board[neighbor[0]][neighbor[1]] = self.board[tile_to_move_coord[0]][tile_to_move_coord[1]]
                    self.board[tile_to_move_coord[0]][tile_to_move_coord[1]] = 0
        else:
            print("illegal move")

    def board_to_tuple(self):
        ret = []
        for row in self.board:
            ret.append(tuple(row))
        return tuple(ret)

    # consider iterative deepening, depth-limited needed?
    def find_soln(self, depth):
        frontier = [self]
        # board -> (move, last board)
        # the keys act as a set of visited nodes
        pred = {self.board_to_tuple() : (None, None)}
        curr_depth = 0
        while len(frontier) > 0:
            curr = frontier.pop(0)
            if curr.game_over():
                return backtrack(pred, curr.board_to_tuple())
            if curr_depth == depth:
                evaluate_options()
            for move, new_board in curr.successors():
                if (new_board.board_to_tuple() not in pred.keys()):
                    frontier.append(new_board)
                    pred[new_board.board_to_tuple()] = (move, curr.board_to_tuple())
        return None

    def backtrack(pred, goal):
        path = []
        curr = goal
        while curr != None:
            path.insert(0, pred[curr][0])
            curr = pred[curr][1]
        path.remove(None)
        return path