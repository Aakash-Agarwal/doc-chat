from django.urls import path

from doc_chat_gpt import views

urlpatterns = [
    path("chat", views.chat),
]