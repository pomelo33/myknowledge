from flask import Flask
import socket,os,redis

app = Flask(__name__)
r = redis.Redis(host='redis', port=6379)

@app.route('/')
def hello():
    count = r.incr('hits')
    return f"Hello from {os.getenv('HOSTNAME')}! Hits: {count}"
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)