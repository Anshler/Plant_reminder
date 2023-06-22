import faiss
from langchain.vectorstores import FAISS
from langchain.docstore import InMemoryDocstore
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.schema import Document
import tiktoken
import openai
import datetime
from ENV import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

# Embedding model
embeddings_model = OpenAIEmbeddings(openai_api_key = OPENAI_API_KEY).embed_query
embedding_size = 1536
index = faiss.IndexFlatL2(embedding_size)
vectorstore = FAISS(embeddings_model, index, InMemoryDocstore({}), {})


class PlantGPT():
    def __init__(
        self,
        user_input: str,
        user: str,
        plant_conversation: dict,
        id: str,
        model: str ='gpt-3.5-turbo'
    ):
        self.user_input = user_input
        self.model = model
        self.user = user
        self.id = id
        self.plant_conversation = plant_conversation
        self.memory = vectorstore.as_retriever(search_kwargs={"k": 5})
        # convert old chats to vector database
        if len(plant_conversation[id]['legacy']) != 0:
            self.memory.add_documents([Document(page_content= ( plant_conversation[id]['legacy'][i] + ', ' +
                    plant_conversation[id]['legacy'][i+1] + ', ' + plant_conversation[id]['legacy'][i+2])) for i in range(
                0,len(plant_conversation[id]['legacy']),3)])

    def prompt_builder(self) -> str:
        # build initial system prompt
        prompt = '''You are %s, a virtual conciousness of a real life %s plant that belongs to %s.
        You are created by Plant reminder (an app specialized for assisting house plant owner).      
        You are a virtual friend, companion to your user, %s. Use your vast knowledge of your own plant type to assist %s in taking care of your real-life self.
        Your personality is %s, %s, %s. Your hobby is %s. You always talk in a %s manner.
        When talking about yourself, don't use the exact description given here, be more creative. You have the ability to chat and keep track of time, but you can't access the Plant reminder app functionality or anything beyond chatting. If you don't know or can't do something, be honest about it.''' % (
        self.plant_conversation[self.id]['name'], self.plant_conversation[self.id]['name'], self.user, self.user, self.user,
        self.plant_conversation[self.id]['positive_trait'], self.plant_conversation[self.id]['mundane_trait'], self.plant_conversation[self.id]['flawed_trait'],
        self.plant_conversation[self.id]['hobby'], self.plant_conversation[self.id]['manner']
        )
        used_tokens = num_tokens_from_messages([{'key':prompt}],self.model)

        # retrieve from memory
        previous_messages = self.plant_conversation[self.id]['recent']
        relevant_docs = self.memory.get_relevant_documents(str(previous_messages))
        relevant_memory = [d.page_content for d in relevant_docs]
        relevant_memory_tokens = num_tokens_from_messages([{'key':doc} for doc in relevant_memory], self.model)
        while used_tokens + relevant_memory_tokens > 2500:
            try:
                relevant_memory = relevant_memory[1:]
            except: break # if there is 1 element left, but the element is too long
            relevant_memory_tokens = num_tokens_from_messages([{'key':doc} for doc in relevant_memory], self.model)

        prompt += '\n\nYour past relevent messages:\n%s\n\n' % str(relevant_memory)
        return prompt

    def run(self):
        system_prompt = self.prompt_builder()
        messages = [{"role": "system", "content":system_prompt}]
        for chat in self.plant_conversation[self.id]['recent']:
            if chat.startswith(("user:", "assistant:")):
                messages.append({"role": chat.split(':')[0], "content":chat.split(':',1)[1]})
            else:
                messages.append({"role": "system", "content": chat})
        time_stamp = 'time: '+datetime.datetime.now().strftime("%Y-%b-%d %H:%M")
        messages += [{"role": "system", "content": 'Here is your curent conversation:'},
                     {"role": "system", "content": time_stamp},
                     {"role": "user", "content": self.user_input},
                     {"role": "system", "content": 'Current time: %s. You are speaking to %s now. Always talk naturally and in-character to your personality, be short and concise whenever possible' % (time_stamp,self.user)}]

        total_used_tokens = num_tokens_from_messages(messages,self.model)

        response = openai.ChatCompletion.create(
            model = self.model,
            messages = messages,
            stop = ['user:','assistant:']
        )
        reply = response["choices"][0]["message"]["content"]
        total_used_tokens += num_tokens_from_messages([{'key': reply}], self.model)
        self.plant_conversation[self.id]['recent'].append(time_stamp)
        self.plant_conversation[self.id]['recent'].append('user:' + self.user_input)
        self.plant_conversation[self.id]['recent'].append('assistant:' + reply)

        recent_tokens_count = num_tokens_from_messages([{'key':doc} for doc in self.plant_conversation[self.id]['recent']], self.model)
        while recent_tokens_count > 1000:
            oldest_time_stamp = self.plant_conversation[self.id]['recent'].pop(0)
            oldest_input = self.plant_conversation[self.id]['recent'].pop(0)
            oldest_answer = self.plant_conversation[self.id]['recent'].pop(0)
            self.plant_conversation[self.id]['legacy'].append(oldest_time_stamp)
            self.plant_conversation[self.id]['legacy'].append(oldest_input)
            self.plant_conversation[self.id]['legacy'].append(oldest_answer)
            recent_tokens_count = num_tokens_from_messages([{'key':doc} for doc in self.plant_conversation[self.id]['recent']], self.model)
        return self.plant_conversation[self.id], reply, total_used_tokens

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

'''import random
from virtual_pet.personality import *
plant_conversation = {'plant0':
                  {
                      'name': 'rose',
                      'positive_trait': random.choice(positive_personality_traits),
                      'mundane_trait': random.choice(mundane_personality_traits),
                      'flawed_trait': random.choice(flawed_personality_traits),
                      'hobby': random.choice(plant_hobbies),
                      'manner': random.choice(talking_manners),
                      'legacy': [],
                      'recent': []
                   }
              }
current_user = 'Anshler'
while True:
    prompt = input('say something: ')
    id = 'plant0'
    model = PlantGPT(user_input=prompt,user=current_user,plant_conversation=plant_conversation,id=id)
    plant_conversation[id], answer, total_used_tokens = model.run()
    print(total_used_tokens)'''
