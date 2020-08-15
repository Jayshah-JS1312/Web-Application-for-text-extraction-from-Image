import os
from flask import Flask,render_template,request
from ocr_core import ocr_core

upload_folder = '/static/uploads'

extensions = set(['png','jpg','jpeg'])

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1].lower() in extensions

@app.route('/',methods = ['GET','POST'])
def upload_image():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('upload.html',msg = "No file selected")
        file = request.files['file']

        if file.filename == '':
            return render_template('upload.html', msg='No file selected')
        
        if file and allowed_file(file.filename):
            extracted_text = ocr_core(file)
            return render_template('upload.html',
                                   msg='Successfully processed',
                                   extracted_text=extracted_text,
                                   img_src=upload_folder + file.filename)
    
    elif request.method == 'GET':
        return render_template('upload.html')

if __name__ == '__main__':
    app.run()