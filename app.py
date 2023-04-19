from flask import Flask, render_template, request, url_for, redirect
import time

app = Flask(__name__)

# Game state variables
starting_player = None
pile_sizes = []
min_pick = None
max_pick = None
game_round = 0
game_started = False
game_completed = False
game_start_time = None
game_time_limit = None
game_timer = None
scores = {}
round_start_time = None
round_end_time = None
total_score_to_win = None
player1 = None
player2 = None
move = None
pile_num = None
current_player = None

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    return render_template('admin.html')

@app.route('/set_game_settings', methods=['POST'])
def set_game_settings():
    global pile_sizes
    global min_pick
    global max_pick
    global current_player
    global total_score_to_win
    global player1
    global player2
    
    pile_sizes.append(request.form['pile_size_1'])
    pile_sizes.append(request.form['pile_size_2'])
    pile_sizes.append(request.form['pile_size_3'])
    min_pick = int(request.form['min_stones'])
    max_pick = int(request.form['max_stones'])
    if request.form['first_player'] == 'player1':
        current_player = player1
    else:
        current_player = player2
    total_score_to_win = int(request.form['total_score_to_win'])
    return redirect(url_for('admin'))


@app.route('/playerOne', methods=['POST'])
def playerOne():
    global player1, current_player
    player1 = request.form['player_name']
    return render_template('playerOne.html', player1=player1, current_player=current_player)

@app.route('/playerOneInput', methods=['POST'])
def playerOneInput():
    global player1, current_player
    pile_num = request.form['pile_select']
    move = int(request.form['stone_number'])
    return render_template('playerOne.html', player1=player1, current_player=current_player)

@app.route('/playerTwo', methods=['GET', 'POST'])
def playerTwo():
    global player2, current_player
    player2 = request.form['player_name']
    return render_template('playerTwo.html', player2=player2, current_player=current_player)

@app.route('/playerTwoInput', methods=['POST'])
def playerTwoInput():
    global player2, current_player
    pile_num = request.form['pile_select']
    move = int(request.form['stone_number'])
    return render_template('playerTwo.html', player2=player2, current_player=current_player)

@app.route('/play', methods=['GET', 'POST'])
def play():
    global min_pick
    global max_pick
    global winner
    global scores
    global move
    global pile_num
    global player1
    global player2
    global current_player

    if request.method == 'GET':
        return render_template('play.html')
    else:
        # Get the number of stones in each pile from the form
        pile1 = pile_sizes[0]
        pile2 = pile_sizes[1]
        pile3 = pile_sizes[2]
        
        # Get the game settings from the form
        # min_pick = int(request.form['max_take'])
        # max_pick = int(request.form['min_take'])
        # total_score = int(request.form['total_score'])
        
        
        # Initialize the scores to 0
        scores = {
            player1: 0,
            player2: 0
        }
        # Play the game until one player reaches the total score
        while max(scores.values()) < int(total_score_to_win):
            # Display the current state of the game
            print(f'Player {current_player}\'s turn')
            print(f'Pile 1: {pile1}, Pile 2: {pile2}, Pile 3: {pile3}')
            print(f'Scores: {scores}')
            print(max(scores.values()))
            
            print('current_player '+current_player)
            # Wait for the players to make their move
            while move is None or pile_num is None:
                time.sleep(1)
            
            # Get the player's move from the form
            # move = int(request.form[f'{current_player}_move'])
            
            # Validate the player's move
            if move < min_pick or move > max_pick:
                print(f'Invalid move: {move}')
                move = None
                pile_num = None
                continue
            
            # Determine which pile the player is taking stones from
            # pile_num = int(request.form[f'{current_player}_pile'])
            if pile_num == 1:
                pile = pile1
            elif pile_num == 2:
                pile = pile2
            elif pile_num == 3:
                pile = pile3
            else:
                print(f'Invalid pile number: {pile_num}')
                move = None
                pile_num = None
                continue
            
            # Validate the player's move based on the number of stones in the pile
            if move > pile:
                print(f'Invalid move: {move}')
                move = None
                pile_num = None
                continue
            
            # Update the number of stones in the pile and the player's score
            if pile_num == 'pile1':
                pile1 -= move
            elif pile_num == 'pile2':
                pile2 -= move
            elif pile_num == 'pile3':
                pile3 -= move
            scores[current_player] += move
            
            # Switch to the other player's turn
            if current_player == player1:
                current_player = player2
            else:
                current_player = player1
            move = None
            pile_num = None
        
        # Determine the winner
        if scores[player1] > scores[player2]:
            winner = player1
        else:
            winner = player2
        
        # Display the winner and final scores
        print(f'{winner} wins!')
        print(f'Final scores: {scores}')
        
        return redirect(url_for('result', winner=winner, scores=scores))

@app.route('/result')
def result():
    return render_template('result.html', winner=winner, scores=scores)

@app.route('/')
def index():
    return render_template('index.html', player1=player1)

if __name__ == '__main__':
    app.run(debug=True)
