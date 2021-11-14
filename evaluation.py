from grid import Grid

MAX_TILE_CREDIT = 10e4
WEIGHT_MATRIX = [
    [2048, 1024, 64, 32],
    [512, 128, 16, 2],
    [256, 8, 2, 1],
    [4, 2, 1, 1]
]


class Evaluation:

    def __init__(self) -> None:
        self.ROW        = 4
        self.COLUMN     = 4

    def evaluate(self, grid: Grid):
        """Evaluate the grid board based on some pre-defined heuristic functions"""
        empty = self.empty_tiles(grid)
        position = self.max_tile_position(grid)
        weighted_sum = self.weighted_board(grid)
        smooth = self.smoothness(grid)
        mono = self.monotonicity(grid)

        # TODO: should use weights to measure heuristics
        return empty + position + weighted_sum + smooth + mono

    def empty_tiles(self, grid):
        """Return the number of empty tiles on the grid board"""
        return grid.get_num_empty_tiles()

    def max_tile_position(self, grid):
        """Return an significantly large negative when the max tile is not on the desired corner, vice versa"""
        board = grid.board
        max_tile = max(max(board, key=lambda x: max(x)))

        # Considered with the WEIGHT_MATRIX, always keep the max tile in the corner
        if board[0][0] == max_tile:
            return MAX_TILE_CREDIT
        else:
            return -MAX_TILE_CREDIT

    def weighted_board(self, grid):
        """Perform point-wise product on the grid board and a pre-defined weight matrix"""
        ROW, COLUMN = self.ROW, self.COLUMN
        board = grid.board

        result = 0
        for i in range(ROW):
            for j in range(COLUMN):
                result += board[i][j] * WEIGHT_MATRIX[i][j]

        # Larger result means better
        return result

    def smoothness(self, grid):
        """Smoothness heuristic measures the difference between neighboring tiles and tries to minimize this count"""
        board = grid.board
        ROW, COLUMN = self.ROW, self.COLUMN
        smoothness = 0
        
        for r in board:
            for i in range(COLUMN - 1):
                smoothness += abs(r[i] - r[i + 1])
                pass
        for j in range(ROW):
            for k in range(COLUMN - 1):
                smoothness += abs(board[k][j] - board[k + 1][j])

        return smoothness

    def monotonicity(self, grid):
        """Monotonicity heuristic tries to ensure that the values of the tiles are all either increasing or decreasing along both the left/right and up/down directions"""
        board = grid.board
        ROW, COLUMN = self.ROW, self.COLUMN
        mono = 0
        
        for r in board:
            diff = r[0] - r[1]
            for i in range(COLUMN - 1):
                if (r[i] - r[i + 1]) * diff <= 0:
                    mono += 1
                diff = r[i] - r[i + 1]

        for j in range(ROW):
            diff = board[0][j] - board[1][j]
            for k in range(COLUMN - 1):
                if (board[k][j] - board[k + 1][j]) * diff <= 0:
                    mono += 1
                diff = board[k][j] - board[k + 1][j]

        return mono

