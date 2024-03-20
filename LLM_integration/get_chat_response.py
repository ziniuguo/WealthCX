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
    msg_class_num = input.get("msg_class_num")

    if msg_class_num == 0:
        output = get_general_chat_response(user_message)
    elif msg_class_num == 1:
        output = get_app_usage(user_message)
    elif msg_class_num == 3:
        output = get_news_analysis(user_message)
    elif msg_class_num == 2:
        output = get_terminology_explanation(user_message)
    else:
        # Handle other cases or provide a default value for output
        output = "Unknown msg_class_num"

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
    output_json = {
        "content": response,
        "additional_kwargs": {},
        "type": "ai",
        "example": False
    }
    return output_json

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
    prompt = """Here is our APP document
    Registering an account
Press the profile icon at the bottom right corner of the screen.
Press the register button.
Enter the account details you would like to use, such as the email, password, a confirmation of the password and username.
Press the register button to register an account.
Logging in
Press the profile icon at the bottom right corner of the screen.
Press the log in button.
Enter your username and password.
Press the log in button to login.
Main Page
Access the main page by pressing the home icon in the bottom-left corner.
The list of companies available are: [Apple Inc., Tesla Inc., JPMorgan Chase & Co., Amazon.com Inc., Microsoft Corp., Alphabet Inc., McDonald's Corp., Meta Platforms Inc., NVIDIA Corp., Netflix Inc.].
The list of the respective companies' RICs available are: [AAPL.O, TSLA.O, JPM, AMZN.O, MSFT.O, GOOGL.O, MCD, META.O, NVDA.O, NFLX.O].
Search for a live signal using the search box by entering the company's name or Refinitiv Instrument Code (RIC in short, RIC is a code that identifies a particular company's stock).
Press the live signal of the company by pressing the button with the label of the company in order to view its signal.
Signal
In this particular page, the following data can be viewed: the current price of the company stock, the outlook of the company stock, the target price of the company stock, the inception date of the company and some relevant news reports of the company.
Press the News & Reports button to view the recent news that are related to the company.
Press the Data & Market Trends button to view some historic market trends related to the company.
Data & Market Trends
In this particular page, you can view historical price data of the company stock in graphical format.
Press the return button to return.
History
In the main page, access the history page by pressing the history icon on the bottom of the page.
The page displays a list of past signals that the companies have.
Notifications
Access the settings page by pressing the cog icon on the top-right corner.
In the settings button, press the set time to display notifications button.
Choose a suitable time to display the notification using the time picker that appears. This allows a notification to be set to appear once a day to remind the user to check for updates.
At the chosen time, a notification will appear. Pressing the notification will bring the user to the main page.
Chatbot
At the main page, press the top-left corner to access the chatbot.
At the chatbot page, enter a message or query by pressing the chatbot and press the send icon to send a message.
After a short while, a response would be generated by the chatbot.
    """
    messages = [
        SystemMessage(content="Please follow the following document answer the question. Please use 1. 2. etc to split steps "+prompt),
        HumanMessage(content=message)
    ]
    response = chat_model(messages)
    return response
def get_terminology_explanation(terminology:str):
    # TODO: implement this
    prompt = "Please explain the following fancial terminology word " + terminology
    messages = [
        SystemMessage(content=prompt),
        HumanMessage(content=terminology)
    ]
    response = chat_model(messages)
    return response
