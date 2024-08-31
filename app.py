from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

# Initialize the board
def initialize_board():
    return [[str(3 * j + i + 1) for i in range(3)] for j in range(3)]

# Check victory
def victory_for(board, sgn):
    who = 'me' if sgn == 'X' else 'you'
    cross1 = cross2 = True
    for rc in range(3):
        if board[rc][0] == sgn and board[rc][1] == sgn and board[rc][2] == sgn:
            return who
        if board[0][rc] == sgn and board[1][rc] == sgn and board[2][rc] == sgn:
            return who
        if board[rc][rc] != sgn:
            cross1 = False
        if board[2 - rc][2 - rc] != sgn:
            cross2 = False
    if cross1 or cross2:
        return who
    return None

# Make a list of free fields
def make_list_of_free_fields(board):
    free = []
    for row in range(3):
        for col in range(3):
            if board[row][col] not in ['O', 'X']:
                free.append((row, col))
    return free

# Make a move for the computer
def draw_move(board):
    free = make_list_of_free_fields(board)
    if free:
        row, col = random.choice(free)
        board[row][col] = 'X'

# Flask routes
@app.route('/')
def index():
    board = initialize_board()
    return render_template('index.html', board=board, message="Your turn", winner=None)

@app.route('/move', methods=['POST'])
def move():
    board = [[request.form.get(f'{row}{col}', str(3 * row + col + 1)) for col in range(3)] for row in range(3)]
    row = int(request.form.get('row'))
    col = int(request.form.get('col'))
    
    if board[row][col] not in ['O', 'X']:
        board[row][col] = 'O'
        winner = victory_for(board, 'O')
        if not winner:
            draw_move(board)
            winner = victory_for(board, 'X')
    
    if winner:
        message = "You won!" if winner == 'you' else "I won"
    elif not make_list_of_free_fields(board):
        message = "Tie!"
        winner = "Tie"
    else:
        message = "Your turn"
    
    return render_template('index.html', board=board, message=message, winner=winner)

if __name__ == '__main__':
    app.run(debug=True)
