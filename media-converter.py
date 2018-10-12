# import required libraries
from flask import Flask, render_template, request, redirect, send_from_directory, flash, url_for
from PIL import Image
import os
import pydub
import ffmpy

# define the temporary storage folder
UPLOAD_FOLDER = 'uploaded_files'

app = Flask(__name__)
app.secret_key = os.urandom(16)

# function for image conversion
def convert_image(filename, options):
    # load image file into temporary storage
    im = Image.open(os.path.join(UPLOAD_FOLDER, filename))

    # change the depth of image
    im = im.convert(options['depth'])

    # resize image
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

    # reformat image
    output = "out_" + filename.split(".")[0] + "." + options['format']
    if options['format']=="ico":
        size = [(width, height)]
        im.save(os.path.join(UPLOAD_FOLDER, output), sizes=size)
    else:
        im.save(os.path.join(UPLOAD_FOLDER, output))

    # send the output file
    return output

# function for audio conversion
def convert_audio(filename, options):
    # load audio file into temporary storage
    the_file = os.path.join(UPLOAD_FOLDER, filename)

    # get the audio file extension
    ext = filename.split(".")[1]

    # define audio segment
    sound = pydub.AudioSegment.from_file(the_file, ext)

    # define new name for output file
    output = "output_" + os.path.splitext(filename)[0] + "." + options['format']

    # define the output path
    new_path = os.path.join(UPLOAD_FOLDER, output)
    
    # change the audio format, audio sample rate, channel, and bitrate
    saved = sound.export(new_path, format=options['format'], bitrate=options['bitrate'], parameters=["-ac", options['channel'], "-ar", options['samplerate']])
    
    # delete the original file
    os.remove(the_file)

    # send the output file
    return output

# function for video conversion
def convert_video(filename, options):
    # load the video file into temporary storage
    input_file = os.path.join(UPLOAD_FOLDER, filename)

    # define output file name
    output_name = "converted_" + filename.split(".")[0] + "." + options['format']
    
    # define the output path
    output_file = os.path.join(UPLOAD_FOLDER, output_name)
    
    # change the video format, frame rate, frame size, aspect ratio, bitrate, audio channel, and audio sample rate
    ff = ffmpy.FFmpeg (
      inputs = {input_file: None},
      outputs = {output_name: '-vf "scale=' + options['framesize'] + ', setdar=' + options['aspect-ratio'] + '" -r ' + options['framerate'] + ' -b:v ' + options['bitrate'] + ' -ac ' + options['channel'] + ' -ar ' + options['samplerate']}
    )
    ff.run()

    # move the converted files
    os.rename(output_name, output_file)

    # send the output file
    return output_name

# Routing

@app.route('/')
# return index page (upload page)
def index():
    return render_template('upload.html')

@app.route('/download/<filename>')
# return download page
def download(filename):
    return render_template('download.html', filename=filename)

@app.route('/upload', methods=['POST'])
# function for uploading file
def upload():
    try:
        # get the file
        file = request.files['file']

        # get the filetype
        filetype = request.form['filetype']

        # save file into temporary storage
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))

        # check the filetype and call the conversion function
        if filetype == 'image':
            output = convert_image(file.filename, request.form)
        elif filetype == 'audio':
            output = convert_audio(file.filename, request.form)
        elif filetype == 'video':
            output = convert_video(file.filename, request.form)

        # redirect to the download page
        return redirect(url_for('download', filename=output))
    except:
        flash('Cannot convert file.', 'error')
        return redirect(url_for('index'))

@app.route('/file/<filename>')
# function for downloading file
def file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)