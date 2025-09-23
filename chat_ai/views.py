from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
import json
import time
from .models import InteracaoChatIA, ConfiguracaoChatIA
from .services import ChatIAService


@login_required
def chat_view(request):
    """View principal do chat com IA"""
    return render(request, 'chat_ai/chat.html')


@csrf_exempt
@require_http_methods(["POST"])
@login_required
def chat_api_view(request):
    """API para interação com o chat de IA"""
    try:
        data = json.loads(request.body)
        mensagem_usuario = data.get('mensagem', '').strip()
        contexto = data.get('contexto', 'InformacaoGeral')
        sessao_id = data.get('sessao_id', '')
        
        if not mensagem_usuario:
            return JsonResponse({
                'success': False,
                'error': 'Mensagem não pode estar vazia'
            })
        
        # Iniciar cronômetro
        start_time = time.time()
        
        # Processar mensagem com IA
        chat_service = ChatIAService()
        resposta_ia = chat_service.processar_mensagem(
            mensagem_usuario, 
            contexto, 
            request.user
        )
        
        # Calcular tempo de resposta
        tempo_resposta_ms = int((time.time() - start_time) * 1000)
        
        # Salvar interação
        interacao = InteracaoChatIA.objects.create(
            usuario=request.user,
            mensagem_usuario=mensagem_usuario,
            resposta_ia=resposta_ia,
            contexto=contexto,
            tempo_resposta_ms=tempo_resposta_ms,
            sessao_id=sessao_id
        )
        
        return JsonResponse({
            'success': True,
            'resposta': resposta_ia,
            'tempo_resposta': tempo_resposta_ms,
            'interacao_id': interacao.id
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Dados JSON inválidos'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Erro interno: {str(e)}'
        })


@csrf_exempt
@require_http_methods(["POST"])
@login_required
def feedback_chat_view(request):
    """API para feedback do chat"""
    try:
        data = json.loads(request.body)
        interacao_id = data.get('interacao_id')
        feedback = data.get('feedback')  # True para positivo, False para negativo
        
        if not interacao_id:
            return JsonResponse({
                'success': False,
                'error': 'ID da interação é obrigatório'
            })
        
        try:
            interacao = InteracaoChatIA.objects.get(
                id=interacao_id,
                usuario=request.user
            )
            interacao.feedback_positivo = feedback
            interacao.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Feedback registrado com sucesso'
            })
            
        except InteracaoChatIA.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Interação não encontrada'
            })
            
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Dados JSON inválidos'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Erro interno: {str(e)}'
        })


@login_required
def historico_chat_view(request):
    """View para histórico de conversas do usuário"""
    interacoes = InteracaoChatIA.objects.filter(
        usuario=request.user
    ).order_by('-data_interacao')[:50]  # Últimas 50 interações
    
    context = {
        'interacoes': interacoes,
    }
    return render(request, 'chat_ai/historico.html', context)


@login_required
def sugestoes_pets_view(request):
    """View para sugestões de pets baseadas no perfil do usuário"""
    from pets.models import Pet
    
    # Buscar pets compatíveis com o perfil do usuário
    pets_sugeridos = Pet.objects.filter(
        status_anuncio='Aprovado',
        status_adocao='Disponível'
    )
    
    # Aplicar filtros baseados no perfil do usuário
    if request.user.cidade and request.user.estado:
        pets_sugeridos = pets_sugeridos.filter(
            cidade__icontains=request.user.cidade,
            estado=request.user.estado
        )
    
    # Limitar a 6 sugestões
    pets_sugeridos = pets_sugeridos.select_related('doador').prefetch_related('fotos')[:6]
    
    context = {
        'pets_sugeridos': pets_sugeridos,
    }
    return render(request, 'chat_ai/sugestoes_pets.html', context)