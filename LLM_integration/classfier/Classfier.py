import class_app_usage
import class_news_analysis
import class_terminology_explanation

input = {'msg_class_num':1,'user_input':'I want to know the meaning of BID value'}

def classfier(input:dict):
    if input.get("msg_class_num") == 0:
        pass
    elif input.get("msg_class_num") == 1:
        output = class_app_usage.class_app_usage(input.get("user_input"))
    elif input.get("msg_class_num") == 2:
        output = class_news_analysis.class_news_analysis(input.get("user_input"))
    elif input.get("msg_class_num") == 3:
        output = class_terminology_explanation.class_terminology_explanation(input.get("user_input"))
    return output

x = classfier(input)
print(x)