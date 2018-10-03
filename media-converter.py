from flask import Flask, render_template, request, redirect, send_from_directory, flash, url_for
from PIL import Image
import os

UPLOAD_FOLDER = 'uploaded_files'

app = Flask(__name__)
app.secret_key = os.urandom(16)

def convert_image(filename, options):
  #load image
  print os.path.join(UPLOAD_FOLDER, filename)
  im = Image.open(os.path.join(UPLOAD_FOLDER, filename))
  print "bug"
  #change depth
  im = im.convert(options['depth'])
  print "bug"
  #resize
  width, height = im.size
  width = int(width*int(options['res'])/100)  
  height = int(height*int(options['res'])/100)
  im = im.resize((width,height), Image.NEAREST)
  print "bug"
  #reformat
  output ="out_"+filename.split(".")[0]+"."+options['format']
  im.save(os.path.join(UPLOAD_FOLDER, output))
  print "bug"

def convert_audio(filename, options):
    pass

def convert_video(filename, options):
    pass

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/download/<filename>')
def download(filename):
    return render_template('download.html', filename=filename)

@app.route('/upload', methods=['POST'])
def upload():
    try:
        file = request.files['file']
        filetype = request.form['filetype']
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))

        if filetype == 'image':
            convert_image(file.filename, request.form)
        elif filetype == 'audio':
            convert_audio(file.filename, request.form)
        elif filetype == 'video':
            convert_video(file.filename, request.form)

        return redirect(url_for('download', filename=file.filename))
    except:
        flash('Cannot convert file.', 'error')
        return redirect(url_for('index'))

@app.route('/file/<filename>')
def file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)