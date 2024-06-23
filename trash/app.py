from flask import Flask,  jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

# take environment variables from .env.
load_dotenv()

app = Flask(__name__)
cors = CORS(app)


@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "msg": "Welcome to ResumeRanker API",
        "success": "success"
    })


@app.route('/', defaults={'u_path': ''})
@app.route('/<path:u_path>')
def allroutes(u_path):
    return jsonify({
        "msg": "bad request",
        "success": "failed",
        "error": "404 | url not found",
    })


def fixBaseDirectory(array=[], rootPath=''):
    for x in array:
        future_dir = os.path.join(rootPath, x)
        if not os.path.isdir(future_dir):
            os.system(f"mkdir {future_dir}")
    print('base directory initialized')

if __name__ == '__main__':
    app.config['CORS_HEADERS'] = 'Content-Type'
    port = int(os.environ.get('PORT', 5000))

    rootPath = os.path.abspath(os.path.dirname(__file__))

    fixBaseDirectory([
        'storage',
        'storage\input',
        'storage\output',
        'storage\masks'
    ], rootPath)

    # app.run(host='127.0.0.1', port=port, debug=True)
