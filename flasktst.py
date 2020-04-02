from flask import request
import flask
from flask_cors import CORS

from word2v import multiprocw2v
from testimagedec import multiprocim

import time
import base64, re
from io import BytesIO
from PIL import Image

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/w2v', methods=['GET'])
def get_method_w2v():
    return {
    "About":"the api to interact with word2vec",
    "Usage":{"content":"string (The quick fox)", "output":"labled vectors"}
    }

@app.route('/image', methods=['GET'])
def get_method_image():
    return {
    "About":"the api to interact with image ",
    "Usage":{"images":["image", "image", "image"], "output":"{im :pred}"}
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
	out = multiprocw2v(request.json["content"])
	return out

def decode_im(coded_string):
	IMAGE_SHAPE = (224, 224)

	base64_data = re.sub('^data:image/.+;base64,', '', coded_string)
	byte_data = base64.b64decode(base64_data)
	image_data = BytesIO(byte_data)
	image = Image.open(image_data).resize(IMAGE_SHAPE)
	image = image.convert("RGB")

	t = time.time()
	image.save("test_img\\"+str(t) + '.png', "PNG")

	return image


@app.route('/image', methods=['POST'])
def post_method_imagepred():
	coded_string = request.json["image"]
	image = decode_im(coded_string)

	out = multiprocim(image)
	print(out)
	out = {"im":out}
	return out

@app.route('/compare', methods=['POST'])
def post_method_compare():
    return 0

@app.route('/test', methods=['POST'])
def post_method_tester():
	import base64, re
	from io import BytesIO
	from PIL import Image
	

	coded_string = request.json["image"]
	base64_data = re.sub('^data:image/.+;base64,', '', coded_string)
	byte_data = base64.b64decode(base64_data)
	image_data = BytesIO(byte_data)

	img = Image.open(image_data)

	t = time.time()
	img.save("test_img\\"+str(t) + '.png', "PNG")


	time.sleep(3)
	return {"G":"gg"}

if __name__=='__main__':
	CORS(app)
	app.run(threaded=False)
