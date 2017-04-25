import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
from werkzeug import secure_filename

# ML stuff
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
    return "data"

# process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    # Get the image data from the POST
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

    # This is a little goofy but we need to convert it to something that works
    # with jsonify. Python sets do not and also numpy float32's do not
    # So made a list of little dictionaries
    data = []
    for pred in preds:
        data.append({'id': pred[0], 'term': pred[1], 'score': float(pred[2])})
    # resutl
    print(data)
    return jsonify(status='got image',prediction=data)

    # # name of the uploaded file
    # file = request.files['file']
    # print(file)
    # # Check if the file is one of the allowed types/extensions
    # if file and allowed_file(file.filename):
    #     # Make the filename safe, remove unsupported chars
    #     filename = secure_filename(file.filename)
    #     # Move the file form the temporal folder to the upload folder
    #     file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    #     # Redirect the user to the uploaded_file route, which
    #     # will basicaly show on the browser the uploaded file
    #     return "image saved"
    #     #print(data)
    #     #return redirect(url_for('uploaded_file', filename=filename))

if __name__ == "__main__":
    app.run( host='172.16.223.189', port=8080, debug=False)
