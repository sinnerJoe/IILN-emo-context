import flask
from flask import Flask
from flask import request
from flask import jsonify
import classifier
import process_data

app = Flask(__name__)


# @app.route('/', methods=['GET'])
# def get_index_page():
#     return app.send_static_file('index.html')


@app.route('/emotion', methods=['POST'])
def post_emotion():
    data = request.get_json()
    sentence = process_data.process(data)
    response = {"emotion" : classifier.naive_bayes(sentence)}
    return jsonify(response)