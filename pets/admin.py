from django.contrib import admin
from django.utils.html import format_html
from .models import Pet, FotoPet, CandidaturaAdocao


class FotoPetInline(admin.TabularInline):
    """Inline para fotos do pet"""
    model = FotoPet
    extra = 1
    fields = ('imagem', 'descricao', 'ordem')


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    """Admin para o modelo Pet"""
    
    list_display = ('nome', 'especie', 'porte', 'sexo', 'cidade', 'estado', 'status_anuncio', 'status_adocao', 'doador', 'data_cadastro')
    list_filter = ('especie', 'porte', 'sexo', 'status_anuncio', 'status_adocao', 'estado', 'data_cadastro')
    search_fields = ('nome', 'cidade', 'doador__nome', 'doador__email')
    list_editable = ('status_anuncio', 'status_adocao')
    ordering = ('-data_cadastro',)
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('doador', 'nome', 'especie', 'porte', 'sexo', 'idade_meses')
        }),
        ('Descrição', {
            'fields': ('descricao', 'historia', 'informacoes_saude')
        }),
        ('Localização', {
            'fields': ('cidade', 'estado')
        }),
        ('Status', {
            'fields': ('status_anuncio', 'status_adocao', 'motivo_rejeicao')
        }),
        ('Metadados', {
            'fields': ('data_cadastro', 'data_atualizacao'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('data_cadastro', 'data_atualizacao')
    inlines = [FotoPetInline]
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('doador').prefetch_related('fotos')
    
    def save_model(self, request, obj, form, change):
        # Se for ONG verificada, aprovar automaticamente
        if obj.doador.is_ong_verificada() and obj.status_anuncio == 'Pendente':
            obj.status_anuncio = 'Aprovado'
        super().save_model(request, obj, form, change)


@admin.register(FotoPet)
class FotoPetAdmin(admin.ModelAdmin):
    """Admin para o modelo FotoPet"""
    
    list_display = ('pet', 'descricao', 'ordem', 'data_upload')
    list_filter = ('data_upload', 'pet__especie')
    search_fields = ('pet__nome', 'descricao')
    ordering = ('pet', 'ordem', 'data_upload')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('pet')


@admin.register(CandidaturaAdocao)
class CandidaturaAdocaoAdmin(admin.ModelAdmin):
    """Admin para o modelo CandidaturaAdocao"""
    
    list_display = ('pet', 'candidato', 'status', 'data_envio', 'data_visualizacao')
    list_filter = ('status', 'data_envio', 'pet__especie')
    search_fields = ('pet__nome', 'candidato__nome', 'candidato__email')
    ordering = ('-data_envio',)
    
    fieldsets = (
        ('Informações da Candidatura', {
            'fields': ('pet', 'candidato', 'status')
        }),
        ('Respostas do Formulário', {
            'fields': ('respostas_formulario',),
            'classes': ('collapse',)
        }),
        ('Observações do Doador', {
            'fields': ('observacoes_doador',)
        }),
        ('Datas', {
            'fields': ('data_envio', 'data_visualizacao', 'data_resposta'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('data_envio', 'data_visualizacao', 'data_resposta')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('pet', 'candidato')
