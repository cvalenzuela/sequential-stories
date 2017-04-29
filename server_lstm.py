#
# This server classifies an images and then runs a lstm network over it.
#

import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
from werkzeug import secure_filename
from lstm import lstmText

# Keras
from keras.applications.resnet50 import ResNet50
from keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np

# Some file reading and image stuff
from keras.preprocessing import image
from io import BytesIO
from PIL import Image
import base64

# Initialize the Flask application
app = Flask(__name__)
ip = '172.16.220.175'

# Load the RESNET model
model = ResNet50(weights='imagenet')

# path to the upload directory
app.config['UPLOAD_FOLDER'] = 'uploads/'
# extension accepted to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route("/")
def hello():
    return "Server Running..."

# process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    Get the image data from the POST
    data = request.form['img']
    # This decodes it into an image
    img = Image.open(BytesIO(base64.b64decode(data)))
    # Resize to 224x224 and make sure it's RGB
    img = img.resize((224,224))
    img = img.convert("RGB")
    # Turn it into a matrix (224x224x3)
    x = image.img_to_array(img)
    # Add a dimension to make it (1x224x224x3)
    x = np.expand_dims(x, axis=0)
    # This remaps the pixel values to a negative<->positive range
    x = preprocess_input(x)
    # Get a prediction
    preds = model.predict(x)
    # decode the results into a list of tuples (class, description, probability)
    preds = decode_predictions(preds, top=3)[0]
    data = []
    generated_text = lstmText(preds)
    term = " ".join(preds[0][1].split("_")).capitalize()

    for pred in preds:
        data.append({'id': pred[0], 'term': pred[1], 'score': float(pred[2])})

    return jsonify(status='got image',prediction=data, text=generated_text, term=term)

if __name__ == "__main__":
    app.run(host=ip, port=8080, debug=False)
