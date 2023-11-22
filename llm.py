from langchain.llms import OpenAI
import os

# Create a list of documents (in this case, only one document)
docs = [
    "LangChain is a framework for developing applications powered by language models, offered as both a Python and a TypeScript package. We believe that the most powerful and differentiated language model applications will: Be data-aware: connect a language model to other sources of data"]
#

from langchain.prompts import PromptTemplate

prompt_template = PromptTemplate(
    input_variables=["news"],
    template="please split the the following news into several bullet points: {news}",
)
prompt = prompt_template.format(news="")

os.environ["OPENAI_API_KEY"] = "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"
llm = OpenAI(temperature=0.9)
print(llm(docs[0]))
