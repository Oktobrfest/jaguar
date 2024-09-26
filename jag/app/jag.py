# import ast
# import base64
# import io
# import logging
# import os
# import re
# import subprocess
# import sys
# import threading
# import time
# import urllib  # Moved urllib here as it's a standard library import
# from datetime import datetime
# from threading import Thread, Lock
# from typing import Any


# import ffmpeg
# import flask
# import langchain
# import numpy as np
# import openai
# import pytesseract
# from PIL import Image
# from flask import Blueprint, jsonify, render_template, request, \
#     send_from_directory, app, current_app  # Combined Flask imports into one line
# from google.cloud import aiplatform, vision  # Alphabetized
# from langchain.chains import RetrievalQA
# from langchain.output_parsers import PydanticOutputParser  # Removed duplicate StrOutputParser
# from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
# from langchain_community.llms.vertexai import VertexAI  # Moved before langchain_google_vertexai
# from langchain_google_vertexai import ChatVertexAI 
# from langchain_openai import ChatOpenAI, OpenAI
# from pydantic import BaseModel, Field, ValidationError, field_validator, \
#     ValidationInfo  # Combined Pydantic imports into one line


# from .configs.config import Config
# from .zstream import Zstream

# import pwd

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))



# streamList = []
# zstream = Zstream()

# frontend = Blueprint('frontend', __name__, template_folder="templates/%s" % current_app.config['SITE_CONFIG']['template_folder'],
#                      static_folder="static")


# @frontend.route("/", methods=["GET", "POST"], endpoint="home")
# def home():
#     return flask.render_template(
#         'main.html.j2',
#         items = zstream.getStreamNames(),
#         configuration = current_app.config['SITE_CONFIG']
#     )


# @frontend.route("/player/<appname>/<streamname>", methods=["GET", "POST"],
#                 endpoint="player")
# def player(appname, streamname):
#     page = flask.render_template(
#         'player.html.j2',
#         streamname = streamname,
#         appname = appname,
#         configuration = current_app.config['SITE_CONFIG']
#     )
#     return page


# @frontend.route("/setup_helper", methods=["GET", "POST"],
#                 endpoint="setup_helper")
# def setup_helper():
#     page = flask.render_template(
#         'setup_helper.html.j2',
#         configuration = current_app.config['SITE_CONFIG']
#     )
#     return page


# @frontend.route('/static/<path:path>')
# def send_static(path):
#     return send_from_directory('static', path)


# # Render AI Webpage
# @frontend.route("/ai", methods=["GET", "POST"], endpoint="ai")
# def ai():
#     page = flask.render_template(
#         'ai.html.j2',
#         configuration = current_app.config['SITE_CONFIG']
#     )
#     return page


# @frontend.route('/images/<path:filename>')
# def download_file(filename):
#     return send_from_directory(OUTPUT_DIR, filename, as_attachment=True)


# @frontend.route("/favicon.ico")
# def favicon():
#     return send_from_directory(
#         os.path.join(frontend.root_path, "static"),
#         "favicon.ico",
#         mimetype="image/vnd.microsoft.icon",
#     )


# #local OCR
# @frontend.route('/do-ocr', methods=['POST'])
# def do_ocr():
#     files = [os.path.join('/app/static/images', f) for f in
#              os.listdir('/app/static/images') if f.endswith('.png')]
#     if not files:
#         return jsonify({'error': 'No images found'}), 404

#     latest_image_path = sorted(files)[-1]

#     try:
#         img = Image.open(latest_image_path)
#         text = pytesseract.image_to_string(img)
#         return jsonify({'extracted_text': text})
#     except FileNotFoundError:
#         return jsonify({'error': 'Image not found'}), 404
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500


# class Question(BaseModel):
#     cleaned_question: str = Field(
#         description="The extracted question from the text")
#     # question_type: str = Field(description="The type of question")
#     answer_section: str = Field(
#         description="The section of the text providing possible answers and any additional "
#                     "info related to the question")


# class Answer(BaseModel):
#     proposed_answer: Any = Field(
#         description="AI's proposed answer to the question of any format")
#     answer_confidence: float = Field(
#         description="Confidence level of the AI on the proposed answer")

#     #  alternate_answer: str = Field(description="Alternate answer if confidence is below a threshold", default="")

#     @field_validator('answer_confidence')
#     def confidence_must_be_reasonable(cls, value):
#         if not (0 <= value <= 100):
#             raise ValueError("Confidence must be between 0 and 100 percent")
#         return value

# # use this for cheap lookups/testing
# # gpt_model = "gpt-4o-mini"

# # the real deal
# # gpt_model = "gpt-4"
# # newest one (unverified)
# gpt_model = "gpt-4o"

# gpt_max_tokens = 1024


# llm = ChatOpenAI(model=gpt_model, temperature=0.2, max_tokens=gpt_max_tokens,
#                  openai_api_key=openai.api_key)

# @frontend.route('/submit-ocr', methods=['POST'])
# def submit_ocr():  # rename to extract_question later
#     question_text = request.form['question_text']
#     topics = "coding, " + request.form['topics']

#     prompt_text = """
#                       Look over this Text... ---
#                       Text Blob: {question_text}
#                       """

#     try:
#         # question_parser = JsonOutputFunctionsParser()
#         #   question_parser = PydanticOutputParser(pydantic_object=Question)

#         prompt = PromptTemplate(
#             template=prompt_text,
#             input_variables=["question_text", "topics"],
#             #    partial_variables={"format_instructions": question_parser.get_format_instructions()},
#         )

#         chain = prompt | llm  #| question_parser

#         llm_reply = chain.invoke(
#             {"topics": topics, "question_text": question_text})

#         result = {
#             "cleaned_question": llm_reply.content,
#             "answer_section": " Not today- llm_json.answer_section_json"
#         }

#         return jsonify(result)

#     except Exception as e:  # Add error handling for unexpected issues
#         return jsonify({'error': str(e)}), 500


# @frontend.route('/get-answer', methods=['POST'])
# def get_answer():
#     clean_question = request.form['extracted_question']
#     # extracted_answer_section = request.form['extracted_answer_section']

#     # prompt_text = """ Answer this question and give a confidence level. Question: {clean_question}\n Additional Information/Answer Options: {extracted_answer_section}
#     #                      """

#     prompt_text = """ Answer this question and give a confidence level. """

#     try:
#         #   answer_parser = PydanticOutputParser(pydantic_object=Answer)

#         prompt = PromptTemplate(
#             template=prompt_text,
#             input_variables=["clean_question"],
#             # partial_variables={"format_instructions": question_parser.get_format_instructions()},
#         )

#         chain = prompt | llm  #| answer_parser

#         llm_reply = chain.invoke({"clean_question": clean_question})

#         return jsonify({"ai_answer": llm_reply.content})

#     except Exception as e:  # Add error handling for unexpected issues
#         return jsonify({'error': str(e)}), 500
#     # end of WORKS!!



