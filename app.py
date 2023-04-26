from flask import Flask, render_template, request, url_for, redirect
import time, logging
from flask import jsonify
from flask import Response
from flask import session


app = Flask(__name__)
app.secret_key = 'your_secret_key'
logging.basicConfig(level=logging.DEBUG)
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
total_score_to_win = -1
player1 = None
player2 = None
move = -1
pile_num = None
current_player = None
winner = None
guess = None
score = 0
timer = 0
feedback = None
score1 = 0
score2 = 0
start_time = None
time_left = 30

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    global scores, total_score_to_win, pile_sizes, player1, player2
    return render_template('admin.html', scores=scores, total_score_to_win=total_score_to_win, pile_sizes=pile_sizes, player1=player1, player2=player2)
    return render_template('judge.html', player1=player1, player2=player2, time_remaining=timer)

@app.route('/set_game_settings', methods=['POST'])
def set_game_settings():
    global pile_sizes
    global min_pick
    global max_pick
    global current_player
    global total_score_to_win
    global player1
    global player2, timer
    
    pile_sizes.append(request.form['pile_size_1'])
    pile_sizes.append(request.form['pile_size_2'])
    pile_sizes.append(request.form['pile_size_3'])
    timer = pile_sizes[2]
    min_pick = int(request.form['min_stones'])
    max_pick = int(request.form['max_stones'])
    if request.form['first_player'] == 'player1':
        current_player = player1
    else:
        current_player = player2
    total_score_to_win = int(request.form['total_score_to_win'])
    return redirect(url_for('admin'))
    return render_template('judge.html', player1=player1, player2=player2, time_remaining=timer)

@app.route('/start_timer')
def start_timer():
    global start_time
    start_time = int(time.time() * 1000)
    return jsonify({'message': 'Timer started', 'start_time': start_time})


@app.route('/get_global_value')
def get_global_value():
    global time_left # replace this with your own function to get the global value
    return jsonify(global_value=time_left)

@app.route("/myFlaskRoute", methods=["POST"])
def myFlaskRoute():
    global time_left
    data = request.form.get("myData")
    time_left = data
    return "Data received from JavaScript"

@app.route('/stream_time')
def stream_time():
    def generate():
        while True:
            # start_time = session.get('start_time')
            # print(start_time)
            if start_time is not None:
                now = time.time()
                elapsed_time = int(now - start_time)
                yield f'data: {elapsed_time}\n\n'
            time.sleep(1)

    return Response(generate(), mimetype='text/event-stream')

@app.route('/playerOne', methods=['GET','POST'])
def playerOne():
    global player1, player2, current_player, timer, start_time, time_left
    player1 = player1 or request.form['player_name']
    time_left = time_left or 30
    return render_template('playerOne.html', player1=player1, player2=player2, current_player=current_player, score1=score1, time_left=time_left)

@app.route('/playerOneInput', methods=['POST'])
def playerOneInput():
    global player1, player2, current_player, pile_num, move, winner, scores, start_time, timer, time_left
    # pile_num = request.form['pile_select']
    move = int(request.form['stone_number'])
    time_left = int(request.form['time_left'])
    return redirect(url_for('playerOne', player1=player1, player2=player2, current_player=current_player, score1=score1, time_left=time_left))

@app.route('/playerTwo', methods=['GET', 'POST'])
def playerTwo():
    global player1, player2, current_player, timer, start_time, time_left, score2
    player2 = player2 or request.form['player_name']
    return render_template('playerTwo.html', player1=player1, player2=player2, current_player=current_player, score2=score2, time_left=time_left)

@app.route('/playerTwoInput', methods=['POST'])
def playerTwoInput():
    global player1, player2, current_player, pile_num, move, winner, scores, score, total_score_to_win, score1, score2, start_time, time_left
    # pile_num = request.form['pile_select']
    # move = int(request.form['stone_number'])
    guess = int(request.form['guess'])
    if (move + guess) % 2 == 0:
        score1 += 1
    else:
        score2 += 1
    print(score1, score2)
    return redirect(url_for('playerTwo', player1=player1, player2=player2, current_player=current_player, score2=score2, time_left=time_left))

    while score <= 0:
        guess = int(request.form['guess'])
        if abs(guess - int(move)) <= total_score_to_win:
            if guess == int(move):
                score += 50
            else:
                score += 10
        if guess < move:
            feedback = 'High'
        else:
            feedback = 'Low'
        if score <= 0:
            return render_template('playerTwo.html', test=player1, player2=player2, current_player=current_player, score=score, feedback=feedback)
    return render_template('result.html', score=score)
    
    # if winner:
    #     return render_template('result.html', winner=winner, player1=player1, player2=player2, score1=scores[player1], score2=scores[player2])
    # else:
    #     return render_template('playerTwo.html', player2=player2, current_player=current_player)

@app.route('/result')
def result():
    global winner, player1, player2, score1, score2
    if score1>score2:
        winner = player1
    else:
        winner = player2
    return render_template('result.html', winner=winner, player1=player1, player2=player2, score1=score1, score2=score2)

@app.route('/playGame', methods=['POST'])
def playGame():
    global min_pick
    global max_pick
    global winner
    global scores
    global move
    global pile_num
    global player1
    global player2
    global current_player

    app.logger.debug(request.method)
    app.logger.debug('Else condition')
    # Get the number of stones in each pile from the form
    pile1 = int(pile_sizes[0])
    pile2 = int(pile_sizes[1])
    pile3 = int(pile_sizes[2])
        
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
    app.logger.debug("Play function called")
    app.logger.debug(scores)
    app.logger.debug(total_score_to_win)
    app.logger.debug(pile_sizes)
    app.logger.debug(player1)
    app.logger.debug(player2)
    while max(scores.values()) < int(total_score_to_win):
        # Display the current state of the game
        print(f'Player {current_player}\'s turn')
        print(f'Pile 1: {pile1}, Pile 2: {pile2}, Pile 3: {pile3}')
        print(f'Scores: {scores}')
            
        # Wait for the players to make their move
        while move is None or pile_num is None:
            time.sleep(1)
            
        # print(move, pile_num)
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
        if pile_num == 'pile1':
            pile = pile1
        elif pile_num == 'pile2':
            pile = pile2
        elif pile_num == 'pile3':
            pile = pile3
        else:
            print(f'Invalid pile number: {pile_num}')
            move = None
            pile_num = None
            continue
        # print(pile)
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
        
    return render_template('result.html', winner=winner, player1=player1, player2=player2, score1=scores[player1], score2=scores[player2])

@app.route('/')
def index():
    global time_left, starting_player, pile_sizes, min_pick, max_pick, game_round, game_started, game_completed, game_start_time, game_time_limit, game_timer
    global scores, round_start_time, round_end_time, total_score_to_win, player1, player2, move, pile_num, current_player, winner, guess, score, timer, feedback, score1, score2, start_time
    # return render_template('index.html', player1=player1)
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
    total_score_to_win = -1
    player1 = None
    player2 = None
    move = -1
    pile_num = None
    current_player = None
    winner = None
    guess = None
    score = 0
    timer = 0
    feedback = None
    score1 = 0
    score2 = 0
    start_time = None
    time_left = 30
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
