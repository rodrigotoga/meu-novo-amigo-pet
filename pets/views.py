from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from .models import Pet, FotoPet, CandidaturaAdocao
from .forms import PetForm, FotoPetForm, BuscaPetForm, CandidaturaAdocaoForm


class PetListView(ListView):
    """View para listar pets disponíveis"""
    model = Pet
    template_name = 'pets/pet_list.html'
    context_object_name = 'pets'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Pet.objects.filter(
            status_anuncio='Aprovado',
            status_adocao='Disponível'
        ).select_related('doador').prefetch_related('fotos')
        
        # Aplicar filtros de busca
        form = BuscaPetForm(self.request.GET)
        if form.is_valid():
            especie = form.cleaned_data.get('especie')
            porte = form.cleaned_data.get('porte')
            sexo = form.cleaned_data.get('sexo')
            idade = form.cleaned_data.get('idade')
            cidade = form.cleaned_data.get('cidade')
            estado = form.cleaned_data.get('estado')
            apenas_verificados = form.cleaned_data.get('apenas_verificados')
            
            if especie:
                queryset = queryset.filter(especie=especie)
            if porte:
                queryset = queryset.filter(porte=porte)
            if sexo:
                queryset = queryset.filter(sexo=sexo)
            if idade:
                if idade == '0-6':
                    queryset = queryset.filter(idade_meses__lte=6)
                elif idade == '6-12':
                    queryset = queryset.filter(idade_meses__gte=6, idade_meses__lte=12)
                elif idade == '12-24':
                    queryset = queryset.filter(idade_meses__gte=12, idade_meses__lte=24)
                elif idade == '24-60':
                    queryset = queryset.filter(idade_meses__gte=24, idade_meses__lte=60)
                elif idade == '60+':
                    queryset = queryset.filter(idade_meses__gte=60)
            if cidade:
                queryset = queryset.filter(cidade__icontains=cidade)
            if estado:
                queryset = queryset.filter(estado=estado)
            if apenas_verificados:
                queryset = queryset.filter(doador__verificado=True)
        
        return queryset.order_by('-data_cadastro')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = BuscaPetForm(self.request.GET)
        return context


class PetDetailView(DetailView):
    """View para detalhes do pet"""
    model = Pet
    template_name = 'pets/pet_detail.html'
    context_object_name = 'pet'
    
    def get_queryset(self):
        return Pet.objects.select_related('doador').prefetch_related('fotos')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pet = self.get_object()
        
        # Verificar se o usuário já se candidatou
        if self.request.user.is_authenticated:
            context['ja_candidatou'] = CandidaturaAdocao.objects.filter(
                pet=pet,
                candidato=self.request.user
            ).exists()
        else:
            context['ja_candidatou'] = False
        
        return context


class PetCreateView(LoginRequiredMixin, CreateView):
    """View para cadastrar novo pet"""
    model = Pet
    form_class = PetForm
    template_name = 'pets/pet_form.html'
    success_url = reverse_lazy('pets:meus_pets')
    
    def form_valid(self, form):
        pet = form.save(commit=False)
        pet.doador = self.request.user
        
        # Se for ONG verificada, aprovar automaticamente
        if self.request.user.is_ong_verificada():
            pet.status_anuncio = 'Aprovado'
        else:
            pet.status_anuncio = 'Pendente'
        
        pet.save()
        
        if pet.status_anuncio == 'Aprovado':
            messages.success(
                self.request, 
                f'Pet "{pet.nome}" cadastrado e aprovado automaticamente!'
            )
        else:
            messages.success(
                self.request, 
                f'Pet "{pet.nome}" cadastrado! Aguarde a moderação.'
            )
        
        return redirect('pets:pet_detail', pk=pet.pk)


class PetUpdateView(LoginRequiredMixin, UpdateView):
    """View para editar pet"""
    model = Pet
    form_class = PetForm
    template_name = 'pets/pet_form.html'
    
    def get_queryset(self):
        return Pet.objects.filter(doador=self.request.user)
    
    def get_success_url(self):
        return reverse('pets:pet_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, f'Pet "{self.object.nome}" atualizado com sucesso!')
        return super().form_valid(form)


@login_required
def meus_pets_view(request):
    """View para listar pets do usuário logado"""
    pets = Pet.objects.filter(doador=request.user).order_by('-data_cadastro')
    
    # Estatísticas
    stats = {
        'total': pets.count(),
        'aprovados': pets.filter(status_anuncio='Aprovado').count(),
        'pendentes': pets.filter(status_anuncio='Pendente').count(),
        'rejeitados': pets.filter(status_anuncio='Rejeitado').count(),
        'disponiveis': pets.filter(status_adocao='Disponível').count(),
        'adotados': pets.filter(status_adocao='Adotado').count(),
    }
    
    context = {
        'pets': pets,
        'stats': stats,
    }
    return render(request, 'pets/meus_pets.html', context)


@login_required
def candidatura_adocao_view(request, pet_id):
    """View para candidatura de adoção"""
    pet = get_object_or_404(Pet, id=pet_id, status_anuncio='Aprovado', status_adocao='Disponível')
    
    # Verificar se já se candidatou
    if CandidaturaAdocao.objects.filter(pet=pet, candidato=request.user).exists():
        messages.warning(request, 'Você já se candidatou para adotar este pet.')
        return redirect('pets:pet_detail', pk=pet.id)
    
    if request.method == 'POST':
        form = CandidaturaAdocaoForm(request.POST)
        if form.is_valid():
            candidatura = form.save(commit=False)
            candidatura.pet = pet
            candidatura.candidato = request.user
            candidatura.save()
            
            messages.success(
                request, 
                f'Candidatura enviada com sucesso! O doador será notificado.'
            )
            return redirect('pets:pet_detail', pk=pet.id)
    else:
        form = CandidaturaAdocaoForm()
    
    context = {
        'form': form,
        'pet': pet,
    }
    return render(request, 'pets/candidatura_form.html', context)


@login_required
def candidaturas_recebidas_view(request):
    """View para candidaturas recebidas pelo usuário"""
    # Buscar candidaturas dos pets do usuário
    candidaturas = CandidaturaAdocao.objects.filter(
        pet__doador=request.user
    ).select_related('pet', 'candidato').order_by('-data_envio')
    
    context = {
        'candidaturas': candidaturas,
    }
    return render(request, 'pets/candidaturas_recebidas.html', context)


@login_required
def candidatura_detail_view(request, candidatura_id):
    """View para detalhes da candidatura"""
    candidatura = get_object_or_404(
        CandidaturaAdocao, 
        id=candidatura_id,
        pet__doador=request.user
    )
    
    # Marcar como visualizada
    candidatura.marcar_como_visualizada()
    
    context = {
        'candidatura': candidatura,
    }
    return render(request, 'pets/candidatura_detail.html', context)


@login_required
def responder_candidatura_view(request, candidatura_id):
    """View para responder candidatura"""
    candidatura = get_object_or_404(
        CandidaturaAdocao, 
        id=candidatura_id,
        pet__doador=request.user
    )
    
    if request.method == 'POST':
        observacoes = request.POST.get('observacoes', '')
        acao = request.POST.get('acao')
        
        candidatura.observacoes_doador = observacoes
        candidatura.marcar_como_respondida()
        
        if acao == 'aprovar':
            messages.success(request, 'Candidatura aprovada! Entre em contato com o candidato.')
        else:
            messages.info(request, 'Resposta enviada para o candidato.')
        
        return redirect('pets:candidaturas_recebidas')
    
    context = {
        'candidatura': candidatura,
    }
    return render(request, 'pets/responder_candidatura.html', context)


@login_required
def alterar_status_pet_view(request, pet_id):
    """View para alterar status de adoção do pet"""
    pet = get_object_or_404(Pet, id=pet_id, doador=request.user)
    
    if request.method == 'POST':
        novo_status = request.POST.get('status_adocao')
        if novo_status in ['Disponível', 'Em Processo', 'Adotado']:
            pet.status_adocao = novo_status
            pet.save()
            messages.success(request, f'Status do pet alterado para "{novo_status}".')
        
        return redirect('pets:meus_pets')
    
    context = {
        'pet': pet,
    }
    return render(request, 'pets/alterar_status.html', context)


def home_view(request):
    """View da página inicial"""
    # Pets em destaque (últimos aprovados)
    pets_destaque = Pet.objects.filter(
        status_anuncio='Aprovado',
        status_adocao='Disponível'
    ).select_related('doador').prefetch_related('fotos')[:6]
    
    # Estatísticas gerais
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    stats = {
        'total_pets': Pet.objects.filter(status_anuncio='Aprovado').count(),
        'pets_disponiveis': Pet.objects.filter(
            status_anuncio='Aprovado',
            status_adocao='Disponível'
        ).count(),
        'total_usuarios': User.objects.count(),
    }
    
    context = {
        'pets_destaque': pets_destaque,
        'stats': stats,
    }
    return render(request, 'home.html', context)
