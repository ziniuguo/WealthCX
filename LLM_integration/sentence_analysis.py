import spacy
from fuzzywuzzy import process
import re
import datetime

nlp = spacy.load("en_core_web_sm")

company_to_ric = {
    "J.P. Morgan Chase & Co": "JPM",
    "Amazon.com Inc": "AMZN.O",
    "Microsoft Corp": "MSFT.O",
    "Alphabet Inc": "GOOGL.O",
    "Tesla Inc": "TSLA.O",
    "McDonald's Corp": "MCD",
    "Meta Platforms Inc": "META.O",
    "NVIDIA Corp": "NVDA.O",
    "Netflix Inc": "NFLX.O",
}

def find_closest_company(input_text, companies):
    closest_match, score = process.extractOne(input_text, companies.keys())
    if score > 30:
        return closest_match
    else:
        return None

text = "I want to read yesterday's news about JP Morgan. Today date is 2024-03-01"
doc = nlp(text)

date_pattern = r"\d{4}-\d{2}-\d{2}"
dates = re.findall(date_pattern, text)
date = dates[0] if dates else datetime.date.today().strftime("%Y-%m-%d")

info = []

for ent in doc.ents:
    if ent.label_ in ["ORG"]:
        closest_company = find_closest_company(ent.text, company_to_ric)
        if closest_company:
            ric = company_to_ric[closest_company]
            info.append({"ric": ric, "date": date})

print(info)