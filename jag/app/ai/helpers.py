from flask import jsonify

from langchain_core.messages import HumanMessage



def ask_ai_human_msg(llm, question):
    try:
        message = HumanMessage(question)
        llm_reply = llm.invoke([message])

        #testing
        # das_reply = llm_reply.content
        return llm_reply.content


    except Exception as e:
        return jsonify(e)



