from flask import request
import flask
from flask_cors import CORS

from word2v import apiw2v
from testimagedec import apiim

from multiprocessing import Pool

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['CORS_HEADERS'] = 'Content-Type'
_pool = None


@app.route('/w2v', methods=['GET'])
def get_method_w2v():
    return {
    "About":"the api to interact with word2vec",
    "Usage":{"content":"string (The quick fox)", "output":"labled vectors"}
    }

@app.route('/imagee', methods=['GET'])
def get_method_image():
    return {
    "About":"the api to interact with image ",
    "Usage":{"images":["image", "image", "image"], "output":"lables"}
    }

@app.route('/compare', methods=['GET'])
def get_method_compare():
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

#curl -i -H "Content-Type: application/json" -X POST -d '{"content": "A short story is a piece of prose fiction that typically can be read in one sitting and focuses on a self-contained incident or series of linked incidents, with the intent of evoking a"}' http://localhost:5000/
@app.route('/w2v', methods=['POST'])
def post_method_w2v():
	#out = apiw2v(request.json["content"])
	#return out
	print(type(request.json["content"]))
	f = _pool.apply_async(apiw2v,[request.json["content"]])
	r = f.get()
	return r

@app.route('/image', methods=['POST', 'GET'])
def post_method_imagepred():
    out = apiim()
    return out

@app.route('/compare', methods=['POST'])
def post_method_compare():
    return 0

@app.route('/test', methods=['POST'])
def post_method_tester():
    import base64
    try:
        #imagefile = flask.request.files.get('imagefile', '')
        coded_string = request.json["image"]
        im = base64.b64decode(coded_string)
        import cv2 
        cv2.imshow("ada",im)
        key = cv2.waitKey(0)
    
    except Exception as err:
        print("------------")
        print(err)

    return 0


if __name__=='__main__':
	_pool = Pool(processes=4)
	try:
		# insert production server deployment code
		CORS(app)
		app.run()
	except KeyboardInterrupt:
		_pool.close()
		_pool.join()
