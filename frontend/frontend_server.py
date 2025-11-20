from flask import Flask, send_from_directory
import os

app = Flask(__name__, static_folder='.')

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

if __name__ == "__main__":
    app.run(
        host="10.50.166.219",
        port=3000,
        ssl_context="adhoc",
        debug=False
    )
