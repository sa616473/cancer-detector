from flask import Flask, render_template, request


from werkzeug.utils import secure_filename
import os
import requests
import base64

app = Flask(__name__)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])

def predictor():

    predictor_dict = {
        'df': 'Dermatofibroma (df)',
        'akiec':  'Actinic keratoses and intraepithelial carcinoma (akiec)',
        'mel': 'Melanoma (mel)',
        'bcc':  'Basal cell carcinoma (bcc)',
        'bkl':  'Benign keratosis-like lesions (bkl)',
        'vasc': 'Vascular lesions (vasc)',
        'nv': 'Melanocytic nevi (nv)'
    }
    f = request.files['file']
    basepath = os.path.dirname(__file__)
    print(basepath)
    file_path = os.path.join(basepath, 'uploads', 'uploaded.png')
    f.save(file_path)
    print(file_path)

    binaryContent = open(file_path, 'rb')
    myobj = {"files": binaryContent,"containHeatMap":True}

    mURL = "https://ac922.mapsysinc.com/visual-insights/api/dlapis/0230d128-dc6c-4474-89ef-80b59ee57386"
    resultSource = requests.post(mURL, files=myobj, verify=True)
    resultsPack = resultSource.json()
    # print(resultsPack)
    heatmap = resultsPack.get('heatmap')
    heatmapData = heatmap.replace('data:image/png;base64,', '')
    imgdata = base64.b64decode(heatmapData)

    modelResult = resultsPack.get('classified')
    keyValues = list(modelResult.keys())
    confidence = float(modelResult[keyValues[0]])
    prediction = predictor_dict[keyValues[0]]

    heatpath = 'output/' + 'output' + '.png'
    with open(heatpath, "wb") as fh:
        fh.write(imgdata)
        fh.close()
    
    response = {
        'prediction': prediction,
        'confidence': confidence,
        'heatmappath': heatpath,
    }
    
    return response

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(port=port)

# def model_predict():
#     # Get the file from post request
#     f = request.files['file']

#     # Save the file to ./uploads
#     basepath = os.path.dirname(__file__)
#     file_path = os.path.join(basepath, 'uploads', secure_filename(f.filename))
#     f.save(file_path)
#     print(file_path)

#     img = image.load_img(file_path, target_size=(32,32))
#     x = image.img_to_array(img)
#     x = x / 255.
#     x = x[np.newaxis, :, :, :1]

#     out = model.predict(x)
#     print(out)
#     response = classes.iloc[(np.argmax(out))][1]
#     print(response)
#     return response

