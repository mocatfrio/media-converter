from flask import Flask, render_template, request, redirect, send_from_directory, flash, url_for
import os

UPLOAD_FOLDER = 'uploaded_files'

app = Flask(__name__)
app.secret_key = os.urandom(16)

def convert_image(filename, options):
    pass

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