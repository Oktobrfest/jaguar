import openai

from langchain_openai import ChatOpenAI, OpenAI
from flask import current_app

from ..configs.config import Config




# eventually re-factor this.
openai.api_key = Config.OPENAI_API_KEY


# the real deal
gpt_model = "gpt-4o"

gpt_max_tokens = current_app.config['GPT_MAX_TOKENS']

gpt_llm = ChatOpenAI(model=gpt_model, temperature=0.2,
                     max_tokens=gpt_max_tokens,
                 openai_api_key=openai.api_key)