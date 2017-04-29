#
# This server runs im2txt over a saved image
#

import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
from werkzeug import secure_filename
import subprocess

# Initialize the Flask application
app = Flask(__name__)
ip = '172.16.220.175'

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

@app.route('/upload', methods=['POST'])
def upload():
    print("Upload Requested ")
    file = request.files['file']
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'image.jpg'))
        # run the classification
        cmd = ['im2txt/models/im2txt/bazel-bin/im2txt/run_inference --checkpoint_path="im2txt/trained/model.ckpt-3000000" --vocab_file="im2txt/trained/word_counts.txt" --input_files="uploads/image.jpg"']
        p = subprocess.check_output(cmd, shell=True)
        # get the result
        result = str(p,'utf-8')
        result = result.split("0)")[1].split("(")[0].strip().capitalize()
        return jsonify(status="got text", text=result)

if __name__ == "__main__":
    app.run(host=ip, port=8080, debug=False)
