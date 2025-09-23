from django.db import models
from django.contrib.auth import get_user_model

Usuario = get_user_model()


class InteracaoChatIA(models.Model):
    """Modelo para registrar interações com o chat de IA"""
    
    CONTEXTO_CHOICES = [
        ('BuscaPet', 'Busca de Pet'),
        ('DuvidaAdocao', 'Dúvida sobre Adoção'),
        ('CuidadosPet', 'Cuidados com Pet'),
        ('SuporteTecnico', 'Suporte Técnico'),
        ('SugestaoPet', 'Sugestão de Pet'),
        ('InformacaoGeral', 'Informação Geral'),
    ]
    
    usuario = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE,
        related_name='interacoes_chat',
        verbose_name="Usuário"
    )
    mensagem_usuario = models.TextField(verbose_name="Mensagem do usuário")
    resposta_ia = models.TextField(verbose_name="Resposta da IA")
    contexto = models.CharField(
        max_length=20, 
        choices=CONTEXTO_CHOICES,
        verbose_name="Contexto da interação"
    )
    
    # Metadados da interação
    data_interacao = models.DateTimeField(auto_now_add=True, verbose_name="Data da interação")
    tempo_resposta_ms = models.PositiveIntegerField(
        blank=True, 
        null=True,
        verbose_name="Tempo de resposta (ms)"
    )
    
    # Feedback do usuário (opcional)
    feedback_positivo = models.BooleanField(
        blank=True, 
        null=True,
        verbose_name="Feedback positivo",
        help_text="Se o usuário avaliou a resposta como útil"
    )
    
    # Dados adicionais da sessão
    sessao_id = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        verbose_name="ID da sessão",
        help_text="Identificador da sessão de chat"
    )
    
    class Meta:
        verbose_name = "Interação Chat IA"
        verbose_name_plural = "Interações Chat IA"
        db_table = 'interacao_chat_ia'
        ordering = ['-data_interacao']
    
    def __str__(self):
        return f"Chat IA - {self.usuario.nome} - {self.data_interacao.strftime('%d/%m/%Y %H:%M')}"
    
    @classmethod
    def get_estatisticas_contexto(cls):
        """Retorna estatísticas de uso por contexto"""
        from django.db.models import Count
        return cls.objects.values('contexto').annotate(
            total=Count('id')
        ).order_by('-total')
    
    @classmethod
    def get_tempo_resposta_medio(cls):
        """Retorna o tempo médio de resposta da IA"""
        from django.db.models import Avg
        return cls.objects.filter(
            tempo_resposta_ms__isnull=False
        ).aggregate(
            tempo_medio=Avg('tempo_resposta_ms')
        )['tempo_medio']


class ConfiguracaoChatIA(models.Model):
    """Modelo para configurações do chat de IA"""
    
    nome = models.CharField(max_length=100, unique=True, verbose_name="Nome da configuração")
    valor = models.TextField(verbose_name="Valor")
    descricao = models.TextField(
        blank=True, 
        null=True,
        verbose_name="Descrição"
    )
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de criação")
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name="Data de atualização")
    
    class Meta:
        verbose_name = "Configuração Chat IA"
        verbose_name_plural = "Configurações Chat IA"
        db_table = 'configuracao_chat_ia'
    
    def __str__(self):
        return f"{self.nome}: {self.valor[:50]}..."
    
    @classmethod
    def get_configuracao(cls, nome, default=None):
        """Obtém uma configuração por nome"""
        try:
            config = cls.objects.get(nome=nome, ativo=True)
            return config.valor
        except cls.DoesNotExist:
            return default