import base64
import io
import json
import os
import re
import time
from datetime import datetime
from typing import List, Dict, Any
import flask

from flask import current_app, jsonify, request, Response
from PIL import Image
from werkzeug.utils import secure_filename

import httpx
import langchain
import openai
from langchain_core.messages import HumanMessage
from langchain_google_vertexai import ChatVertexAI
from langchain_openai import ChatOpenAI, OpenAI

from ..zstream import Zstream


# was throwing errors for images, try setting static
# api = flask.Blueprint('api', __name__)
zstream = Zstream()

# NOT SURE IF TO USE THIS WAY OR VIA: current_app.config['STATIC_FOLDER??']
api = flask.Blueprint('api', __name__, static_folder=current_app.static_folder)





@api.route(current_app.config['API_PATH'] + "/streams/", methods=['GET'])
def api_list_streams():
    streams = []
    for stream in zstream.getStreamNames():
        streams.append({'app': stream[0], 'name': stream[1]})
    return construct_response(streams)


@api.route(current_app.config['API_PATH'] + "/streams/<stream_name>/", methods=['GET'])
def api_stream(stream_name):
    # Filter for streams with 'name' == stream_name
    stream = list(filter(lambda stream: stream['name'] == stream_name, zstream.getStreams()))
    return construct_response(stream)


@api.route('/api/images')
def list_images():
    image_folder = os.path.join(current_app.static_folder, 'images')
    # img_folder = os.path.join(app.root_path, "static")
    images = [
        {
            'original': f'/static/images/{filename}'
        }
        for filename in os.listdir(image_folder) if filename.endswith(('png', 'jpg', 'jpeg'))
    ]
    return jsonify(images)


# for testing (cheaper)
# didnt work
# google_model = "code-gecko@001"
# google_model = "text-bison@001"

# Cheaper Testing Model (UNTESTED), probably not cheapest!!
# google_model = "gemini-1.0-pro"

# OLD (APPARENTLY) for production:
# google_model = "gemini-pro-vision"
# for production:
google_model = "gemini-1.5-flash"

# use this for cheap lookups/testing
# gpt_model = "gpt-4o-mini"

gpt_max_tokens = 4024



@api.route('/upload_cropped', methods=['POST'], endpoint="upload_cropped")
def upload_cropped():
    if 'images' not in request.files:
        return jsonify({'error': 'No images provided'}), 400

    images = request.files.getlist('images')

    # create the cropped group folder
    timestamp = datetime.now().strftime("%Y-%m-%d-time-%H-%M-%S")

    new_images_dir = current_app.config['CROPPED_IMAGES_FOLDER']


    # content = []
    # for image in images:
    #     secured_filename = secure_filename(image.filename)
    #     filename = f"pic--{secured_filename}"
    #     save_path = os.path.join(new_images_dir, filename)

    #     # Open the image using PIL
    #     with Image.open(image.stream) as image_data:
    #         image_data.save(save_path)
    #         # Save the image to a byte array
    #         img_byte_arr = io.BytesIO()
    #         image_data.save(img_byte_arr, format='PNG')
    #         # Encode the image to base64 directly from memory
    #         encoded_image = base64.b64encode(img_byte_arr.getvalue()).decode(
    #             'utf-8')
    #         encoded_image = f"data:image/png;base64,{encoded_image}"

    #         content.append({
    #             "type": "image_url",
    #             "image_url": {"url": encoded_image},
    #         })

    #         # if GoogleAI:
    #         #     content.append({
    #                 #             "text": image_tag
    #                 #         })

    # content.append({
    #     "type": "text",
    #     "text": prompt_txt,
    # })
    
    # TEMP BSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS
    # gpt_llm = 5
    
    # raw_gpt_answer = ask_ai_human_msg(gpt_llm, content)
    # parsed_answer = parse_response(raw_gpt_answer)

    # gpt_answer = { 'gpt': parsed_answer }

    # google_llm = ChatVertexAI(model_name=google_model)
    # raw_google_answer = ask_ai_human_msg(google_llm, content)



    # google_parsed_answer = parse_response(raw_google_answer)

    # google_answer = {'google': google_parsed_answer}

    # combo_answer = {**gpt_answer, **google_answer}


    # return jsonify({"ai_response": combo_answer})

    return jsonify({"ai_response": "AAAAAAAAAAAAAAAAA TMP BS AAAAAAAAAAA"})



def construct_response(streams: List[Dict[str, Any]]) -> Response:
    """
    Constructs a JSON response from a list of stream dictionaries.

    Args:
        streams (List[Dict[str, Any]]): A list of dictionaries representing streams.
            Each dictionary is expected to be JSON-serializable.

    Returns:
        Response: A Flask Response object containing the JSON-encoded streams.
    """
    response_data = {"streams": streams}
    return jsonify(response_data)


# NEEDS RE-DOING!!! HIGH PRIORITY!!!!!!!!!!!!!!!!!!!!!!!!!!!
@api.route('/capture-status')
def get_capture_status():
    # global capture_flag, successful_capture

    # TEMP---- NEEDS TO BE RE-DONE PROPERLY!
    capture_flag = False
    successful_capture = False

    time.sleep(25)
    return jsonify({
        'isCapturing': capture_flag,
        'successfulCapture': successful_capture
    })