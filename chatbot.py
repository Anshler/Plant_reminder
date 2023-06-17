import faiss
from langchain.vectorstores import FAISS
from langchain.docstore import InMemoryDocstore
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.schema import Document
import tiktoken
import openai

api_key = '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'
openai.api_key = api_key

# Embedding model
embeddings_model = OpenAIEmbeddings(openai_api_key = api_key).embed_query
embedding_size = 1536
index = faiss.IndexFlatL2(embedding_size)
vectorstore = FAISS(embeddings_model, index, InMemoryDocstore({}), {})


class PlantGPT():
    def __init__(
        self,
        user_input: str,
        user: str,
        plant_list: dict,
        id: str,
        model: str ='gpt-3.5-turbo'
    ):
        self.user_input = user_input
        self.model = model
        self.user = user
        self.id = id
        self.plant_list = plant_list
        self.memory = vectorstore.as_retriever(search_kwargs={"k": 5})
        # convert old chats to vector database
        if len(plant_list[id]['legacy']) != 0:
            self.memory.add_documents([Document(page_content= (
                    plant_list[id]['legacy'][i] + ' ' + plant_list[id]['legacy'][i+1])) for i in range(
                0,len(plant_list[id]['legacy']),2)])

    def prompt_builder(self) -> str:
        # build initial system prompt
        prompt = '''You are %s, a virtual conciousness of a real life %s plant, your personality is %s. You are a virtual friend, created by Plant reminder, an app specialized for helping house plant owner. You are companion to your user, %s. You can use your vast knowledge of your own plant type to assist %s in taking care of your real-life self. Always talk naturally and in-character to your personality. ''' % (
        self.plant_list[self.id]['name'], self.plant_list[self.id]['name'], self.plant_list[self.id]['personality'], self.user, self.user)
        used_tokens = num_tokens_from_messages([{'key':prompt}],self.model)

        # retrieve from memory
        previous_messages = self.plant_list[self.id]['recent']
        relevant_docs = self.memory.get_relevant_documents(str(previous_messages))
        relevant_memory = [d.page_content for d in relevant_docs]
        relevant_memory_tokens = num_tokens_from_messages([{'key':doc} for doc in relevant_memory], self.model)
        while used_tokens + relevant_memory_tokens > 2500:
            relevant_memory = relevant_memory[:-1]
            relevant_memory_tokens = num_tokens_from_messages([{'key':doc} for doc in relevant_memory], self.model)
        prompt += '''\nYour past relevent messages:\n%s\n\n''' % str(relevant_memory)

        return prompt


    def run(self):
        system_prompt = self.prompt_builder()
        messages = [{"role": "system", "content":system_prompt}]
        messages += [{"role": chat.split(':')[0], "content":chat.split(':',1)[1]} for chat in self.plant_list[self.id]['recent']]
        messages += [{"role": "user", "content": self.user_input}]
        messages += [{"role": "system", "content": 'always give short answer, except for explaining'}]
        response = openai.ChatCompletion.create(
            model = self.model,
            messages = messages,
            stop = ['user:','assistant:']
        )
        reply = response["choices"][0]["message"]["content"]
        self.plant_list[self.id]['recent'].append('user:' + self.user_input)
        self.plant_list[self.id]['recent'].append('assistant:' + reply)
        tokens_count = num_tokens_from_messages([{'key':doc} for doc in self.plant_list[self.id]['recent']], self.model)
        print(tokens_count)
        while tokens_count > 1000:
            oldest_input = self.plant_list[self.id]['recent'].pop(0)
            oldest_answer = self.plant_list[self.id]['recent'].pop(0)
            self.plant_list[self.id]['legacy'].append(oldest_input)
            self.plant_list[self.id]['legacy'].append(oldest_answer)
            print(tokens_count)
            tokens_count = num_tokens_from_messages([{'key':doc} for doc in self.plant_list[self.id]['recent']], self.model)
        print(reply)
        return self.plant_list[self.id], reply

# Token counter
def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301"):
    """Returns the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-3.5-turbo":
        print("Warning: gpt-3.5-turbo may change over time. Returning num tokens assuming gpt-3.5-turbo-0301.")
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301")
    elif model == "gpt-4":
        print("Warning: gpt-4 may change over time. Returning num tokens assuming gpt-4-0314.")
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

plant_list = {'plant0':
                  {'name': 'rose',
                   'personality': 'cheerful, funny, love sun',
                   'legacy': [],
                   'recent': ['user:who are you?',
                              "assistant:Hello there! I'm Rose, a virtual consciousness of a real-life rose plant. I was created by Plant Reminder app to be a companion and a helpful friend to you, Anshler. How can I assist you today?"]
                   }
              }
current_user = 'Anshler'
while True:
    prompt = input('say something: ')
    id = 'plant0'
    model = PlantGPT(user_input=prompt,user=current_user,plant_list=plant_list,id=id)
    plant_list[id], answer = model.run()
