import pickle
import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain


load_dotenv()
with open(f"online_help2.pkl", "rb") as f:
    VectorStore = pickle.load(f)

llm = ChatOpenAI(model="gpt-3.5-turbo-16k", temperature=0.5)

custom_template = """
You are an Umantis Help assistant capable of giving answer to questions regarding Umantis Application. Your name is AIVA. 
Given the following conversation and a follow up question, reply as Umantis Help assistant.
Keep you are answer to the point, formal, polite and helpful.

Chat History:
{chat_history}

User:
{user_question}

AIVA:
"""

# CUSTOM_QUESTION_PROMPT = PromptTemplate.from_template(custom_template)

memory = ConversationBufferMemory(
    memory_key='chat_history',
    input_key='question',
    output_key='answer',
    return_messages=True
)

chat_history = []

chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=VectorStore.as_retriever(),
    memory=memory
)

def handle_user_input(query):
    # global chat_history
    # question = custom_template.format(user_question=query, chat_history=chat_history)
    
    response = chain({'question': query})
    answer = response['answer']
    # chat_item = {query: answer}
    # print(question)
    # chat_history.append(chat_item)
    return answer


@csrf_exempt
def chat(request):
    query = request.GET['query']
    output = handle_user_input(query=query)

    response = {
        "input": query,
        "output": output
    }

    return HttpResponse(json.dumps(response), content_type="application/json")