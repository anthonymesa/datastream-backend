from flask import Flask

HOST_PORT=8080

app = Flask(__name__)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=HOST_PORT)

