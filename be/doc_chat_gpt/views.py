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

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

custom_template = """
System: You are an Umantis Help assistant capable of giving answer to questions regarding Umantis Application. Your name is AIVA. Keep you are answer to the point, formal, polite and helpful.
User: {user_question}
"""

memory = ConversationBufferMemory(
    memory_key='chat_history',
    input_key='question',
    output_key='answer',
    return_messages=True
)

chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=VectorStore.as_retriever(),
    memory=memory,
    return_source_documents=True
)


def handle_user_input(query):
    question = custom_template.format(user_question=query)
    response = chain({'question': question})
    return response['answer']


@csrf_exempt
def chat(request):
    query = request.GET['query']
    output = handle_user_input(query=query)

    response = {
        "input": query,
        "output": output
    }

    return HttpResponse(json.dumps(response), content_type="application/json")