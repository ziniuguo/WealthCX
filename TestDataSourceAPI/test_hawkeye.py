import requests
import json

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
r2 = json.loads(r1.json()['body'])
print(r2)