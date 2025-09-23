# 🐾 Meu Novo Amigo Pet

Uma plataforma web completa para conectar animais que precisam de um lar a pessoas dispostas a oferecer amor, cuidado e uma segunda chance.

## 🎯 Sobre o Projeto

O "Meu Novo Amigo Pet" é um sistema web desenvolvido em Django que facilita a adoção responsável de animais, oferecendo:

- **Portal centralizado** para encontrar pets para adoção
- **Sistema de moderação** para garantir a qualidade dos anúncios
- **Chat com IA** para suporte e sugestões personalizadas
- **Processo transparente** de candidatura para adoção
- **Verificação de ONGs** para maior confiabilidade

## ✨ Funcionalidades Principais

### 👥 Para Usuários
- **Cadastro e perfil personalizado**
- **Busca avançada de pets** com filtros por espécie, porte, idade, localização
- **Sistema de candidatura** para adoção
- **Chat com IA** para suporte e sugestões
- **Histórico de interações**

### 🏢 Para ONGs/Protetores
- **Verificação de conta** para maior credibilidade
- **Aprovação automática** de anúncios (ONGs verificadas)
- **Gerenciamento de candidaturas** recebidas
- **Destaque visual** nos resultados de busca

### 👨‍💼 Para Administradores
- **Painel de moderação** para anúncios
- **Gerenciamento de usuários** e verificação de ONGs
- **Estatísticas e relatórios** da plataforma
- **Configuração do chat IA**

## 🚀 Tecnologias Utilizadas

- **Backend**: Django 5.2.6
- **Banco de Dados**: SQLite (desenvolvimento)
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **IA**: Sistema de chat inteligente com processamento de linguagem natural
- **Autenticação**: Sistema customizado de usuários

## 📋 Pré-requisitos

- Python 3.8+
- Django 5.2.6
- Pillow (para upload de imagens)

## 🛠️ Instalação e Configuração

### 1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd meu-novo-amigo-pet
```

### 2. Crie um ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3. Instale as dependências
```bash
pip install django pillow
```

### 4. Execute as migrações
```bash
python manage.py migrate
```

### 5. Crie um superusuário
```bash
python manage.py createsuperuser
```

### 6. Execute o servidor
```bash
python manage.py runserver
```

### 7. Acesse a aplicação
- **Site**: http://127.0.0.1:8000/
- **Admin**: http://127.0.0.1:8000/admin/

## 📱 Como Usar

### Para Usuários Comuns

1. **Cadastre-se** na plataforma
2. **Busque pets** usando os filtros disponíveis
3. **Visualize detalhes** do pet de interesse
4. **Candidature-se** para adoção preenchendo o formulário
5. **Use o chat IA** para tirar dúvidas e receber sugestões

### Para ONGs/Protetores

1. **Cadastre-se** como ONG
2. **Solicite verificação** no painel do usuário
3. **Cadastre pets** para adoção
4. **Gerencie candidaturas** recebidas
5. **Aprove automaticamente** (ONGs verificadas)

### Para Administradores

1. **Acesse o painel admin** em `/admin/`
2. **Modere anúncios** pendentes
3. **Verifique ONGs** solicitantes
4. **Gerencie usuários** e conteúdo
5. **Configure o chat IA**

## 🗂️ Estrutura do Projeto

```
meu_novo_amigo_pet/
├── accounts/           # Gerenciamento de usuários
├── pets/              # Sistema de pets e adoção
├── chat_ai/           # Chat com inteligência artificial
├── templates/         # Templates HTML
├── static/           # Arquivos estáticos (CSS, JS, imagens)
├── media/            # Uploads de usuários
└── meu_novo_amigo_pet/  # Configurações do projeto
```

## 🎨 Interface

A plataforma possui uma interface moderna e responsiva com:

- **Design limpo** e intuitivo
- **Navegação fácil** entre seções
- **Cards visuais** para pets
- **Chat interativo** com IA
- **Formulários otimizados** para mobile
- **Feedback visual** para ações do usuário

## 🤖 Chat com IA

O assistente virtual oferece:

- **Sugestões personalizadas** de pets
- **Orientações sobre adoção**
- **Dicas de cuidados** com animais
- **Suporte técnico** da plataforma
- **Processamento de linguagem natural**
- **Histórico de conversas**

## 🔒 Segurança

- **Autenticação segura** com senhas criptografadas
- **Proteção CSRF** em todos os formulários
- **Validação de dados** no frontend e backend
- **Upload seguro** de imagens
- **Controle de acesso** por tipo de usuário

## 📊 Modelos de Dados

### Usuario
- Informações pessoais e de contato
- Tipo de conta (Individual/ONG)
- Status de verificação
- Relacionamentos com pets e candidaturas

### Pet
- Informações básicas (nome, espécie, porte, etc.)
- Status de anúncio e adoção
- Localização e descrição
- Relacionamento com doador e fotos

### CandidaturaAdocao
- Formulário de candidatura em JSON
- Status de processamento
- Relacionamentos com pet e candidato

### InteracaoChatIA
- Histórico de conversas com IA
- Métricas de performance
- Feedback dos usuários

## 🚀 Deploy

Para produção, considere:

1. **Configurar banco PostgreSQL**
2. **Usar servidor web** (Nginx + Gunicorn)
3. **Configurar HTTPS**
4. **Otimizar arquivos estáticos**
5. **Configurar backup** do banco de dados

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 📞 Suporte

Para dúvidas ou suporte:
- **Email**: suporte@meunovoamigopet.com
- **Chat IA**: Disponível na plataforma
- **Documentação**: Este README

---

**Feito com ❤️ para conectar amor e cuidado aos nossos amigos de quatro patas! 🐾**
