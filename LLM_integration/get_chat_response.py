from __future__ import annotations

from langchain.prompts import PromptTemplate
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

import query_summary
from LLM_integration import chat_model, sentence_analysis, llm_client


def get_chat_response(input:dict):
    output = ""
    user_message = input["user_input"]
    match input.get("msg_class_num"):
        case 0:
            output = get_general_chat_response(user_message)
        case 1:
            output = get_app_usage(user_message)
        case 2:
            output = get_news_analysis(user_message)
        case 3:
            output = get_terminology_explanation(user_message)
    return output

def get_news_analysis(company_name:str):
    target_company_RIC = sentence_analysis.analyze_text(company_name)
    json_result = query_summary.query_combined_table(target_company_RIC[0]['ric'])
    template_string = """
        You are an expert investment consultant. 
        Analyze the news below and talk about the potential influence of the stockmarket:
        {news_text}
        """
    prompt = PromptTemplate(input_variables=['message'], template=template_string)

    # response = client.chat.completions.create(
    #     messages = [
    #         {
    #             "role": "user",
    #             "content": f"You are an expert investment consultant. Analyze the news below and talk about the potential influence of the stockmarket: {json_result}"
    #         }
    #     ],
    #     model="gpt-3.5-turbo"
    # )
    response = llm_client(prompt.format(news_text=json_result[0]["Summary"]))
    return response

def get_general_chat_response(message:str):
    template_string = """
    You are an expert investment consultant.
    Please reply to {message} in a couple of lines
    """
    prompt = PromptTemplate(input_variables=['message'], template=template_string)
    messages = [
        SystemMessage(content="You are an expert investment consultant. Please reply to the following:"),
        HumanMessage(content=message)
    ]
    response = chat_model(messages)
    return response

def get_app_usage(message:str):
    # TODO: implement this
    prompt = 'Here is our APP document'
    response = "function"
    return response
def get_terminology_explanation(terminology:str):
    # TODO: implement this
    prompt = "Please explain the following fancial terminology word " + terminology
    response = "function"
    return response
