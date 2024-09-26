from builtins import property

from .prompt_factories import TemplateFactory, Meta
from .prompt import Prompt


class PromptBuilder:
    @staticmethod
    def create_prompt(prompt_text, input_variables, meta) -> Prompt:
        prompt = Prompt(prompt_text, input_variables, meta)
        prompt_factory = PromptBuilder.determine_factory(meta)
        prompt.langchain_prompt = prompt_factory.create_prompt(prompt_text,
                                                               input_variables,
                                                               meta)

        return prompt

    @staticmethod
    def determine_factory(meta) -> TemplateFactory:
        """Dynamically retrieve the class based on the 'depends' key"""
        class_name = f"{meta.depends}Factory"
        factory_class = globals().get(class_name)
        if not factory_class:
            raise ValueError(f"Factory class not found: {class_name}")

            # Ensure the class exists and is a subclass of TemplateFactory
        if not issubclass(factory_class, TemplateFactory):
            raise ValueError(
                f"Factory class is not a subclass of TemplateFactory:"
                f" {class_name}")

        return factory_class()

# def ask_ai_human_msg(llm, question):
#     try:
#         message = HumanMessage(question)
#         llm_reply = llm.invoke([message])
#
#         #testing
#         # das_reply = llm_reply.content
#         return llm_reply.content
#
#
#     except Exception as e:
#         return jsonify(e)


# content = []
#     for image in images:
#         secured_filename = secure_filename(image.filename)
#         filename = f"pic--{secured_filename}"
#         save_path = os.path.join(new_images_dir, filename)

#         # Open the image using PIL
#         with Image.open(image.stream) as image_data:
#             image_data.save(save_path)
#             # Save the image to a byte array
#             img_byte_arr = io.BytesIO()
#             image_data.save(img_byte_arr, format='PNG')
#             # Encode the image to base64 directly from memory
#             encoded_image = base64.b64encode(img_byte_arr.getvalue()).decode(
#                 'utf-8')
#             encoded_image = f"data:image/png;base64,{encoded_image}"

#             content.append({
#                 "type": "image_url",
#                 "image_url": {"url": encoded_image},
#             })

#             # if GoogleAI:
#             #     content.append({
#                     #             "text": image_tag
#                     #         })

#     content.append({
#         "type": "text",
#         "text": prompt_txt,
#     })
