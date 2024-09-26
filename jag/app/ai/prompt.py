from dataclasses import dataclass

from .prompt_factories import Meta
from ..services.image_processing import ImageProcessor


@dataclass
class Prompt:
    prompt_text: str
    input_variables: list
    meta: Meta
    _langchain_prompt = ''
    image_processor: ImageProcessor = None

    @property
    def langchain_prompt(self):
        return self._langchain_prompt

    @langchain_prompt.setter
    def langchain_prompt(self, prompt_template):
        self._langchain_prompt = prompt_template
