from __future__ import annotations

from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
import os

# Create a list of documents (in this case, only one document)
docs = ["At Apple's September event, the company unveiled the iPhone 15, which will be available in a range of colors "
        "including pink, yellow, green, blue, and black. Additionally, Apple introduced the Apple Watch Series 9 and "
        "Apple Watch Ultra 2. The Apple Watch Ultra Series 2 has a peak brightness of 3,000 nits and offers a battery "
        "life of 36 hours on a charge or 72 hours with Low Power Mode. The iPhone 15 is expected to inherit features "
        "from its predecessors and support USB-C charging. Apple's new products are also focused on environmental "
        "sustainability, with the Apple Watch Series 9 being the company's first carbon-neutral product through the "
        "use of clean electricity and recycled materials."]
#

os.environ["OPENAI_API_KEY"] = "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"
from langchain.prompts import PromptTemplate

def split_summary(news):
    # OpenAIEmbeddings(model="gpt-3.5-turbo-instruct")
    prompt_template = PromptTemplate(
        input_variables=["news"],
        template="please split the the following news into several bullet points: {news}. Besides, please indicate each bullet point by '-'.",
    )
    prompt = prompt_template.format(news = docs[0])

    # llm = OpenAI(temperature = 0.9)
    llm = OpenAI(model_name="gpt-3.5-turbo-instruct")
    return llm(prompt)


