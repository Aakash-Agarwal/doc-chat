from django.urls import path

from doc_chat_gpt import views

urlpatterns = [
    path("query", views.query, name="post_query"),
]