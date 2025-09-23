from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    """Modelo customizado de usuário para a plataforma Meu Novo Amigo Pet"""
    
    TIPO_CONTA_CHOICES = [
        ('Individual', 'Individual'),
        ('ONG', 'ONG'),
    ]
    
    nome = models.CharField(max_length=255, verbose_name="Nome completo")
    telefone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefone")
    cidade = models.CharField(max_length=100, blank=True, null=True, verbose_name="Cidade")
    estado = models.CharField(max_length=2, blank=True, null=True, verbose_name="Estado")
    tipo_conta = models.CharField(
        max_length=20, 
        choices=TIPO_CONTA_CHOICES, 
        default='Individual',
        verbose_name="Tipo de conta"
    )
    verificado = models.BooleanField(
        default=False, 
        verbose_name="Verificado",
        help_text="Selo de confiança para ONGs/Protetores"
    )
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de criação")
    
    # Campos do AbstractUser que vamos usar
    email = models.EmailField(unique=True, verbose_name="E-mail")
    first_name = None  # Não usaremos
    last_name = None   # Não usaremos
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome', 'username']
    
    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
        db_table = 'usuario'
    
    def __str__(self):
        return f"{self.nome} ({self.email})"
    
    def is_ong_verificada(self):
        """Verifica se é uma ONG verificada"""
        return self.tipo_conta == 'ONG' and self.verificado
    
    def get_full_name(self):
        return self.nome
    
    def get_short_name(self):
        return self.nome.split()[0] if self.nome else self.email