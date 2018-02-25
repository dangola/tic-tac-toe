import json


def ai_response(request):

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

    body = json.loads(request.body.decode('utf-8'))
    grid = body['grid']
    move = body['move']

    response = {}
    response['grid'] = grid
    response['winner'] = ' '

    if (move is None):
        return response
    winner = check_winner(grid)
    if winner != ' ':
        response['winner'] = winner
        return response

    for i in range(len(grid)):
        if grid[i] == ' ':
            grid[i] = 'O'
            response['grid'] = grid
            response['winner'] = check_winner(grid)
            return response

    return response
