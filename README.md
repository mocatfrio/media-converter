### Multimedia Networking Project I
# Media Converter Web Application Using Python

By Group 3:
* 5115100043 - Hafara Firdausi
* 5115100069 - Pius Pambudi
* 5115100070 - Ahmad Burhanuddin Utomo
* 5115100117 - Cahya Putra Hikmawan

#### How to Deploy
1. Install Flask (in Linux environment)
    ```sh
    pip install flask
    ```
    p.s. You can using **virtualenv**

2. Install Python Library for Image Converter
    * Install **image**
      ```sh
      pip install image
      ```
3. Install Python Library for Audio Converter
    * Install **pydub**
      ```sh
      pip install pydub
      ```
    * Install **pydub dependency (ffmpeg & libavcodec-extra)**
      ```sh
      sudo apt-get install ffmpeg libavcodec-extra
      ```
4. Install Python Library for Video Converter
    * Install **ffmpy**
      ```sh
      pip install ffmpy
      ```
5. Set Flask APP and Flask ENV
    ```sh
    export FLASK_APP=media-converter.py
    export FLASK_ENV=development
    ```

    for windows
    ```sh
    set FLASK_APP=media-converter.py
    set FLASK_ENV=development
    ```
6. Run!
    ```sh
    flask run
    ```