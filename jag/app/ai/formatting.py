import re




def parse_response(response_text: str) -> dict:
    """Format the response text received from the AI to populate the following category sections. ONLY ANSWER, SHORT ANSWER, ELABORATION, CODE"""
    sections = {
        "ONLY ANSWER": (r"\[ONLY_ANSWER_START\](.*?)\[ONLY_ANSWER_END\]", ""),
        "SHORT ANSWER": (r"\[SHORT_ANSWER_START\](.*?)\[SHORT_ANSWER_END\]", ""),
        "ELABORATION": (r"\[ELABORATION_START\](.*?)\[ELABORATION_END\]", ""),
        "CODE": (r"\[CODE_START\](.*?)\[CODE_END\]", "")
    }

    parsed_data = {}
    for section, (pattern, default) in sections.items():
        regex = re.compile(pattern, re.DOTALL)
        match = regex.search(response_text)
        parsed_data[section] = match.group(1).strip() if match else default

    return parsed_data







