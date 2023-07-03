from pychatgpt import ChatGPT
import openai
import tiktoken
import json
from utils.plant_profile_management import clean_calendar
from ENV import OPENAI_API_KEY
from utils.android_port import get_file_path
botanical_assistant = open(get_file_path('app_config/botanical_assistant.txt'),encoding='utf-8').read()
real_plant_classifier = open(get_file_path('app_config/real_plant_classifier.txt'),encoding='utf-8').read()
calendar_builder = open(get_file_path('app_config/calendar_builder.txt'),encoding='utf-8').read()
session_token = ''
openai.api_key = OPENAI_API_KEY

def get_chatgpt_classifier(prompt, mode ='paid'):
    model = 'gpt-3.5-turbo'
    total_tokens_used = 0
    while True:
        try:
            wrapper_prompt = real_plant_classifier
            if mode == 'free':
                model = ChatGPT(session_token)
                prompt = wrapper_prompt + '\n' + prompt
                resp = model.send_message(prompt)
                resp = resp['message']
            else:
                messages = [
                    {"role": "system", "content": wrapper_prompt},
                    {"role": "user", "content": prompt}]
                resp = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=messages
                )
                resp = resp['choices'][0]['message']['content']
            resp = resp[resp.index('{'):resp.rindex('}') + 1]
            total_tokens_used += num_tokens_from_messages(messages, model)
            total_tokens_used += num_tokens_from_messages([{'key': resp}], model)
            result = json.loads(resp)
            return result['result'], total_tokens_used
        except: pass

def get_chatgpt_assistant(prompt, mode='paid'):
    model = 'gpt-3.5-turbo'
    total_tokens_used = 0
    while True:
        try:
            wrapper_prompt = botanical_assistant.split('[PROMPT]')
            if mode == 'free':
                model = ChatGPT(session_token)
                wrapper_prompt = botanical_assistant.split('[PROMPT]')
                prompt = wrapper_prompt[0] + prompt + wrapper_prompt[1]
                resp = model.send_message(prompt)
                resp = resp['message']
            else:
                messages = [
                        {"role": "system", "content": wrapper_prompt[0]},
                        {"role": "user", "content": prompt},
                        {"role": "system", "content": wrapper_prompt[1]}]
                resp = openai.ChatCompletion.create(
                    model=model, messages=messages
                )
                resp = resp['choices'][0]['message']['content']
                total_tokens_used += num_tokens_from_messages(messages, model)
                total_tokens_used += num_tokens_from_messages([{'key': resp}], model)
            resp = resp[resp.index('{'):resp.rindex('}') + 1]
            result = json.loads(resp)
            return result, total_tokens_used
        except Exception as e:
            print(e)

def get_chatgpt_calendar(prompt, mode='paid'):
    model = 'gpt-3.5-turbo'
    total_tokens_used = 0
    while True:
        try:
            wrapper_prompt = calendar_builder.split('[PROMPT]')
            if mode == 'free':
                model = ChatGPT(session_token)
                wrapper_prompt = botanical_assistant.split('[PROMPT]')
                prompt = wrapper_prompt[0] + prompt + wrapper_prompt[1]
                resp = model.send_message(prompt)
                resp = resp['message']
            else:
                messages = [
                        {"role": "system", "content": wrapper_prompt[0]},
                        {"role": "user", "content": prompt},
                        {"role": "system", "content": wrapper_prompt[1]}]
                resp = openai.ChatCompletion.create(
                    model=model, messages=messages
                )
                resp = resp['choices'][0]['message']['content']
                total_tokens_used += num_tokens_from_messages(messages, model)
                total_tokens_used += num_tokens_from_messages([{'key':resp}], model)
            resp = resp[resp.index('{'):resp.rindex('}') + 1]
            result = json.loads(resp)
            result = clean_calendar(result)
            return result, total_tokens_used
        except Exception as e:
            print(e)

# Token counter
def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301"):
    """Returns the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-3.5-turbo":
        #print("Warning: gpt-3.5-turbo may change over time. Returning num tokens assuming gpt-3.5-turbo-0301.")
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301")
    elif model == "gpt-4":
        #print("Warning: gpt-4 may change over time. Returning num tokens assuming gpt-4-0314.")
        return num_tokens_from_messages(messages, model="gpt-4-0314")
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif model == "gpt-4-0314":
        tokens_per_message = 3
        tokens_per_name = 1
    else:
        raise NotImplementedError(f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens

prompt = '''Plan's name: red rose
Owner's location: kansas
Jobs to perform:
Water the red rose every 3-4 days, make sure the soil is evenly moist but not waterlogged.
Red roses prefer a moderate to high humidity level. Mist the leaves regularly, especially during dry seasons.
Prune your rose regularly to remove dead or diseased parts and promote healthy growth. Provide support for the plant as it grows, as the branches can become heavy with flowers. '''

#print(get_chatgpt_assistant(prompt,'paid'))
