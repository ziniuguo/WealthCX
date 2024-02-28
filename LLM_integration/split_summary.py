from __future__ import annotations

import time

from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
import os
from pathlib import Path
from langchain.prompts import PromptTemplate

# Create a list of documents (in this case, only one document)
docs = ["At Apple's September event, the company unveiled the iPhone 15, which will be available in a range of colors "
        "including pink, yellow, green, blue, and black. Additionally, Apple introduced the Apple Watch Series 9 and "
        "Apple Watch Ultra 2. The Apple Watch Ultra Series 2 has a peak brightness of 3,000 nits and offers a battery "
        "life of 36 hours on a charge or 72 hours with Low Power Mode. The iPhone 15 is expected to inherit features "
        "from its predecessors and support USB-C charging. Apple's new products are also focused on environmental "
        "sustainability, with the Apple Watch Series 9 being the company's first carbon-neutral product through the "
        "use of clean electricity and recycled materials."]


#


def access_setup():
    data = Path(os.path.join(os.path.dirname(__file__), '../Configuration/openai_key.txt')).read_text()
    os.environ["OPENAI_API_KEY"] = data


def split_summary(news):
    # OpenAIEmbeddings(model="gpt-3.5-turbo-instruct")
    start_time = time.perf_counter()
    access_setup()
    prompt_template = PromptTemplate(
        input_variables=["news"],
        template="please split the the following news into several bullet points: {news}. Besides, please indicate each bullet point by '-'. Each points around 15-20 words",
    )
    if news == "":
        prompt = prompt_template.format(news=docs[0])
    else:
        prompt = prompt_template.format(news=news)

    # llm = OpenAI(temperature = 0.9)
    llm = OpenAI(model_name="gpt-3.5-turbo-instruct")
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print(execution_time)
    with open("./execution_times.txt", 'a') as f:
        f.write(f"{execution_time}\n")
    return llm(prompt)
