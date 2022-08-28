"""
Routes and views for the flask application.
"""
import docx
from datetime import datetime
from flask import render_template,request,jsonify,send_from_directory   
from FlaskWebProject2 import app
from werkzeug.utils import secure_filename
import os.path
from os import path
import os  
from simpletransformers.classification import ClassificationModel
from sklearn.model_selection import train_test_split



#train_args ={'reprocess_input_data': True,
#             'fp16':False,
#             'num_train_epochs': 15}


#model = ClassificationModel(
#    'bert',model_name='checkpoint-32070-epoch-15',
#    num_labels=39,
#    args=train_args,
#    use_cuda=False,cache_dir=os.path.join(app.config['CONTENT_FOLDER'] ,'/outputs/checkpoint-32070-epoch-15')
#)

train_args ={"reprocess_input_data": True,
             "fp16":False,
             "num_train_epochs": 15}


model = ClassificationModel(
    "bert", "/content/outputs/checkpoint-32070-epoch-15",
    num_labels=39,
    args=train_args,
    use_cuda=False
)

@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static','images'), 'favicon.png', mimetype='image/png')
@app.route('/', methods = ['GET','POST'])
def upload():
    #msg = ''
    if request.method == 'POST':  
        f = request.files['file']
        filename = secure_filename(f.filename)
        print(filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        #msg = f.filename
        usrInput = getText(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        usrOutput = DoWork(usrInput)
        return jsonify(usrInput=usrInput[101:110],usrOutput=usrOutput)
    return render_template('upload.html',year = datetime.utcnow().year)
  
def getText(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return fullText


def DoWork (text):
    predictions, raw_outputs = model.predict(text[101:110])
    return predictions
