from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def word2vecapi():
    if request.method == 'POST':
        return {"input":"string", "output":"labled vectors"}
    elif request.method == 'GET':
        return {
        "About":"the api to interact with word2vecdada",
        "Usage":{"input":"string", "output":"labled vectors"}
        }


if __name__ == '__main__':
    app.run(debug=True)

"""
curl -g -X POST -d '{"hi":"tst", "hello":"nothin"}' -H 'Contentent-Type: application/json' http://127.0.0.1:5000/
curl -g -d '{"key1":"value1", "key2":"value2"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/
"""