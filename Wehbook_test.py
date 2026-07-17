import requests
user_message = "Can you tell me about black holes in 3-4 lines"
request_message = {"message": user_message}
url = "http://localhost:5678/webhook-test/6ec5921e-11d0-4832-be89-7a7cdf494c14"
response = requests.post(url, json=request_message)
print(response.status_code)
print(response.json())