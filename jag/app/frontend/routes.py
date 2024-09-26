# Standard Library Imports
import ast
import base64
import io
import logging
import os
import re
import subprocess
import sys
import threading
import time
import urllib  # Moved urllib here as it's a standard library import
from datetime import datetime
from threading import Thread, Lock
from typing import Any
import pwd

# Third-Party Library Imports
import ffmpeg
import flask
import langchain
import numpy as np
import openai
import pytesseract
from PIL import Image
from flask import Blueprint, jsonify, render_template, request, \
    send_from_directory, app, current_app, g
from google.cloud import aiplatform, vision  # Alphabetized
from langchain.chains import RetrievalQA
from langchain.output_parsers import PydanticOutputParser  # Removed duplicate StrOutputParser
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_community.llms.vertexai import VertexAI  # Moved before langchain_google_vertexai
from langchain_google_vertexai import ChatVertexAI 
from langchain_openai import ChatOpenAI, OpenAI
from pydantic import BaseModel, Field, ValidationError, field_validator, \
    ValidationInfo
from flask_login import current_user, login_required, logout_user

# Local Imports
from ..configs.config import Config
from ..zstream import Zstream
from ..services.ocr_service import perform_ocr
from ..ai.prompt_builder import PromptBuilder, Meta
from ..models import Prompt, Users
from ..database import session


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

streamList = []
zstream = Zstream()

frontend = Blueprint('frontend', __name__, template_folder="../templates/%s" % current_app.config['SITE_CONFIG']['template_folder'],
                     static_folder="../static")


@frontend.route("/", methods=["GET", "POST"], endpoint="home")
def home():
    return flask.render_template(
        'main.html.j2',
        items=zstream.getStreamNames(),
        configuration=current_app.config['SITE_CONFIG'],
        user=current_user,
    )


@frontend.route("/player/<appname>/<streamname>", methods=["GET", "POST"],
                endpoint="player")
def player(appname, streamname):
    page = flask.render_template(
        'player.html.j2',
        streamname=streamname,
        appname=appname,
        configuration=current_app.config['SITE_CONFIG'],
        user=current_user,
    )
    return page


@frontend.route("/setup_helper", methods=["GET", "POST"],
                endpoint="setup_helper")
def setup_helper():
    page = flask.render_template(
        'setup_helper.html.j2',
        configuration = current_app.config['SITE_CONFIG'],
        user=current_user,
    )
    return page


@frontend.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


# Render AI Webpage
@frontend.route("/ai", methods=["GET", "POST"], endpoint="ai")
def ai():
    page = flask.render_template(
        'ai.html.j2',
        configuration=current_app.config['SITE_CONFIG'],
        user=current_user,
    )
    return page


@frontend.route('/images/<path:filename>')
def download_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


@frontend.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(frontend.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


#local OCR
@frontend.route('/do-ocr', methods=['POST'])
def do_ocr():
    image_folder = current_app.config['CAPTURE_IMAGE_DESTINATION']
    try:
        extracted_text = perform_ocr(image_folder)
        return jsonify({'extracted_text': extracted_text})
    except FileNotFoundError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


class Question(BaseModel):
    cleaned_question: str = Field(
        description="The extracted question from the text")
    # question_type: str = Field(description="The type of question")
    answer_section: str = Field(
        description="The section of the text providing possible answers and any additional "
                    "info related to the question")


class Answer(BaseModel):
    proposed_answer: Any = Field(
        description="AI's proposed answer to the question of any format")
    answer_confidence: float = Field(
        description="Confidence level of the AI on the proposed answer")

    #  alternate_answer: str = Field(description="Alternate answer if confidence is below a threshold", default="")

    @field_validator('answer_confidence')
    def confidence_must_be_reasonable(cls, value):
        if not (0 <= value <= 100):
            raise ValueError("Confidence must be between 0 and 100 percent")
        return value

# use this for cheap lookups/testing
# gpt_model = "gpt-4o-mini"

# the real deal
# gpt_model = "gpt-4"
# newest one (unverified)
gpt_model = "gpt-4o"

gpt_max_tokens = 1024


llm = ChatOpenAI(model=gpt_model, temperature=0.2, max_tokens=gpt_max_tokens,
                 openai_api_key=openai.api_key)

@frontend.route('/submit-ocr', methods=['POST'])
def submit_ocr():  # rename to extract_question later
    question_text = request.form['question_text']
    topics = "coding, " + request.form['topics']

    prompt_text = """figure out what these characters are"""

    #  WORKS. JUST NEEDS REFACTORING.
    # try:
    #     # question_parser = JsonOutputFunctionsParser()
    #     #   question_parser = PydanticOutputParser(pydantic_object=Question)
    #
    #     # prompt = PromptTemplate(
    #     #     template=prompt_text,
    #     #     input_variables=["question_text", "topics"],
    #     #     #    partial_variables={"format_instructions": question_parser.get_format_instructions()},
    #     # )
    #
    #     # Prompt text is retrieved from DB based on either settings in
    #     # 'settings' or something set in the form submission. For now just
    #     # hard code something.
    #     input_variables = ["question_text", "topics"]
    #     meta = Meta(depends='PromptTemplate')
    #     prompt = PromptBuilder.create_prompt(prompt_text, input_variables, meta)
    #
    #     # Here somewhere construct BOTH a 'Question' object  AND a
    #     # Question_Chain Object(parent) & save them both to the
    #     # DB,
    #     # where the answer will also append to.
    #
    #     chain = prompt.langchain_prompt | llm  # | question_parser
    #
    #     llm_reply = chain.invoke(
    #         {"topics": topics, "question_text": question_text})
    #
    #     result = {
    #         "cleaned_question": llm_reply.content,
    #         "answer_section": " Not today- llm_json.answer_section_json"
    #     }
    #
    #
    #
    #     # prompt = PromptTemplate(
    #     #     template=prompt_text,
    #     #     input_variables=["question_text", "topics"],
    #     #     #    partial_variables={"format_instructions": question_parser.get_format_instructions()},
    #     # )
    #     #
    #     # chain = prompt | llm  #| question_parser
    #     #
    #     # llm_reply = chain.invoke(
    #     #     {"topics": topics, "question_text": question_text})
    #     #
    #     # result = {
    #     #     "cleaned_question": llm_reply.content,
    #     #     "answer_section": " Not today- llm_json.answer_section_json"
    #     # }
    #
    #     return jsonify(result)
    #
    # except Exception as e:  # Add error handling for unexpected issues
    #     return jsonify({'error': str(e)}), 500

    return jsonify({"ai_answer": "DISABLED FOR TESTING FOR NOW"})


@frontend.route('/get-answer', methods=['POST'])
def get_answer():
    clean_question = request.form['extracted_question']
    # extracted_answer_section = request.form['extracted_answer_section']

    # prompt_text = """ Answer this question and give a confidence level. Question: {clean_question}\n Additional Information/Answer Options: {extracted_answer_section}
    #                      """

    prompt_text = """ Answer this question and give a confidence level. 
    RESPONSE FORMAT: Your response should take this format: 'ONLY ANSWER:', 
    'SHORT 
    ANSWER:', 'ELABORATION'
    ; Explanation on your answer format: ONLY provide the answer with the 
    minimum amount of text absolutely necessary at the start of your reply in a 
    section that begins like this: [ONLY ANSWER: ...]
    . Then in another section that begins like this [SHORT ANSWER: ...] 
    provide a short summary of the answer.  
    Finally, in the last section that begins like this: 
    [ELABORATION: ...] give the rest of your response. 
    Do not do any of those bracketed sections if you cannot find a discernible 
    question and/or that formatting doesn't make sense to use. Alter the 
    response format when you find it necessary to do so and 
    feel free to omit the 'SHORT ANSWER:' section when it isn't 
    practical.
    END RESPONSE FORMAT;
    Question: {clean_question}      """
# WORKS!! JUST NEEDS REFACTORING NOW.
#     try:
#         #   answer_parser = PydanticOutputParser(pydantic_object=Answer)
#
#         prompt = PromptTemplate(
#             template=prompt_text,
#             input_variables=["clean_question"],
#             # partial_variables={"format_instructions": question_parser.get_format_instructions()},
#         )
#
#         chain = prompt | llm  #| answer_parser
#
#         llm_reply = chain.invoke({"clean_question": clean_question})
#
#         return jsonify({"ai_answer": llm_reply.content})
#
#     except Exception as e:  # Add error handling for unexpected issues
#         return jsonify({'error': str(e)}), 500

    return jsonify({"ai_answer": "DISABLED FOR TESTING FOR NOW"})


@frontend.route('/prompts', methods=['POST'])
# @login_required
def create_prompt():
    UID = g._login_user.id
    data = request.json
    if 'prompt_text' not in data:
        return jsonify({'error': 'Prompt text is required'}), 400
    new_prompt = Prompt(
        created_by=UID,
        prompt_text=data['prompt_text']
    )
    session.add(new_prompt)
    session.commit()
    return jsonify({'message': 'Prompt created successfully!'}), 201


@frontend.route('/prompts/<int:prompt_id>', methods=['PUT'])
# @login_required
def update_prompt(prompt_id):
    UID = g._login_user.id
    prompt = Prompt.query.filter_by(prompt_id=prompt_id,
                                    created_by=UID).first_or_404()
    data = request.json
    if 'prompt_text' in data:
        prompt.prompt_text = data['prompt_text']
        session.commit()
        return jsonify({'message': 'Prompt updated successfully!'}), 200
    return jsonify({'error': 'Invalid data'}), 400


@frontend.route('/prompts', methods=['GET'])
# @login_required
def get_prompts():
    UID = g._login_user.id
    prompts = Prompt.query.filter_by(created_by=UID).all()
    return jsonify([{'prompt_id': prompt.prompt_id,
                     'prompt_text': prompt.prompt_text}
                    for prompt in prompts]), 200


@frontend.route('/settings')
# @login_required
def settings():
    return render_template('settings.html.j2')



