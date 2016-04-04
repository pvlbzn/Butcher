import os

from flask import Flask, render_template, request, redirect, \
        url_for, send_from_directory
from werkzeug import secure_filename

# TODO: Move to the settings.
UPLOAD_FOLDER = 'uploads/'
ALLOWED = set(['png', 'jpg'])

a = Flask(__name__)
a.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
a.config['MAX_CONTENT_LENGTH'] = 25 * 1024 * 1024

@a.route('/')
def index():
    return render_template('index.html')

@a.route('/upload', methods=['POST'])
def upload():
    uploaded = request.files.getlist("file[]")
    filenames = []
    for f in uploaded:
        if f and file_allowed(f.filename):
            filename = secure_filename(f.filename)
            f.save(os.path.join(a.config['UPLOAD_FOLDER'], filename))
            filenames.append(filename)
    return render_template('upload.html', filenames=filenames)

def file_allowed(fname):
    return '.' in fname and fname.rsplit('.', 1)[1] in ALLOWED

def rescale():
    pass
    return redirect(url_for('uploaded_file', filename=fname))

@a.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(a.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    a.run(
            host='0.0.0.0',
            port=int('8080'),
            debug=True,
        )
