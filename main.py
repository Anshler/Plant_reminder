import time
from pyChatGPT import ChatGPT
import json
import os
import openai

name = 'Mary'

#ChatGPT
session_token = 'eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..1MPL4dWk7K6TimFt.t5LRJ7JKnflrLrhzIY0FKkGiqQmPryoZYERgiio32dOPsavKskdy7-G_yp8uu1RQJPMvKaA-EGfaZOm_HbRnJXhAIU5vTtNUYRLySsoGpIo3G7DB4qI3aLHdbXdLpH3UXgE1EKRRUufqXkuTY769yaS2yVs1j2UGGA1GBqmxezXwOadxeNTzXQc55nb6JPIE6uQP8GM7EnHLcNuhnu7Emi9oT_9dyFiE3SFKPwCmWwE71yylnaF6pZFyLbo4gmaQeuZCZr5Sbe3X0qmLAVtLnXsArWQrkKPHrG3lefKZVgN61TNyN3z97PbKdnEmElXqLIS4pxLy1mKf7lw4tlPZJLtLGT9UAKYaBmqpmXEXPMHNGbrAWe8aZ6KRXVv58-JRYwD6xEIL2WPx60lT9zwof3LnSCccWQNTmBXA6FJCupLvcMjk7NJbFoyTrgf2PNDWj0IAU-Jb0cKNqqHa7WLn1mmdfjJXFi7VEb82FEP5rO97p276323xJ9V8-UHf0BqB5z_qR0qSgFi67dJcydTpRRNPN2OM4_aY37sJzQS43I93qXIpk6A_4GJUFXKHv8IkN1GW2hpGHDS7TbOCYgV9r0F7zAdTsgoZu8E7SIgH-a5b_YgbpFqILtbX3pt5ZEy8cSPABt2blbiRglb8Z4n06opXhfjWe1kzgqWrT6qWr5n1mptM5qRBP2S5qNpbnSWKn2W0uCs3ztFrQjMxIGTB3JadnQVX1Zt65EIdxOixR5p-bZ4uozxeXS_2-oV0U3D_nuZnzlIDfWZ0GBvjeoJpb6intrheW7x1G945OFkeUk03F2EpTu7-YGCUAwLmjnQ0HAFcFjd6kL9E-GYvD332cebZTG8S6DQKzjDnJP1mg_X7aJNIXoUxU2w0O8B-obebFu_Me1JrdYqOAdON4h8Mt7G5WkLIxoZ7i3FJLnfDhko83H-O_Rdr2OgPuvpH6603V-GGxPVBJVICWWQqaxsS6r9Fz9Vs4YclkzGIS8cu805piRPhxRGYgUKHbEt3la4FQWKFN1xzyTkK2zgLg4if4znfPTYRAGJ1DgEqwOFFOTKOxrX2-47K_3LM0ctkZZRvWLnwJp4AtiU86jyWJ6qFPQUmiSAtuAUsZzHSHmKdiow7OrUdLbfY8pWmd5cMaJWX7K-ArcYTTIPA8LhacsaaV4GQpKNoMHQpif9cS0RT1-Exghw-4b_L4pCgfx_P7b7xZmDAeP3CABFKc9jnktZs1jwWsd0caMUvtGXNJaAogYzOSlbp2t9xzHIbwXaCtdZ3lijucQboCOFub8TEwG4YVDEsTgqxGrJUJU9P2fwezsnRWbFdW_KJH-TXa3w4VSQWw0ukLpBPLjROCbQM4V6girITg0T8gCnnmEDPCrHqUNF9pJk-hHaze2R4KA_iLCBdb12aRj1HoqWF3nqa2QE3blQ7-JpB3OWbHgIyHuW4Wa5qSM-GEsT7QvgAwXdqJUstNoyoKcXUBOBuuXnoPTeRgOmGMQKXs7em0LT3i71FROeXahBfoET18yYJSXb6yrGxFwqCEwOHmZBKzih9zSIo40K8dUfGQXjEC1_wOjbpieTmGyY1EvXXFBQ3gQ3Q8Qv9TpXc3FLZvm_-0uOQ1J5dwmLbqbHboE3jp5KTlJznrmFi7uam2SxQXuCBVVBYdhUTFflQAS1XwAQAnP_H_uoTRJqa1jiVs69NYNKCFK5TiWExjPYyBhLleNM0kr8_F2LYUo3QGw6inCo59ekGKqUnRdBUZyzLXC7pSNXNnXBwvoofuKuNV5fBdUBIHe2SY1gq34VMJcYdezNY8v80dTculVuVVVeQIZWFN4G8wX4IXHI03AgaJsb_-ube7S44ApOHVL2naBsb1wxums9VOZJP8Bb66KEJU9w7XDACNf59u3_Vng8iOrVfnMUAHn6XLb88RAXjkSsZ-lB1OzoBzjdyQxaNLk-eSCDUpY0v25bhtsQB_tbQKRD8MKm1mpwd96Cjpper_qWt1inEf47Z9LJk6JLfQ8iK7BVESwzwBHmViUFy_BU-uam2sra_MHv5Nj3tjulq-vXBcq_uYPepNB0VEJINnzILz7uMpuQ74e5xArjplPemSwzBunA9RJdNY1pCPF9_wUDwSZiJ_dqYo63twLPDbvsa71bpVa43zU304PSo9W4hFr5BHzwNkJ0xdQCA96dp9RSeCSih-z-Zop9bVRIolXfPE5YD17AoLOQ_fZ9qbiY8ThrodwW09gkTQ28rtqcXgaLwjGRHUaVCWJq55V1QKy1yXKBg51uf3QgTg6GzmTGDIf_C2TaWaI_n8x8YPqnFxUvHeX_g4RMcuYD7Nfe0iQYmcaBSx2w75Ond28z-6lwrDaUP69dREYXBo9TJwvmTgumfoO6zSg8-6eQhPC-tQZDkuXBoEjGqD5hsZX1z-0mKmO1KHApdkYGCxdvFPQhBoypq-iDS_oNyQ2IWEX-uxP_8zQhy--QTV_p3qkHH1Sd4x3Uqq2-YtIDGLdR2l8EDdNGfdWtf6SzB5VMZ_N-AD732PyjFDA-thyW3kQGYUJlPK9M.8fAWgicnDknFcpuikNxRZw'
api = ChatGPT(session_token)


plant_info = json.load(open(name+"/info.json", "r", encoding='utf-8'))
user_info = json.load(open("profile/user/user.json", "r", encoding='utf-8'))

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
        resp = api.send_message(prompt)

        message = str(resp['message']).replace("\"You\"","You")

        a = open(name + '/recent_log.txt', 'w', encoding='utf-8')
        a.write(recent_log)
        b = open(name + '/summary.txt', 'w', encoding='utf-8')
        b.write(message)
        api.refresh_chat_page()

    return open(name + '/recent_log.txt', "r+", encoding='utf-8'), open(name + '/summary.txt', "r+", encoding='utf-8')

while True:

    recent_log, summary = token_size_management(name)
    # print(header_prompt)
    read_summary = summary.read()
    read_recent_log = recent_log.read()

    conversation = header_prompt + '\n\n' + read_summary + read_recent_log
    try:
        prompt = input("You:\n")
        conversation += user_info['name']+':\n'+prompt+'\n\n'+'You:(always short answer, except for explanation)\n'
        resp = api.send_message(conversation)
        message = resp['message']
        if '\n\n'+user_info['name']+':' in message:
            message = message.split('\n\n'+user_info['name']+':')[0]+'\n\n'
        print('\n',plant_info['name']+':\n',message)
        conversation += message

        current_log = user_info['name'] + ':\n' + prompt + '\n\n' + 'You:\n' + message
        recent_log.write(current_log)
        log.write(current_log)

    except Exception as e:
        print(e)

    api.refresh_chat_page()


