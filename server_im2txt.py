#
# This server runs im2txt over a saved image
#

import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
from werkzeug import secure_filename
import subprocess
from verbs import verbs
from phrases import start, continuation, restart, end, finish
from random import choice

# Initialize the Flask application
app = Flask(__name__)
ip = '172.16.220.175'

# path to the upload directory
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']) # extension accepted to be uploaded

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route("/")
def hello():
    print(current_text)
    return "Server Running..."

@app.route('/upload', methods=['POST'])
def upload():
    print("Upload Requested ")
    file = request.files['file']
    name = request.form.getlist('name')[0]
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename) # Make the filename safe, remove unsupported chars
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'image.jpg'))
        # run the classification
        cmd = ['im2txt/models/im2txt/bazel-bin/im2txt/run_inference --checkpoint_path="im2txt/trained/model.ckpt-3000000" --vocab_file="im2txt/trained/word_counts.txt" --input_files="uploads/image.jpg"']
        p = subprocess.check_output(cmd, shell=True)
        # get the result
        result = str(p,'utf-8')
        result = result.split("0)")[1].split("(")[0].strip().split(".")[0].strip()
        if (name == '1'):
            result = choice(start) + " " + result # It all began when a woman standing on a beach with a dog
        elif (name == '2'):
            result = " " + choice(verbs["verbs"])["past"] + " " + result + "." # arranged a group of people sitting around a table.
        elif (name == '3'):
            result = " " + choice(continuation) + " " + result  # But for a brief moment, a small bird sitting on top of a wooden bench
        elif (name == '4'):
            result = " " + choice(verbs["verbs"])["past"] + " " + result + "." # blinked a man sitting on top of a wooden bench next to a tree.
        elif (name == '5'):
            result = " " + choice(restart) + " " + result # Since then, a group of people sitting around a table eating food
        elif (name == '6'):
            result = " " + choice(verbs["verbs"])["past"] + " " + result + "." # battled a close up of a person holding a pair of scissors.
        elif (name == '7'):
            result = " " + choice(end) + " " + result  # From then on, a group of people standing on top of a sandy beach
        elif (name == '8'):
            result = " " + choice(verbs["verbs"])["past"] + " " + result + "." # haunted a close up of a television set with a keyboard.
        elif (name == '9'):
            result = " " + choice(finish) + " " + result + "." # Now, a bike is parked next to a fence.
        print(result)
        return jsonify(status="got text", text=result)

if __name__ == "__main__":
    app.run(host=ip, port=8080, debug=False)
