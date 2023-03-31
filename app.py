# from __future__ import division, print_function
# coding=utf-8
import os
import numpy as np

# Keras
from keras.models import load_model
import keras.utils as image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
# Define a flask app
app = Flask(__name__)

#MAP
predictor_dict = {
        0 : 'Dermatofibroma (df)',
        1 :  'Actinic keratoses and intraepithelial carcinoma (akiec)',
        2 : 'Melanoma (mel)',
        3:  'Basal cell carcinoma (bcc)',
        4:  'Benign keratosis-like lesions (bkl)',
        5: 'Vascular lesions (vasc)',
        6: 'Melanocytic nevi (nv)'
    }

# Model saved with Keras model.save()
MODEL_PATH = './models/model_skin_cancer.h5'

# Load your trained model
model = load_model(MODEL_PATH)
# model._make_predict_function()          # Necessary
print('Model loaded. Start serving...')

print('Model loaded. Check http://127.0.0.1:5000/')


def model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(100,75))
    # Preprocessing the image
    x = image.img_to_array(img)
    mean = 159.88411714650246
    std = 46.45448942251337
    x = (x - mean) / std
    x = x.reshape(75, 100, 3)
    x = np.expand_dims(x, axis=0)

    preds = model.predict(x)
    return preds


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path, model)

        # Process your result for human
        pred_class = np.argmax(preds[0])
        result = predictor_dict[pred_class]               # Convert to string
        return result
    return None

if __name__ == '__main__':
    app.run(debug=True)

