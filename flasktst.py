from flask import request
import flask
from word2v import api

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/')
def main_method():
    text = request.args.get('text')

    if text is None:
        return {
        "About":"the api to interact with word2vec",
        "Usage":{"input":"string (/?text=The quick fox)", "output":"labled vectors"}
        }
    else:
        out = api(text)
        print("text is not ")
        return out

app.run()
