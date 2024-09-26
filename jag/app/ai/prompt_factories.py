import abc
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.messages import HumanMessage


class Meta:
    def __init__(self, depends=None):
        self.depends = depends


class TemplateFactory(abc.ABC):
    def create_prompt(self, prompt_text, input_variables, meta: Meta):
        pass


class ChatPromptTemplateFactory(TemplateFactory):
    def create_prompt(self, prompt_text, input_variables, meta):
        return ChatPromptTemplate(
            input_variables=input_variables
        )


class PromptTemplateFactory(TemplateFactory):
    """This was originally used for the OCR Questions and Cleaned_question"""
    def create_prompt(self, prompt_text, input_variables, meta):
        if input_variables is None:
            input_variables = ["question_text", "topics"]
        return PromptTemplate(
            template=prompt_text,
            input_variables=input_variables
            # partial_variables={"format_instructions": question_parser.get_format_instructions()},
        )


class HumanMessageFactory(TemplateFactory):
    """This was used for the multi-modal IMAGES content prompts!"""
    def create_prompt(self, prompt_text, input_variables, meta):
        return HumanMessage(content=prompt_text)

