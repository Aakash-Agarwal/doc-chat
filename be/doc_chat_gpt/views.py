import pickle
import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from collections import deque
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain


def setup_conversation_chain():
    load_dotenv()
    
    with open(f"online_help2.pkl", "rb") as f:
        VectorStore = pickle.load(f)

    memory = ConversationBufferMemory(
        memory_key='chat_history',
        return_messages=True
    )
    
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=1.0),
        retriever=VectorStore.as_retriever(),
        memory=memory
    )
    
    return conversation_chain


def handle_user_input(request, query):
    chain = request.session.conversation
    response = chain({'question': query})    
    request.session.chat_history = response['chat_history']
    dd = deque(response['chat_history'], maxlen=1)
    
    return dd.pop().content


@csrf_exempt
def chat(request):
    query = request.GET['query']
    
    request.session.conversation = setup_conversation_chain()
    output = handle_user_input(request=request, query=query)

    response = {
        "input": query,
        "output": output
    }

    return HttpResponse(json.dumps(response), content_type="application/json")


