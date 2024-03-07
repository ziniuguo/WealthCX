import os
from pathlib import Path
from langchain.llms import OpenAI
import os
from pathlib import Path
from langchain.prompts import PromptTemplate
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from langchain.chat_models import ChatOpenAI

# set up openai credentials and language models used
print("connecting llm")
data = Path(os.path.join(os.path.dirname(__file__), '../Configuration/openai_key.txt')).read_text()
os.environ["OPENAI_API_KEY"] = data
chat_model = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.3)
llm_client = OpenAI(model_name="gpt-3.5-turbo",temperature=0.3)
