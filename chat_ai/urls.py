from django.urls import path
from . import views

app_name = 'chat_ai'

urlpatterns = [
    path('', views.chat_view, name='chat'),
    path('api/mensagem/', views.chat_api_view, name='chat_api'),
    path('api/feedback/', views.feedback_chat_view, name='feedback_chat'),
    path('historico/', views.historico_chat_view, name='historico'),
    path('sugestoes-pets/', views.sugestoes_pets_view, name='sugestoes_pets'),
]
