from django.urls import path
from . import views

app_name = 'pets'

urlpatterns = [
    # Páginas públicas
    path('', views.home_view, name='home'),
    path('buscar/', views.PetListView.as_view(), name='pet_list'),
    path('<int:pk>/', views.PetDetailView.as_view(), name='pet_detail'),
    
    # Páginas do usuário logado
    path('meus-pets/', views.meus_pets_view, name='meus_pets'),
    path('cadastrar/', views.PetCreateView.as_view(), name='pet_create'),
    path('<int:pk>/editar/', views.PetUpdateView.as_view(), name='pet_update'),
    path('<int:pet_id>/candidatar/', views.candidatura_adocao_view, name='candidatura_adocao'),
    path('<int:pet_id>/alterar-status/', views.alterar_status_pet_view, name='alterar_status'),
    
    # Candidaturas
    path('candidaturas-recebidas/', views.candidaturas_recebidas_view, name='candidaturas_recebidas'),
    path('candidatura/<int:candidatura_id>/', views.candidatura_detail_view, name='candidatura_detail'),
    path('candidatura/<int:candidatura_id>/responder/', views.responder_candidatura_view, name='responder_candidatura'),
]
