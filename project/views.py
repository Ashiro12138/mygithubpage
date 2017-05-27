from flask import Flask, render_template, session, redirect, url_for, escape, request, flash
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username']:
            session['username'] = request.form['username'][:20]
            return redirect(url_for('index'))
        else:
            flash("Please enter a valid username")
            return render_template('login.html')
    return render_template('login.html')

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/chat')
def chat():
    return render_template('chat.html')

@socketio.on('message')
def handleMessage(msg):
    if 'username' in session:
        print(session['username'])
    else:
        print('nothing')
    print('Message: ' + msg[:200])
    send(session['username']+": "+msg[:200], broadcast=True)


if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0',port=5000,debug=True)
