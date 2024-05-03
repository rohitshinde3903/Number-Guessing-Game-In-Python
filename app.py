from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = '123'

def initialize_game():
    session['computer'] = random.randint(1, 100)
    session['counter'] = 0
    session['guessed_numbers'] = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'computer' not in session:
        initialize_game()

    message = ""
    result = False
    retain_focus = False  # Flag to retain focus on input field
    if request.method == 'POST':
        guess = int(request.form['guess'])
        session['counter'] += 1
        session['guessed_numbers'].append(guess)

        if guess != session['computer']:
            if guess > session['computer']:
                message = "Guess lower"
            else:
                message = "Guess higher"
            retain_focus = True  # Set the flag to retain focus on input field
        else:
            message = "Correct guess! You guessed it in {} attempts.".format(session['counter'])
            result = True

    return render_template('index.html', message=message, result=result, counter=session.get('counter', 0),
                           guessed_numbers=session.get('guessed_numbers', []), retain_focus=retain_focus)

@app.route('/reset')
def reset():
    initialize_game()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
