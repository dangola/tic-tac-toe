import json


def ai_response(grid, move):
    def check_winner(grid):
        """ Check horizontal, vertical, diagonal win """
        if grid[0] == grid[1] == grid[2] != ' ':
            return grid[0]
        elif grid[3] == grid[4] == grid[5] != ' ':
            return grid[3]
        elif grid[6] == grid[7] == grid[8] != ' ':
            return grid[6]

        if grid[0] == grid[3] == grid[6] != ' ':
            return grid[0]
        elif grid[1] == grid[4] == grid[7] != ' ':
            return grid[1]
        elif grid[2] == grid[5] == grid[8] != ' ':
            return grid[2]

        if grid[0] == grid[4] == grid[8] != ' ':
            return grid[0]
        elif grid[2] == grid[4] == grid[6] != ' ':
            return grid[2]
        return ' '

    def ai_move(grid):
        for i in range(len(grid)):
            if grid[i] == ' ':
                return i
        return None

    if move is not None:
        if grid[move] != ' ':
            raise ValueError('Move not valid.')
        else:
            grid[move] = 'X'
            winner = check_winner(grid)
            if winner != ' ':
                return grid, winner
            if ai_move(grid) is not None:
                grid[ai_move(grid)] = 'O'
                winner = check_winner(grid)
            else:
                return grid, winner
    return grid, check_winner(grid)
