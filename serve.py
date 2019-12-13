from flask import Flask, request, jsonify
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)

class word2vec(Resource):
    def get(self):
        return {
        "About":"the api to interact with word2vec",
        "Usage":{"input":"string", "output":"labled vectors"}
        }

    def post(self):
        print(request.json, request.data)
        #inputstr = request.get_json(force=True)
        #print(inputstr)
        #return jsonify("out",inputstr)

api.add_resource(word2vec, "/")

if __name__ == '__main__':
    app.run(debug=True)

"""
curl -g -X POST -d '{"hi":"tst", "hello":"nothin"}' -H 'Contentent-Type: application/json' http://127.0.0.1:5000/
curl -g -d '{"key1":"value1", "key2":"value2"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/
"""