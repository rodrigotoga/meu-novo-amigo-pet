from django.contrib import admin
from .models import InteracaoChatIA, ConfiguracaoChatIA


@admin.register(InteracaoChatIA)
class InteracaoChatIAAdmin(admin.ModelAdmin):
    """Admin para o modelo InteracaoChatIA"""
    
    list_display = ('usuario', 'contexto', 'data_interacao', 'tempo_resposta_ms', 'feedback_positivo')
    list_filter = ('contexto', 'data_interacao', 'feedback_positivo')
    search_fields = ('usuario__nome', 'usuario__email', 'mensagem_usuario')
    ordering = ('-data_interacao',)
    
    fieldsets = (
        ('Informações da Interação', {
            'fields': ('usuario', 'contexto', 'sessao_id')
        }),
        ('Mensagens', {
            'fields': ('mensagem_usuario', 'resposta_ia')
        }),
        ('Métricas', {
            'fields': ('tempo_resposta_ms', 'feedback_positivo')
        }),
        ('Data', {
            'fields': ('data_interacao',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('data_interacao',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('usuario')


@admin.register(ConfiguracaoChatIA)
class ConfiguracaoChatIAAdmin(admin.ModelAdmin):
    """Admin para o modelo ConfiguracaoChatIA"""
    
    list_display = ('nome', 'ativo', 'data_criacao', 'data_atualizacao')
    list_filter = ('ativo', 'data_criacao')
    search_fields = ('nome', 'descricao')
    ordering = ('nome',)
    
    fieldsets = (
        ('Configuração', {
            'fields': ('nome', 'valor', 'descricao', 'ativo')
        }),
        ('Metadados', {
            'fields': ('data_criacao', 'data_atualizacao'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('data_criacao', 'data_atualizacao')