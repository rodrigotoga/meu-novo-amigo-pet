from django import forms
from django.core.exceptions import ValidationError
from .models import Pet, FotoPet, CandidaturaAdocao


class PetForm(forms.ModelForm):
    """Formulário para cadastro e edição de pets"""
    
    class Meta:
        model = Pet
        fields = [
            'nome', 'especie', 'porte', 'sexo', 'idade_meses',
            'descricao', 'historia', 'informacoes_saude',
            'cidade', 'estado'
        ]
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome do pet'
            }),
            'especie': forms.Select(attrs={'class': 'form-control'}),
            'porte': forms.Select(attrs={'class': 'form-control'}),
            'sexo': forms.Select(attrs={'class': 'form-control'}),
            'idade_meses': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '300'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descreva o pet: personalidade, comportamento, etc.'
            }),
            'historia': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Como foi resgatado? Qual a história do pet?'
            }),
            'informacoes_saude': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Vacinas, castração, problemas de saúde, etc.'
            }),
            'cidade': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cidade onde o pet está'
            }),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adicionar choices para estado
        self.fields['estado'].choices = [
            ('', 'Selecione o estado'),
            ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'),
            ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'),
            ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
            ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'),
            ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'),
            ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
            ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'),
            ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'),
            ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
            ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')
        ]
    
    def clean_idade_meses(self):
        idade = self.cleaned_data.get('idade_meses')
        if idade and idade > 300:  # 25 anos em meses
            raise ValidationError("A idade não pode ser superior a 25 anos.")
        return idade


class FotoPetForm(forms.ModelForm):
    """Formulário para upload de fotos do pet"""
    
    class Meta:
        model = FotoPet
        fields = ['imagem', 'descricao', 'ordem']
        widgets = {
            'imagem': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'descricao': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Descrição da foto (opcional)'
            }),
            'ordem': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
        }


class BuscaPetForm(forms.Form):
    """Formulário de busca de pets"""
    
    ESPECIE_CHOICES = [
        ('', 'Todas as espécies'),
        ('Cão', 'Cão'),
        ('Gato', 'Gato'),
        ('Outro', 'Outro'),
    ]
    
    PORTE_CHOICES = [
        ('', 'Todos os portes'),
        ('Pequeno', 'Pequeno'),
        ('Médio', 'Médio'),
        ('Grande', 'Grande'),
    ]
    
    SEXO_CHOICES = [
        ('', 'Qualquer sexo'),
        ('Macho', 'Macho'),
        ('Fêmea', 'Fêmea'),
    ]
    
    IDADE_CHOICES = [
        ('', 'Qualquer idade'),
        ('0-6', 'Filhote (0-6 meses)'),
        ('6-12', 'Jovem (6-12 meses)'),
        ('12-24', 'Adulto jovem (1-2 anos)'),
        ('24-60', 'Adulto (2-5 anos)'),
        ('60+', 'Idoso (5+ anos)'),
    ]
    
    especie = forms.ChoiceField(
        choices=ESPECIE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    porte = forms.ChoiceField(
        choices=PORTE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    sexo = forms.ChoiceField(
        choices=SEXO_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    idade = forms.ChoiceField(
        choices=IDADE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    cidade = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Cidade'
        })
    )
    
    estado = forms.ChoiceField(
        choices=[
            ('', 'Todos os estados'),
            ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'),
            ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'),
            ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
            ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'),
            ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'),
            ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
            ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'),
            ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'),
            ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
            ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    apenas_verificados = forms.BooleanField(
        required=False,
        label="Apenas ONGs/Protetores verificados",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )


class CandidaturaAdocaoForm(forms.ModelForm):
    """Formulário de candidatura para adoção"""
    
    # Perguntas do formulário de candidatura
    experiencia_pets = forms.ChoiceField(
        choices=[
            ('', 'Selecione uma opção'),
            ('Nenhuma', 'Nenhuma experiência'),
            ('Pouca', 'Pouca experiência'),
            ('Moderada', 'Experiência moderada'),
            ('Muita', 'Muita experiência'),
        ],
        label="Qual sua experiência com pets?",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    tipo_moradia = forms.ChoiceField(
        choices=[
            ('', 'Selecione uma opção'),
            ('Casa', 'Casa com quintal'),
            ('Apartamento', 'Apartamento'),
            ('Sitio', 'Sítio/Chácara'),
            ('Outro', 'Outro'),
        ],
        label="Tipo de moradia",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    tem_outros_pets = forms.ChoiceField(
        choices=[
            ('', 'Selecione uma opção'),
            ('Sim', 'Sim'),
            ('Não', 'Não'),
        ],
        label="Você tem outros pets?",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    tempo_disponivel = forms.ChoiceField(
        choices=[
            ('', 'Selecione uma opção'),
            ('Pouco', 'Pouco tempo (trabalho muito)'),
            ('Moderado', 'Tempo moderado'),
            ('Muito', 'Muito tempo disponível'),
        ],
        label="Quanto tempo você tem disponível para cuidar do pet?",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    motivo_adocao = forms.CharField(
        label="Qual o motivo da adoção?",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Conte-nos por que você quer adotar este pet...'
        })
    )
    
    como_conheceu = forms.CharField(
        label="Como você conheceu nossa plataforma?",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Redes sociais, indicação, busca na internet...'
        })
    )
    
    telefone_contato = forms.CharField(
        max_length=20,
        label="Telefone para contato",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '(11) 99999-9999'
        })
    )
    
    observacoes = forms.CharField(
        required=False,
        label="Observações adicionais",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'placeholder': 'Alguma informação adicional que gostaria de compartilhar?'
        })
    )
    
    class Meta:
        model = CandidaturaAdocao
        fields = []  # Campos serão preenchidos no save()
    
    def save(self, commit=True):
        # Coletar todas as respostas do formulário
        respostas = {
            'experiencia_pets': self.cleaned_data.get('experiencia_pets'),
            'tipo_moradia': self.cleaned_data.get('tipo_moradia'),
            'tem_outros_pets': self.cleaned_data.get('tem_outros_pets'),
            'tempo_disponivel': self.cleaned_data.get('tempo_disponivel'),
            'motivo_adocao': self.cleaned_data.get('motivo_adocao'),
            'como_conheceu': self.cleaned_data.get('como_conheceu'),
            'telefone_contato': self.cleaned_data.get('telefone_contato'),
            'observacoes': self.cleaned_data.get('observacoes'),
        }
        
        candidatura = super().save(commit=False)
        candidatura.respostas_formulario = respostas
        
        if commit:
            candidatura.save()
        return candidatura
