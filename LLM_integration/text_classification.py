from transformers import pipeline


def text_classify(texts:list):
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    candidate_labels = ["read company news", "financial term definition", "app usage"]

    for text in texts:
        result = classifier(text, candidate_labels)
        labels = result["labels"]
        scores = result["scores"]
        prediction = labels[0]
        return_list = [False,False,False]
        return_list[candidate_labels.index(labels[0])] = True
    return return_list



# texts = [
#     "I want to read today's news about JP Morgan. Today date is 2024-03-01",
#     "I want to know the financial word 'BID' means",
#     "I want to know how to see JP Morgan's target price in the app"
# ]
# x = text_classify([texts[2]])
# print(x)