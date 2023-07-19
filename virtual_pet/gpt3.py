import requests

def get_chatgpt_classifier(username, prompt):
    url = "http://123.21.72.140:8948/chat_classifier"  # Replace with the appropriate URL of your Node.js server

    data = {"username":username,"prompt": prompt}

    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()
            return result['result'], result['total_tokens_used']
        else:
            print(f"Request failed with status code {response.status_code}")
            return False, 0
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return False, 0
def get_chatgpt_assistant(username, prompt):
    url = "http://123.21.72.140:8948/chat_assistant"  # Replace with the appropriate URL of your Node.js server

    data = {"username":username,"prompt": prompt}

    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()
            return result['result'], result['total_tokens_used']
        else:
            print(f"Request failed with status code {response.status_code}")
            return {"Overview":"Failed to generate information, Please delete this plant and try again",
                    "Water": "","Light":"","Humidity":"","Temperature":"",
                    "PH Level":"","Suggested Placement Area":"","Others":""}, 0
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return {"Overview":"Failed to generate information, Please delete this plant and try again",
                "Water": "","Light":"","Humidity":"","Temperature":"",
                "PH Level":"","Suggested Placement Area":"","Others":""}, 0

def get_chatgpt_calendar(username, prompt):
    url = "http://123.21.72.140:8948/chat_calendar"  # Replace with the appropriate URL of your Node.js server

    data = {"username":username,"prompt": prompt}

    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()
            return result['result'], result['total_tokens_used']
        else:
            print(f"Request failed with status code {response.status_code}")
            return False, 0
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return False, 0
