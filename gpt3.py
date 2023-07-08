import requests

def get_chatgpt_classifier(prompt):
    url = "http://localhost:8928/chat_classifier"  # Replace with the appropriate URL of your Node.js server

    data = {"prompt": prompt}

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
def get_chatgpt_assistant(prompt):
    url = "http://localhost:8928/chat_assistant"  # Replace with the appropriate URL of your Node.js server

    data = {"prompt": prompt}

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

def get_chatgpt_calendar(prompt):
    url = "http://localhost:8928/chat_calendar"  # Replace with the appropriate URL of your Node.js server

    data = {"prompt": prompt}

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

prompt = '''Plan's name: red rose
Owner's location: kansas
Jobs to perform:
Water the red rose every 3-4 days, make sure the soil is evenly moist but not waterlogged.
Red roses prefer a moderate to high humidity level. Mist the leaves regularly, especially during dry seasons.
Prune your rose regularly to remove dead or diseased parts and promote healthy growth. Provide support for the plant as it grows, as the branches can become heavy with flowers. '''

#print(get_chatgpt_assistant(prompt,'paid'))
