import pickle
import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain


load_dotenv()
with open(f"online_help2.pkl", "rb") as f:
    VectorStore = pickle.load(f)

llm = ChatOpenAI(model="gpt-3.5-turbo-16k", temperature=0.5)

memory = ConversationBufferMemory(
    memory_key='chat_history',
    return_messages=True
)

chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=VectorStore.as_retriever(),
    memory=memory
)

def handle_user_input(query):    
    response = chain({'question': query})
    answer = response['chat_history'][-1:][0]
    print(response['answer'])
    return answer.content


@csrf_exempt
def chat(request):
    query = request.GET['query']
    output = handle_user_input(query=query)

    response = {
        "input": query,
        "output": output
    }

    return HttpResponse(json.dumps(response), content_type="application/json")