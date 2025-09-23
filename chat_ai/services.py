import re
from typing import Dict, List, Optional
from django.contrib.auth import get_user_model
from pets.models import Pet
from .models import InteracaoChatIA

Usuario = get_user_model()


class ChatIAService:
    """Serviço para processar mensagens do chat com IA"""
    
    def __init__(self):
        self.respostas_base = {
            'saudacao': [
                "Olá! 😊 Sou o assistente virtual da plataforma Meu Novo Amigo Pet. Como posso ajudá-lo hoje?",
                "Oi! Estou aqui para ajudá-lo a encontrar o pet perfeito ou tirar suas dúvidas sobre adoção! 🐾",
                "Olá! Bem-vindo à nossa plataforma! Posso ajudá-lo com informações sobre adoção, cuidados com pets e muito mais! 🐕🐱"
            ],
            'busca_pet': [
                "Vou ajudá-lo a encontrar o pet ideal! Que tipo de animal você está procurando?",
                "Ótimo! Vamos encontrar o companheiro perfeito para você. Me conte suas preferências!",
                "Adoro ajudar pessoas a encontrarem seus novos melhores amigos! 🐾 O que você está procurando?"
            ],
            'duvida_adocao': [
                "Fico feliz em esclarecer suas dúvidas sobre adoção! O que gostaria de saber?",
                "Adoção é um ato de amor! Vou ajudá-lo com todas as informações necessárias.",
                "Tire todas suas dúvidas! Estou aqui para orientá-lo no processo de adoção."
            ],
            'cuidados_pet': [
                "Cuidar de um pet é uma responsabilidade linda! Vou compartilhar dicas importantes com você.",
                "Ótima pergunta! Cuidar bem do seu pet é fundamental para uma vida feliz juntos.",
                "Vou te ajudar com informações sobre cuidados essenciais para seu pet! 🐾"
            ],
            'suporte_tecnico': [
                "Vou ajudá-lo com questões técnicas da plataforma. Qual é o problema?",
                "Estou aqui para resolver suas dúvidas sobre o uso da plataforma!",
                "Problemas técnicos? Vamos resolver isso juntos!"
            ]
        }
        
        self.palavras_chave = {
            'saudacao': ['oi', 'olá', 'bom dia', 'boa tarde', 'boa noite', 'hello', 'hi'],
            'busca_pet': ['procurar', 'buscar', 'encontrar', 'adotar', 'pet', 'cachorro', 'gato', 'animal'],
            'duvida_adocao': ['adoção', 'adotar', 'processo', 'como', 'quero', 'dúvida'],
            'cuidados_pet': ['cuidar', 'cuidados', 'alimentação', 'vacina', 'castração', 'saúde'],
            'suporte_tecnico': ['problema', 'erro', 'não funciona', 'ajuda', 'suporte', 'técnico']
        }
    
    def processar_mensagem(self, mensagem: str, contexto: str, usuario: Usuario) -> str:
        """Processa a mensagem do usuário e retorna uma resposta"""
        mensagem_lower = mensagem.lower()
        
        # Determinar o contexto baseado na mensagem
        contexto_detectado = self._detectar_contexto(mensagem_lower)
        
        # Processar baseado no contexto
        if contexto_detectado == 'busca_pet':
            return self._processar_busca_pet(mensagem, usuario)
        elif contexto_detectado == 'duvida_adocao':
            return self._processar_duvida_adocao(mensagem)
        elif contexto_detectado == 'cuidados_pet':
            return self._processar_cuidados_pet(mensagem)
        elif contexto_detectado == 'suporte_tecnico':
            return self._processar_suporte_tecnico(mensagem)
        else:
            return self._resposta_generica(mensagem, usuario)
    
    def _detectar_contexto(self, mensagem: str) -> str:
        """Detecta o contexto da mensagem baseado em palavras-chave"""
        for contexto, palavras in self.palavras_chave.items():
            for palavra in palavras:
                if palavra in mensagem:
                    return contexto
        return 'saudacao'
    
    def _processar_busca_pet(self, mensagem: str, usuario: Usuario) -> str:
        """Processa busca de pets"""
        # Extrair preferências da mensagem
        preferencias = self._extrair_preferencias_pet(mensagem)
        
        # Buscar pets compatíveis
        pets_compatíveis = self._buscar_pets_compatíveis(preferencias, usuario)
        
        if pets_compatíveis:
            resposta = "Encontrei alguns pets que podem ser perfeitos para você! 🐾\n\n"
            for i, pet in enumerate(pets_compatíveis[:3], 1):
                resposta += f"{i}. **{pet.nome}** - {pet.especie} {pet.porte}\n"
                resposta += f"   📍 {pet.cidade}/{pet.estado}\n"
                resposta += f"   🎂 {pet.get_idade_formatada()}\n"
                if pet.doador.verificado:
                    resposta += f"   ✅ ONG/Protetor Verificado\n"
                resposta += "\n"
            
            resposta += "Quer ver mais detalhes de algum deles? Acesse nossa página de busca! 🔍"
        else:
            resposta = "Não encontrei pets que correspondam exatamente às suas preferências, mas temos muitos outros pets incríveis esperando por um lar! 🐾\n\nQue tal dar uma olhada na nossa página de busca? Você pode usar os filtros para encontrar o pet perfeito!"
        
        return resposta
    
    def _extrair_preferencias_pet(self, mensagem: str) -> Dict:
        """Extrai preferências do pet da mensagem"""
        preferencias = {}
        mensagem_lower = mensagem.lower()
        
        # Espécie
        if 'cachorro' in mensagem_lower or 'cão' in mensagem_lower or 'dog' in mensagem_lower:
            preferencias['especie'] = 'Cão'
        elif 'gato' in mensagem_lower or 'cat' in mensagem_lower:
            preferencias['especie'] = 'Gato'
        
        # Porte
        if 'pequeno' in mensagem_lower or 'mini' in mensagem_lower:
            preferencias['porte'] = 'Pequeno'
        elif 'médio' in mensagem_lower or 'medio' in mensagem_lower:
            preferencias['porte'] = 'Médio'
        elif 'grande' in mensagem_lower:
            preferencias['porte'] = 'Grande'
        
        # Sexo
        if 'macho' in mensagem_lower or 'machinho' in mensagem_lower:
            preferencias['sexo'] = 'Macho'
        elif 'fêmea' in mensagem_lower or 'femea' in mensagem_lower or 'fêmea' in mensagem_lower:
            preferencias['sexo'] = 'Fêmea'
        
        # Idade
        if 'filhote' in mensagem_lower or 'bebê' in mensagem_lower or 'bebe' in mensagem_lower:
            preferencias['idade_max'] = 6
        elif 'jovem' in mensagem_lower:
            preferencias['idade_max'] = 24
        elif 'adulto' in mensagem_lower:
            preferencias['idade_min'] = 12
        
        return preferencias
    
    def _buscar_pets_compatíveis(self, preferencias: Dict, usuario: Usuario) -> List[Pet]:
        """Busca pets compatíveis com as preferências"""
        queryset = Pet.objects.filter(
            status_anuncio='Aprovado',
            status_adocao='Disponível'
        ).select_related('doador').prefetch_related('fotos')
        
        # Aplicar filtros baseados nas preferências
        if 'especie' in preferencias:
            queryset = queryset.filter(especie=preferencias['especie'])
        
        if 'porte' in preferencias:
            queryset = queryset.filter(porte=preferencias['porte'])
        
        if 'sexo' in preferencias:
            queryset = queryset.filter(sexo=preferencias['sexo'])
        
        if 'idade_max' in preferencias:
            queryset = queryset.filter(idade_meses__lte=preferencias['idade_max'])
        
        if 'idade_min' in preferencias:
            queryset = queryset.filter(idade_meses__gte=preferencias['idade_min'])
        
        # Priorizar pets da mesma cidade/estado do usuário
        if usuario.cidade and usuario.estado:
            queryset = queryset.filter(
                cidade__icontains=usuario.cidade,
                estado=usuario.estado
            )
        
        return list(queryset[:6])  # Máximo 6 sugestões
    
    def _processar_duvida_adocao(self, mensagem: str) -> str:
        """Processa dúvidas sobre adoção"""
        mensagem_lower = mensagem.lower()
        
        if 'processo' in mensagem_lower or 'como' in mensagem_lower:
            return """O processo de adoção é bem simples! 😊

1️⃣ **Encontre seu pet**: Use nossa busca para encontrar o pet ideal
2️⃣ **Crie sua conta**: Cadastre-se gratuitamente na plataforma
3️⃣ **Candidature-se**: Preencha o formulário de candidatura
4️⃣ **Aguarde contato**: O doador entrará em contato com você
5️⃣ **Conheça o pet**: Agende uma visita para conhecer seu novo amigo
6️⃣ **Adote com amor**: Leve seu novo companheiro para casa!

Tem alguma dúvida específica sobre algum desses passos?"""
        
        elif 'documento' in mensagem_lower or 'papel' in mensagem_lower:
            return """Para adotar, você precisará de:

📋 **Documentos pessoais**:
• RG ou CNH
• CPF
• Comprovante de residência

🏠 **Comprovantes de moradia**:
• Comprovante de que pode ter pets no local
• Fotos do ambiente onde o pet viverá

💰 **Não há taxas**: A adoção é gratuita! 🎉

Algumas ONGs podem pedir documentos adicionais, mas isso é comunicado durante o processo."""
        
        elif 'custo' in mensagem_lower or 'preço' in mensagem_lower or 'valor' in mensagem_lower:
            return """A adoção é **100% gratuita**! 🎉

Mas é importante lembrar que ter um pet envolve custos mensais:

🍽️ **Alimentação**: R$ 50-200/mês (dependendo do porte)
🏥 **Veterinário**: R$ 100-300/mês (consultas, vacinas, medicamentos)
🛁 **Higiene**: R$ 30-80/mês (banho, produtos de limpeza)
🎾 **Brinquedos**: R$ 20-50/mês

O amor e carinho que você receberá não tem preço! 💕"""
        
        else:
            return """Ótima pergunta sobre adoção! 🐾

Posso ajudá-lo com informações sobre:
• Como funciona o processo de adoção
• Documentos necessários
• Custos envolvidos
• Cuidados básicos
• Preparação da casa

O que gostaria de saber especificamente?"""
    
    def _processar_cuidados_pet(self, mensagem: str) -> str:
        """Processa dúvidas sobre cuidados com pets"""
        mensagem_lower = mensagem.lower()
        
        if 'alimentação' in mensagem_lower or 'comida' in mensagem_lower or 'ração' in mensagem_lower:
            return """Alimentação é fundamental para a saúde do seu pet! 🍽️

🐕 **Para cães**:
• 2-3 refeições por dia
• Ração de qualidade adequada à idade e porte
• Água sempre disponível
• Evite alimentos humanos (especialmente chocolate, cebola, uva)

🐱 **Para gatos**:
• Ração seca sempre disponível
• Ração úmida 1-2x por dia
• Água fresca em local separado da comida
• Evite leite (pode causar diarreia)

💡 **Dica**: Consulte um veterinário para a quantidade ideal!"""
        
        elif 'vacina' in mensagem_lower or 'vacinação' in mensagem_lower:
            return """Vacinação é essencial para proteger seu pet! 💉

🐕 **Cães**:
• V8 ou V10 (anual)
• Antirrábica (anual)
• Giárdia (anual)
• Leishmaniose (em áreas endêmicas)

🐱 **Gatos**:
• V3 ou V4 (anual)
• Antirrábica (anual)
• FeLV (recomendada)

📅 **Cronograma**:
• Primeira dose: 45-60 dias
• Reforços: 21-30 dias
• Manutenção: Anual

⚠️ **Importante**: Mantenha a carteirinha de vacinação sempre atualizada!"""
        
        elif 'castração' in mensagem_lower or 'castrar' in mensagem_lower:
            return """Castração é um ato de amor e responsabilidade! ❤️

✅ **Benefícios**:
• Previne doenças (câncer de mama, útero, próstata)
• Reduz comportamento agressivo
• Evita fugas e brigas
• Controla superpopulação

⏰ **Idade ideal**:
• Cães: 6-12 meses
• Gatos: 4-6 meses

🏥 **Onde fazer**:
• Clínicas veterinárias
• ONGs (preços mais acessíveis)
• Campanhas gratuitas

💰 **Custo**: R$ 100-500 (varia por região e porte)

É um investimento na saúde e bem-estar do seu pet! 🐾"""
        
        else:
            return """Cuidar de um pet é uma responsabilidade linda! 🐾

Posso ajudá-lo com informações sobre:
• Alimentação adequada
• Vacinação e saúde
• Castração
• Exercícios e brincadeiras
• Higiene e banho
• Comportamento

O que gostaria de saber sobre cuidados com pets?"""
    
    def _processar_suporte_tecnico(self, mensagem: str) -> str:
        """Processa questões de suporte técnico"""
        return """Estou aqui para ajudar com questões técnicas! 🔧

**Problemas comuns e soluções**:

🔐 **Não consigo fazer login**:
• Verifique se o e-mail está correto
• Use a opção "Esqueci minha senha"
• Limpe o cache do navegador

📱 **Página não carrega**:
• Atualize a página (F5)
• Verifique sua conexão com internet
• Tente em outro navegador

📝 **Não consigo cadastrar pet**:
• Verifique se está logado
• Complete todos os campos obrigatórios
• Verifique o tamanho das imagens (máx. 5MB)

💬 **Chat não funciona**:
• Atualize a página
• Verifique se JavaScript está habilitado

Se o problema persistir, entre em contato conosco! 📧"""
    
    def _resposta_generica(self, mensagem: str, usuario: Usuario) -> str:
        """Resposta genérica quando não consegue classificar a mensagem"""
        import random
        
        respostas = [
            "Interessante! Posso ajudá-lo de várias formas: 🐾\n\n• Encontrar pets para adoção\n• Tirar dúvidas sobre adoção\n• Informações sobre cuidados\n• Suporte técnico\n\nO que gostaria de saber?",
            "Ótima pergunta! Estou aqui para ajudar! 😊\n\nPosso:\n🔍 Sugerir pets compatíveis com seu perfil\n📋 Explicar o processo de adoção\n🐕 Dar dicas de cuidados\n🛠️ Resolver problemas técnicos\n\nComo posso ajudá-lo hoje?",
            "Adoro conversar sobre pets! 🐾\n\nMe conte mais sobre o que você precisa:\n• Quer adotar um pet?\n• Tem dúvidas sobre cuidados?\n• Precisa de ajuda na plataforma?\n\nEstou aqui para ajudar!"
        ]
        
        return random.choice(respostas)
