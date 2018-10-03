# Multimedia Networking

### Media Converter Using Python

#### How to Deploy?
1. Install Flask
```sh
pip install flask
```
for windows, Download

2. Install Python Library for Audio Converter

- Install **pydub**
```sh
pip install pydub
```

- Install **pydub dependency (ffmpeg & libavcodec-extra)**
```sh
sudo apt-get install ffmpeg libavcodec-extra
```

3. Set Flask APP and Flask ENV
```sh
export FLASK_APP=media-converter.py
export FLASK_ENV=development
```

for windows
```sh
set FLASK_APP=media-converter.py
set FLASK_ENV=development
```

4. Run!
```sh
flask run
```