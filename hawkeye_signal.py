import requests
import json

def get_hawkeye_data():
    req_body = {
        "username":"LabCi",
        "password":"+3A-xnpDTW*YNt^A"
    }

    r = requests.post("https://customerapi.hawkeyeanalytics.com/login/",json=req_body)
    print(r.json())

    print(json.loads(r.json()['body'])["access_token"])

    headers = {
        "Authorization":json.loads(r.json()['body'])["access_token"],
    }
    req_body_2 = {
        "request_market": "us",
        "request_action": "RetrieveTrades",
        "request_date": "2023-05-06",
        "request_customer":"LabCi"
    }
    r1 = requests.post("https://customerapi.hawkeyeanalytics.com/",json=req_body_2,headers=headers)
    response_body = json.loads(r1.json()['body'])
    print(response_body)
    # 如果 response_body 是字符串形式的 JSON，需要再次解码
    if isinstance(response_body, str):
        json_data = json.loads(response_body)  # 再次解码
    else:
        json_data = response_body  # 已经是字典，直接使用

    return json_data

