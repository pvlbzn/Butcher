import os

from flask import Flask, render_template, request, \
    redirect, url_for, send_from_directory
from werkzeug import secure_filename

UPLOAD_FOLDER = 'uploads/'
ALLOWED = set(['png', 'jpg'])

a = Flask(__name__)
a.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@a.route('/')
def index():
    return render_template('index.html')

@a.route('/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded file
    file = request.files['file']
    # Check it
    if file and file_allowed(file.filename):
        fname = secure_filename(file.filename)
        file.save(os.path.join(a.config['UPLOAD_FOLDER'], fname))
        return redirect(url_for('uploaded_file', filename=fname))

def file_allowed(fname):
    return '.' in fname and fname.rsplit('.', 1)[1] in ALLOWED

@a.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(a.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    a.run(
            host='0.0.0.0',
            port=int('8080'),
            debug=True,
        )
