from flask import Flask
import socket,os

app = Flask(__name__)

@app.route('/')
def hello():
    # return f"Hello from {socket.gethostname()}!"
    return f"Hello from {os.getenv('HOSTNAME')}!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)