from flask import request
import flask

app = flask.Flask(__name__)
app.config["DEBUG"] = True

#curl -i  -X GET http://localhost:5000/
@app.route('/', methods=['GET'])
def get_method():
    return {
	"About": "The api to compare image results to the text vectors",
	"Usage": {
		"image": ["cat", "dog ", "jumper", "dog"],
		"content": [{
				"word": {
					"0": "or",
					"1": "incident",
					"2": "intent",
					"3": "one",
					"4": "fiction"
				}
			},
			{
				"x1": {
					"0": -0.5332247615,
					"1": -1.1958338022,
					"2": 1.170817852,
					"3": -1.3924382925,
					"4": 0.1888926923
				}
			},
			{
				"x2": {
					"0": -1.8791081905,
					"1": -0.850225091,
					"2": -0.2876406908,
					"3": 0.7106280327,
					"4": -1.7247616053
				}
			}
		]
	}
}

def compare(image, content):
    print(image, content)
    return "sdfhhjk"


#curl -i -H "Content-Type: application/json" -X POST -d '{"image": ["cat", "dog ", "jumper", "dog"],"content": [{"word": {"0": "or","1": "incident","2": "intent","3": "one","4": "fiction"}},{"x1": {"0": -0.5332247615,"1": -1.1958338022,"2": 1.170817852,"3": -1.3924382925,"4": 0.1888926923}},{"x2": {"0": -1.8791081905,"1": -0.850225091,"2": -0.2876406908,"3": 0.7106280327,"4": -1.7247616053}}]}' http://localhost:5000/
@app.route('/', methods=['POST'])
def post_method():
    out = compare(request.json["image"], request.json["content"])
    return out

app.run()



