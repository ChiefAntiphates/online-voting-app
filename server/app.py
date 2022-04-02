from distutils.log import debug
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO



app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000")

button_clicks = 0

@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/test')
def my_test():
    socketio.emit('test_topic', 'Success!!!', namespace='/testnp')
    return jsonify(body='This works!'), 200

@app.route('/click')
def click():
    global button_clicks
    button_clicks += 1
    socketio.emit('clicked', {"number": button_clicks}, namespace='/button_clicks')
    return jsonify(body="You clicked the button", clicks=button_clicks)

if __name__ == '__main__':
    app.debug=True
    socketio.run(app)

