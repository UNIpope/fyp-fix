from flask import request
import flask
from word2v import api

app = flask.Flask(__name__)
app.config["DEBUG"] = True

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

app.run()
