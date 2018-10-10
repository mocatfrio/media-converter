from flask import Flask, render_template, request, redirect, send_from_directory, flash, url_for
from PIL import Image
import os
import pydub
import ffmpy

UPLOAD_FOLDER = 'uploaded_files'

app = Flask(__name__)
app.secret_key = os.urandom(16)

def convert_image(filename, options):
    #load image
    #print os.path.join(UPLOAD_FOLDER, filename)
    im = Image.open(os.path.join(UPLOAD_FOLDER, filename))
    #print "bug"
    #change depth
    im = im.convert(options['depth'])
    #print "bug"
    #resize
    width, height = im.size
    width = int(width*int(options['res'])/100)  
    height = int(height*int(options['res'])/100)
    if options['resx'] and options['resx']:
        width = int(options['resx'])
        height = int(options['resy'])
    sampling = str(options['sampling'])
    if sampling=="NEAREST":
        im = im.resize((width,height), Image.NEAREST)
    elif sampling=="BILINEAR":
        im = im.resize((width,height), Image.BILINEAR)
    elif sampling=="BICUBIC":
        im = im.resize((width,height), Image.BICUBIC)
    elif sampling=="ANTIALIAS":
        im = im.resize((width,height), Image.ANTIALIAS)
    #print "bug"
    #reformat
    output = "out_" + filename.split(".")[0] + "." + options['format']
    if options['format']=="ico":
        size = [(width, height)]
        im.save(os.path.join(UPLOAD_FOLDER, output), sizes=size)
    else:
        im.save(os.path.join(UPLOAD_FOLDER, output))
    #print "bug"
    return output

def convert_audio(filename, options):
    #load_audio_files
    the_file = os.path.join(UPLOAD_FOLDER, filename)
    #get_extention
    ext = filename.split(".")[1]
    #define_segment
    sound = pydub.AudioSegment.from_file(the_file, ext)
    #define_new_name
    output = "output_" + os.path.splitext(filename)[0] + "." + options['format']
    #define_path_to_save
    new_path = os.path.join(UPLOAD_FOLDER, output)
    #change_format, audio_sample_rate, channel, bitrate
    saved = sound.export(new_path, format=options['format'], bitrate=options['bitrate'], parameters=["-ac", options['channel'], "-ar", options['samplerate']])
    #delete_old_files
    os.remove(the_file)
    return output

def convert_video(filename, options):
    #load video files
    input_file = os.path.join(UPLOAD_FOLDER, filename)
    #define output name
    output_name = "converted_" + filename.split(".")[0] + "." + options['format']
    #define path to save
    output_file = os.path.join(UPLOAD_FOLDER, output_name)
    #converting
    ff = ffmpy.FFmpeg (
      inputs = {input_file: None},
      outputs = {output_name: '-vf "scale=' + options['framesize'] + ', setdar=' + options['aspect-ratio'] + '" -r ' + options['framerate'] + ' -b:v ' + options['bitrate'] + ' -ac ' + options['channel'] + ' -ar ' + options['samplerate']}
    )
    ff.run()
    #move the converted files into uploaded folder
    os.rename(output_name, output_file)
    return output_name

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

        #return nama file baru
        if filetype == 'image':
            output = convert_image(file.filename, request.form)
        elif filetype == 'audio':
            output = convert_audio(file.filename, request.form)
        elif filetype == 'video':
            output = convert_video(file.filename, request.form)

        return redirect(url_for('download', filename=output))
    except:
        flash('Cannot convert file.', 'error')
        return redirect(url_for('index'))

@app.route('/file/<filename>')
def file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)