import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
from werkzeug import secure_filename

# Initialize the Flask application
app = Flask(__name__)

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
    # name of the uploaded file
    file = request.files['file']
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        # Move the file form the temporal folder to the upload folder
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Redirect the user to the uploaded_file route, which
        # will basicaly show on the browser the uploaded file
        return "saved that photo!"
        return redirect(url_for('uploaded_file', filename=filename))

if __name__ == "__main__":
    app.run( host='172.16.223.189', port=8080, debug=True)
