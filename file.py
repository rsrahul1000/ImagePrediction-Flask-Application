from flask import Flask, render_template, request, redirect, flash, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os 
import matplotlib.pyplot as plt
import numpy as np
import pickle
from keras.models import Sequential
from keras.models import model_from_json
from skimage import io
from scipy.misc import imresize


#This is done to disable GPU
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

UPLOAD_FOLDER = 'D:\Research\Clock_\static'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['filename'] = 'test.jpg'

model_file = open('Data/Model/model.json', 'r')
model = model_file.read()
model_file.close()
model = model_from_json(model)
model.load_weights("Data/Model/weights.h5")


###################################################
def get_img(data):
    # Getting image array from path:
    img_size = 64
    img = imresize(data, (img_size, img_size, 3))
    return img

def predict(filename):
    data = plt.imread(os.path.join(app.config['UPLOAD_FOLDER'], app.config['filename']))
    data = np.asarray(data)
    data = get_img(data)
    X = np.zeros((1, 64, 64, 3), dtype='float64')
    X[0] = data
    prediction = model.predict(X)
    Y = np.argmax(prediction, axis=1)
    Y = 'cat' if Y[0] == 0 else 'dog'
    return Y
###################################################

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
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], app.config['filename']))
            file.close()
            prediction = predict(app.config['filename'])
            return render_template('upload.html', args = "Given image is {}".format(prediction))
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