from flask import Flask
from flask_cors import CORS
from image_recog import image_recog
from data_graph import data_graph

# 플라스크 앱 생성
app = Flask(__name__)
app.register_blueprint(image_recog)
app.register_blueprint(data_graph)


CORS(app)
if __name__ == '__main__': 
	app.run(host="0.0.0.0", debug=False, port=5000)
