from flask import request
import flask
from word2v import api

from flask_cors import CORS

from platform import python_version
print(python_version())

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['CORS_HEADERS'] = 'Content-Type'

#curl -i  -X GET http://localhost:5000/
@app.route('/', methods=['GET'])
def get_method():
    return {
    "About":"the api to interact with word2vec",
    "Usage":{"input":"string (/?text=The quick fox)", "output":"labled vectors"}
    }

#curl -i -H "Content-Type: application/json" -X POST -d '{"content": "A short story is a piece of prose fiction that typically can be read in one sitting and focuses on a self-contained incident or series of linked incidents, with the intent of evoking a"}' http://localhost:5000/
@app.route('/', methods=['POST'])
def post_method():
    out = api(request.json["content"])
    return out

CORS(app)
app.run()
