def ai_move(grid):
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

    move = {}
    move['grid'] = grid
    move['winner'] = ' '
    winner = check_winner(grid)
    if winner != ' ':
        move['winner'] = winner
        return move

    for i in range(len(grid)):
        if grid[i] == ' ':
            grid[i] = 'O'
            move['grid'] = grid
            move['winner'] = check_winner(grid)
            return move

    return move
