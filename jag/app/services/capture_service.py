import datetime
import os
import time
import threading
from threading import subprocess


from flask import Blueprint, jsonify, render_template, request, \
    send_from_directory, app, current_app 
 
from ..frontend.routes import frontend
from ..configs.config import Config

capture_flag = False
capture_thread = None
capturing = threading.Event()
capturing.clear()
successful_capture = None
# https://pypi.org/project/asyncffmpeg/ UPGRADE TO THIS!


def capture(capture_url):
    global capturing, capture_thread, capture_flag, successful_capture

    # TMP
    print("Starting capture... active thread count: ", threading.active_count())
    print(' enumerate threads: ', threading.enumerate())


    while capturing.is_set():
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f"stream_snapshot_{timestamp}.png"
        filepath = os.path.join('/app/static/images', filename)
       
        command = [
            'ffmpeg',
            '-i', capture_url,
            '-ss', '0',
            '-vframes', '1',
            '-f', 'image2',
            '-update', '1',
            '-pix_fmt', 'yuv420p',
            filepath,
            '-loglevel', 'verbose',
            '-y'
        ]
        # # uuid = os.getuid()
        # # user = os.getlogin()
        # pwuid = pwd.getpwuid()
        # print("user info: ", pwuid)
       
        # print("command follows: ", command)
        print(f"Attempting to save image: {filename}...")
        start_time = time.time()
        time.sleep(1)
        try:
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode == 0:
                successful_capture = True
            else:
                print(f"FFmpeg failed with error: {result.stderr}")
                successful_capture = False
        except Exception as e:
            print(f"Unexpected error: {e}")
        finally:
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"ffmpeg took {elapsed_time:.2f} seconds")
            time.sleep(1)
    print("Stopping capture...")
    capture_thread = None

@frontend.route('/toggle-capture', methods=['POST'])
def toggle_capture():
    global capture_thread, capturing, capture_flag
    capture_url = request.form.get('rtmp_url', Config['CAPTURE_URL'])
    
    # capture_url = Config.CAPTURE_URL
    
    response = {'message': 'Capture toggled', 'isCapturing': capture_flag}
    
    if capturing.is_set():
        capturing.clear()
        capture_flag = False
    else:
        capturing.set()
        capture_flag = True

    # see if capture_thread is already created, if not make it
    try:
        if not capture_thread:
            capture_thread = threading.Thread(target=capture,
                                              args=(capture_url,))
            # start it regardless- because capturing condition is in the funciton.
            capture_thread.start()
    except Exception as e:
        print(f"Unexpected error: {e}")
        response = {'message': f'Failed to toggle capture: {str(e)}',
                    'isCapturing': capture_flag}

    return jsonify(response)



