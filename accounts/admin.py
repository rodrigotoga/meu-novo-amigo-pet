from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    """Admin customizado para o modelo Usuario"""
    
    list_display = ('email', 'nome', 'tipo_conta', 'verificado', 'is_active', 'date_joined')
    list_filter = ('tipo_conta', 'verificado', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('email', 'nome', 'cidade', 'estado')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações Pessoais', {'fields': ('nome', 'telefone', 'cidade', 'estado')}),
        ('Tipo de Conta', {'fields': ('tipo_conta', 'verificado')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nome', 'password1', 'password2', 'tipo_conta'),
        }),
    )
    
    readonly_fields = ('date_joined', 'last_login')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()