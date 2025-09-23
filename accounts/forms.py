from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

Usuario = get_user_model()


class UsuarioRegistrationForm(UserCreationForm):
    """Formulário de cadastro de usuário"""
    
    nome = forms.CharField(
        max_length=255,
        label="Nome completo",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu nome completo'
        })
    )
    
    email = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu e-mail'
        })
    )
    
    telefone = forms.CharField(
        max_length=20,
        required=False,
        label="Telefone",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '(11) 99999-9999'
        })
    )
    
    cidade = forms.CharField(
        max_length=100,
        required=False,
        label="Cidade",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite sua cidade'
        })
    )
    
    estado = forms.ChoiceField(
        choices=[
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
        ],
        required=False,
        label="Estado",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    tipo_conta = forms.ChoiceField(
        choices=Usuario.TIPO_CONTA_CHOICES,
        label="Tipo de conta",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    password1 = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite sua senha'
        })
    )
    
    password2 = forms.CharField(
        label="Confirmação de senha",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirme sua senha'
        })
    )
    
    class Meta:
        model = Usuario
        fields = ('nome', 'email', 'telefone', 'cidade', 'estado', 'tipo_conta', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove o campo username do formulário
        if 'username' in self.fields:
            del self.fields['username']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            raise ValidationError("Este e-mail já está cadastrado.")
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.nome = self.cleaned_data['nome']
        user.telefone = self.cleaned_data.get('telefone', '')
        user.cidade = self.cleaned_data.get('cidade', '')
        user.estado = self.cleaned_data.get('estado', '')
        user.tipo_conta = self.cleaned_data['tipo_conta']

        user.username = user.email 
        
        if commit:
            user.save()
        return user


class UsuarioProfileForm(forms.ModelForm):
    """Formulário para edição do perfil do usuário"""
    
    class Meta:
        model = Usuario
        fields = ('nome', 'telefone', 'cidade', 'estado', 'tipo_conta')
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'tipo_conta': forms.Select(attrs={'class': 'form-control'}),
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


class VerificacaoONGForm(forms.Form):
    """Formulário para solicitação de verificação de ONG"""
    
    nome_organizacao = forms.CharField(
        max_length=255,
        label="Nome da organização",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nome oficial da ONG/Organização'
        })
    )
    
    cnpj = forms.CharField(
        max_length=18,
        label="CNPJ",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '00.000.000/0000-00'
        })
    )
    
    endereco = forms.CharField(
        label="Endereço completo",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Endereço completo da organização'
        })
    )
    
    telefone_organizacao = forms.CharField(
        max_length=20,
        label="Telefone da organização",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '(11) 99999-9999'
        })
    )
    
    site = forms.URLField(
        required=False,
        label="Site da organização",
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'https://www.exemplo.com.br'
        })
    )
    
    descricao_atividades = forms.CharField(
        label="Descrição das atividades",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Descreva as atividades da organização relacionadas ao cuidado de animais'
        })
    )
    
    documentos_comprovatorios = forms.FileField(
        required=False,
        label="Documentos comprobatórios",
        widget=forms.FileInput(attrs={
            'class': 'form-control'
        }),
        help_text="Upload de documento que comprove a existência da organização (opcional)"
    )
    
    def clean_cnpj(self):
        cnpj = self.cleaned_data.get('cnpj')
        # Aqui você pode adicionar validação de CNPJ se necessário
        return cnpj
