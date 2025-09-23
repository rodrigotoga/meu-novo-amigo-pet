from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.html import format_html

class MeuNovoAmigoPetAdminSite(AdminSite):
    site_header = "Meu Novo Amigo Pet - Administração"
    site_title = "Meu Novo Amigo Pet"
    index_title = "Painel de Administração"

admin_site = MeuNovoAmigoPetAdminSite(name='admin')

# Registrar modelos
from accounts.models import Usuario
from pets.models import Pet, FotoPet, CandidaturaAdocao
from chat_ai.models import InteracaoChatIA, ConfiguracaoChatIA

# Importar admins customizados
from accounts.admin import UsuarioAdmin
from pets.admin import PetAdmin, FotoPetAdmin, CandidaturaAdocaoAdmin
from chat_ai.admin import InteracaoChatIAAdmin, ConfiguracaoChatIAAdmin

# Registrar no admin customizado
admin_site.register(Usuario, UsuarioAdmin)
admin_site.register(Pet, PetAdmin)
admin_site.register(FotoPet, FotoPetAdmin)
admin_site.register(CandidaturaAdocao, CandidaturaAdocaoAdmin)
admin_site.register(InteracaoChatIA, InteracaoChatIAAdmin)
admin_site.register(ConfiguracaoChatIA, ConfiguracaoChatIAAdmin)
