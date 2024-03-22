import spacy
from fuzzywuzzy import process
import re
from datetime import datetime, timedelta

def find_closest_company(input_text, companies):
    closest_match, score = process.extractOne(input_text, companies.keys())
    print(score)
    if score > 30:
        return closest_match
    else:
        return None

def analyze_text(text):
    # nlp = spacy.load("en_core_web_sm")
    nlp = spacy.load("en_core_web_lg")
    company_to_ric = {'j.p. morgan chase & co': 'JPM',
 'amazon.com inc': 'AMZN.O',
 'microsoft corp': 'MSFT.O',
 'alphabet inc': 'GOOGL.O',
 'tesla inc': 'TSLA.O',
 "mcdonald's corp": 'MCD',
 'meta platforms inc': 'META.O',
 'nvidia corp': 'NVDA.O',
 'netflix inc': 'NFLX.O'}
    doc = nlp(text)

    date_pattern = r"\d{4}-\d{2}-\d{2}"
    dates = re.findall(date_pattern, text)
    today_date = datetime.strptime(dates[0], "%Y-%m-%d") if dates else datetime.today()
    yesterday_date = today_date - timedelta(days=1)

    if "yesterday's news" in text:
        date_to_use = yesterday_date.strftime("%Y-%m-%d")
    else:
        date_to_use = today_date.strftime("%Y-%m-%d")
    info = []
    for ent in doc.ents:
        # if ent.label_ in ["ORG"]:
            closest_company = find_closest_company(ent.text, company_to_ric)
            if closest_company:
                ric = company_to_ric[closest_company]
                info.append({"ric": ric, "date": date_to_use})
    return info

# # 示例文本
text = "jp morgan"
result = analyze_text(text)
print(result)