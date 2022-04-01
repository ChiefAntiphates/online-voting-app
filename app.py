from distutils.log import debug
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO



app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000")

@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/test')
def my_test():
    socketio.emit('test_topic', 'Success!!!')
    return jsonify(body='This works!'), 200

if __name__ == '__main__':
    app.debug=True
    socketio.run(app)

