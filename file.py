from flask import Flask, render_template, request, redirect, flash, url_for
from werkzeug.utils import secure_filename
import os 

UPLOAD_FOLDER = 'D:\Research\Clock_\static'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload')
def upload_file():
   return render_template('upload.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No File Found')
            return render_template('upload.html', args = 'File Not found')
        file = request.files['file']
        if file.filename == '':
            flash('No file selected')
            return render_template('upload.html', args = 'File Not found')
        if file and allowed_file(file.filename):
            # filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], "test.png"))
            file.close()
            return render_template('upload.html', args = 'File Uploaded Successfully')
        return render_template('upload.html', args = 'File Not of Proper Format')

@app.route('/')
def index():
    return render_template('upload.html', args = 'Reupload Pls')

@app.route('/processing', methods=['POST'])
def processing():
    return render_template('display.html', args = 'Starting to Pre-Process')

if __name__ == '__main__':
   app.secret_key = os.urandom(24)
   app.config['SESSION_TYPE'] = 'filesystem'
   app.run(debug = True)