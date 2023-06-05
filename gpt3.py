from pychatgpt import ChatGPT
try:
    from importlib import resources
except ImportError:
    import importlib_resources as resources
import openai
import json

botanical_assistant = open(resources.path('app_config','botanical_assistant.txt'),encoding='utf-8').read()
real_plant_classifier = open(resources.path('app_config','real_plant_classifier.txt'),encoding='utf-8').read()
session_token = ''
openai.api_key = ''


def get_chatgpt_classifier(prompt, mode ='free'):
    while True:
        try:
            wrapper_prompt = real_plant_classifier
            if mode == 'free':
                model = ChatGPT(session_token)
                prompt = wrapper_prompt + '\n' + prompt
                resp = model.send_message(prompt)
                resp = resp['message']
            else:
                resp = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=[
                    {"role": "system", "content": wrapper_prompt},
                    {"role": "user", "content": prompt}]
                )
                resp = resp['choices'][0]['message']['content']
            resp = resp[resp.index('{'):resp.rindex('}') + 1]
            result = json.loads(resp)
            return result['result']
        except: pass

def get_chatgpt_assistant(prompt, mode='free'):
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
                resp = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo", messages=[
                        {"role": "system", "content": wrapper_prompt[0]},
                        {"role": "user", "content": prompt},
                        {"role": "system", "content": wrapper_prompt[1]}]
                )
                resp = resp['choices'][0]['message']['content']
            resp = resp[resp.index('{'):resp.rindex('}') + 1]
            result = json.loads(resp)
            return result
        except Exception as e:
            print(e)

#print(get_chatgpt_classifier('plant\'s name: ','paid'))
