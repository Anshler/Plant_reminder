import time
import openai
import json
import os

name = 'Mary'
name = 'placeholder_server/plants/'+name
#GPT-3
openai.api_key = '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'


plant_info = json.load(open(name+"/info.json", "r", encoding='utf-8'))
user_info = json.load(open("placeholder_server/user/user.yaml", "r", encoding='utf-8'))

header_prompt = '''You are %s, a virtual conciousness of a real life %s plant, your personality is %s. You are a virtual friend, companion to your user, %s. You can use your vast knowledge of your own plant type to assist %s in taking care of your real-life self. Always talk naturally and in-character to your personality. Here is your conversation:'''%(plant_info['name'], plant_info['type'], plant_info['personality'],user_info['name'], user_info['name'])

print('Type something to start a conversation')

log = open(name+'/log.txt', "a", encoding='utf-8')


def token_size_management(name): # If longer than 800 tokens, summarize first half (GPT-3 maximum is 2000 tokens)
    recent_log = open(name + '/recent_log.txt', encoding='utf-8').read()
    summary = open(name + '/summary.txt', encoding='utf-8').read()

    if len(recent_log.split()) + len(summary.split()) >= 800:
        print(True)
        recent_log = recent_log.split('\n\n')
        n = int(len(recent_log) / 2)
        if recent_log[n].startswith('You:'):
            #print(True)
            n += 1
        recent_log_1 = '\n\n'.join(recent_log[:n])
        recent_log_2 = '\n\n'.join(recent_log[n:])

        recent_log = recent_log_2
        if len(summary)==0:
            summary += recent_log_1
        else:
            summary += 'And then'+'\n\n'+recent_log_1

        prompt = 'Summarize this conversation between %s (the owner) and you (a %s) in less than 300 words: \n\n'%(user_info['name'],plant_info['type'])+summary
        resp = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                temperature=0.7,
                max_tokens=256,
            )

        message = str(resp['choices'][0]['text']).replace("\"You\"","You")

        a = open(name + '/recent_log.txt', 'w', encoding='utf-8')
        a.write(recent_log)
        b = open(name + '/summary.txt', 'w', encoding='utf-8')
        b.write(message)

    return open(name + '/recent_log.txt', "r+", encoding='utf-8'), open(name + '/summary.txt', "r+", encoding='utf-8')

while True:

    recent_log, summary = token_size_management(name)
    # print(header_prompt)
    read_summary = summary.read()
    read_recent_log = recent_log.read()

    conversation = header_prompt + '\n\n' + read_summary + '\n\n' + read_recent_log
    try:
        prompt = input("You:\n")
        conversation += user_info['name']+':\n'+prompt+'\n\n'+'You:(always short answer, except for explanation)\n'

        resp = openai.Completion.create(
            engine="text-davinci-003",
            prompt=conversation,
            temperature=0.7,
            max_tokens=256,
            stop = '\n\n'+user_info['name']+':'
        )

        message = resp['choices'][0]['text'] + '\n\n'
        print('\n',plant_info['name']+':\n',message)
        conversation += message

        current_log = user_info['name'] + ':\n' + prompt + '\n\n' + 'You:\n' + message
        recent_log.write(current_log)
        log.write(current_log)

    except Exception as e:
        print(e)


