from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
from dotenv import load_dotenv
import voting_utils as utils
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'



socketio = SocketIO(app, cors_allowed_origins=os.getenv('CLIENT_URL')or"http://localhost:3000")

button_clicks = 0

print("loaded.")

@app.route('/')
def hello_world():
    print("I got it!")
    return ("hello")


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
    socketio.run(app, host='0.0.0.0', port=os.getenv('SERVER_PORT') or 5000)

