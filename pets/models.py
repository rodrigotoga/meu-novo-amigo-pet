from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

Usuario = get_user_model()


class Pet(models.Model):
    """Modelo para representar um pet disponível para adoção"""
    
    ESPECIE_CHOICES = [
        ('Cão', 'Cão'),
        ('Gato', 'Gato'),
        ('Outro', 'Outro'),
    ]
    
    PORTE_CHOICES = [
        ('Pequeno', 'Pequeno'),
        ('Médio', 'Médio'),
        ('Grande', 'Grande'),
    ]
    
    SEXO_CHOICES = [
        ('Macho', 'Macho'),
        ('Fêmea', 'Fêmea'),
    ]
    
    STATUS_ANUNCIO_CHOICES = [
        ('Pendente', 'Pendente de Moderação'),
        ('Aprovado', 'Aprovado'),
        ('Rejeitado', 'Rejeitado'),
    ]
    
    STATUS_ADOCAO_CHOICES = [
        ('Disponível', 'Disponível'),
        ('Em Processo', 'Em Processo'),
        ('Adotado', 'Adotado'),
    ]
    
    # Informações básicas
    doador = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE, 
        related_name='pets_doados',
        verbose_name="Doador"
    )
    nome = models.CharField(max_length=100, verbose_name="Nome do pet")
    especie = models.CharField(
        max_length=10, 
        choices=ESPECIE_CHOICES, 
        verbose_name="Espécie"
    )
    porte = models.CharField(
        max_length=10, 
        choices=PORTE_CHOICES, 
        verbose_name="Porte"
    )
    sexo = models.CharField(
        max_length=10, 
        choices=SEXO_CHOICES, 
        verbose_name="Sexo"
    )
    idade_meses = models.PositiveIntegerField(
        verbose_name="Idade (meses)",
        help_text="Idade aproximada em meses"
    )
    
    # Descrição e história
    descricao = models.TextField(
        verbose_name="Descrição",
        help_text="Descrição geral do pet"
    )
    historia = models.TextField(
        blank=True, 
        null=True,
        verbose_name="História",
        help_text="História do pet, como foi resgatado, etc."
    )
    informacoes_saude = models.TextField(
        blank=True, 
        null=True,
        verbose_name="Informações de saúde",
        help_text="Vacinas, castração, problemas de saúde, etc."
    )
    
    # Localização
    cidade = models.CharField(max_length=100, verbose_name="Cidade")
    estado = models.CharField(max_length=2, verbose_name="Estado")
    
    # Status
    status_anuncio = models.CharField(
        max_length=20, 
        choices=STATUS_ANUNCIO_CHOICES, 
        default='Pendente',
        verbose_name="Status do anúncio"
    )
    status_adocao = models.CharField(
        max_length=20, 
        choices=STATUS_ADOCAO_CHOICES, 
        default='Disponível',
        verbose_name="Status da adoção"
    )
    
    # Metadados
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name="Data de cadastro")
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name="Data de atualização")
    
    # Motivo de rejeição (se aplicável)
    motivo_rejeicao = models.TextField(
        blank=True, 
        null=True,
        verbose_name="Motivo da rejeição"
    )
    
    class Meta:
        verbose_name = "Pet"
        verbose_name_plural = "Pets"
        db_table = 'pet'
        ordering = ['-data_cadastro']
    
    def __str__(self):
        return f"{self.nome} - {self.especie} ({self.cidade}/{self.estado})"
    
    def is_aprovado(self):
        """Verifica se o anúncio está aprovado"""
        return self.status_anuncio == 'Aprovado'
    
    def is_disponivel(self):
        """Verifica se o pet está disponível para adoção"""
        return self.is_aprovado() and self.status_adocao == 'Disponível'
    
    def get_idade_formatada(self):
        """Retorna a idade formatada em anos e meses"""
        anos = self.idade_meses // 12
        meses = self.idade_meses % 12
        
        if anos > 0 and meses > 0:
            return f"{anos} ano{'s' if anos > 1 else ''} e {meses} mês{'es' if meses > 1 else ''}"
        elif anos > 0:
            return f"{anos} ano{'s' if anos > 1 else ''}"
        else:
            return f"{meses} mês{'es' if meses > 1 else ''}"


class FotoPet(models.Model):
    """Modelo para armazenar fotos dos pets"""
    
    pet = models.ForeignKey(
        Pet, 
        on_delete=models.CASCADE, 
        related_name='fotos',
        verbose_name="Pet"
    )
    imagem = models.ImageField(
        upload_to='pets/fotos/',
        verbose_name="Imagem"
    )
    descricao = models.CharField(
        max_length=255, 
        blank=True, 
        null=True,
        verbose_name="Descrição da foto"
    )
    ordem = models.PositiveIntegerField(
        default=0,
        verbose_name="Ordem",
        help_text="Ordem de exibição das fotos"
    )
    data_upload = models.DateTimeField(auto_now_add=True, verbose_name="Data do upload")
    
    class Meta:
        verbose_name = "Foto do Pet"
        verbose_name_plural = "Fotos dos Pets"
        db_table = 'foto_pet'
        ordering = ['ordem', 'data_upload']
    
    def __str__(self):
        return f"Foto de {self.pet.nome}"


class CandidaturaAdocao(models.Model):
    """Modelo para candidaturas de adoção"""
    
    STATUS_CHOICES = [
        ('Enviada', 'Enviada'),
        ('Visualizada', 'Visualizada'),
        ('Respondida', 'Respondida'),
    ]
    
    pet = models.ForeignKey(
        Pet, 
        on_delete=models.CASCADE,
        related_name='candidaturas',
        verbose_name="Pet"
    )
    candidato = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE,
        related_name='candidaturas',
        verbose_name="Candidato"
    )
    
    # Respostas do formulário de candidatura
    respostas_formulario = models.JSONField(
        verbose_name="Respostas do formulário",
        help_text="Respostas do candidato no formulário de adoção"
    )
    
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='Enviada',
        verbose_name="Status"
    )
    
    data_envio = models.DateTimeField(auto_now_add=True, verbose_name="Data de envio")
    data_visualizacao = models.DateTimeField(
        blank=True, 
        null=True,
        verbose_name="Data de visualização"
    )
    data_resposta = models.DateTimeField(
        blank=True, 
        null=True,
        verbose_name="Data da resposta"
    )
    
    # Observações do doador
    observacoes_doador = models.TextField(
        blank=True, 
        null=True,
        verbose_name="Observações do doador"
    )
    
    class Meta:
        verbose_name = "Candidatura de Adoção"
        verbose_name_plural = "Candidaturas de Adoção"
        db_table = 'candidatura_adocao'
        ordering = ['-data_envio']
        unique_together = ['pet', 'candidato']  # Um candidato só pode se candidatar uma vez por pet
    
    def __str__(self):
        return f"Candidatura de {self.candidato.nome} para {self.pet.nome}"
    
    def marcar_como_visualizada(self):
        """Marca a candidatura como visualizada"""
        if not self.data_visualizacao:
            self.data_visualizacao = timezone.now()
            self.status = 'Visualizada'
            self.save(update_fields=['data_visualizacao', 'status'])
    
    def marcar_como_respondida(self):
        """Marca a candidatura como respondida"""
        self.data_resposta = timezone.now()
        self.status = 'Respondida'
        self.save(update_fields=['data_resposta', 'status'])

