from django.urls import path
from . import views
from .views import UsuarioRegistrationView



app_name = 'accounts'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('cadastrar/', UsuarioRegistrationView.as_view(), name='cadastrar'),
    path('register/', views.UsuarioRegistrationView.as_view(), name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('solicitacao-verificacao/', views.solicitacao_verificacao_ong, name='solicitacao_verificacao'),
]
