import requests

def chat_with_plant_gpt(user_input, user, plant_conversation):
    url = "http://localhost:8948/chat"  # Replace with the appropriate URL of your Node.js server

    data = {
        "user_input": user_input,
        "user": user,
        "plant_conversation": plant_conversation
    }

    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()
            return result['conversation'], result['chat_reply'], result['total_tokens_used']
        else:
            print(f"Request failed with status code {response.status_code}")
            return plant_conversation, '', 0
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return plant_conversation, '', 0
