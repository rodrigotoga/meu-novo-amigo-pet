from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import get_user_model
from .forms import UsuarioRegistrationForm, UsuarioProfileForm, VerificacaoONGForm
from .models import Usuario

User = get_user_model()


class CustomLoginView(LoginView):
    """View customizada para login"""
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('home')


class CustomLogoutView(LogoutView):
    """View customizada para logout"""
    next_page = reverse_lazy('home')


class UsuarioRegistrationView(CreateView):
    """View para cadastro de usuário"""
    model = User
    form_class = UsuarioRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request, 
            'Conta criada com sucesso! Faça login para continuar.'
        )
        return response


@login_required
def profile_view(request):
    """View para visualizar e editar perfil do usuário"""
    if request.method == 'POST':
        form = UsuarioProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('accounts:profile')
    else:
        form = UsuarioProfileForm(instance=request.user)
    
    context = {
        'form': form,
        'user': request.user,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def solicitacao_verificacao_ong(request):
    """View para solicitação de verificação de ONG"""
    if request.user.tipo_conta != 'ONG':
        messages.error(request, 'Apenas contas do tipo ONG podem solicitar verificação.')
        return redirect('accounts:profile')
    
    if request.user.verificado:
        messages.info(request, 'Sua conta já está verificada.')
        return redirect('accounts:profile')
    
    if request.method == 'POST':
        form = VerificacaoONGForm(request.POST, request.FILES)
        if form.is_valid():
            # Aqui você pode salvar a solicitação em uma tabela separada
            # ou enviar por email para o administrador
            messages.success(
                request, 
                'Solicitação de verificação enviada! Aguarde a análise do administrador.'
            )
            return redirect('accounts:profile')
    else:
        form = VerificacaoONGForm()
    
    context = {
        'form': form,
    }
    return render(request, 'accounts/solicitacao_verificacao.html', context)


@login_required
def dashboard_view(request):
    """Dashboard do usuário"""
    user = request.user
    
    # Estatísticas do usuário
    stats = {
        'pets_cadastrados': user.pets_doados.count(),
        'pets_aprovados': user.pets_doados.filter(status_anuncio='Aprovado').count(),
        'pets_pendentes': user.pets_doados.filter(status_anuncio='Pendente').count(),
        'candidaturas_enviadas': user.candidaturas.count(),
    }
    
    # Pets recentes do usuário
    pets_recentes = user.pets_doados.all()[:5]
    
    # Candidaturas recebidas (se for doador)
    candidaturas_recebidas = []
    for pet in user.pets_doados.all():
        candidaturas_recebidas.extend(pet.candidaturas.all())
    
    candidaturas_recebidas = candidaturas_recebidas[:10]  # Últimas 10
    
    context = {
        'user': user,
        'stats': stats,
        'pets_recentes': pets_recentes,
        'candidaturas_recebidas': candidaturas_recebidas,
    }
    
    return render(request, 'accounts/dashboard.html', context)