#!/usr/bin/env python
import os
import django
from datetime import datetime

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meu_novo_amigo_pet.settings')
django.setup()

from django.contrib.auth import get_user_model
from pets.models import Pet

User = get_user_model()

print("🔍 Testando o banco de dados...")
print("=" * 50)

# Contar registros existentes
usuarios_count = User.objects.count()
pets_count = Pet.objects.count()

print(f"📊 Usuários no banco: {usuarios_count}")
print(f"🐾 Pets no banco: {pets_count}")

# Teste de performance - criar um usuário de teste
print("\n⏱️ Testando velocidade de salvamento...")
start_time = datetime.now()

try:
    # Criar usuário de teste (se não existir)
    test_user, created = User.objects.get_or_create(
        email='teste@exemplo.com',
        defaults={
            'username': 'teste_user',
            'nome': 'Usuário Teste',
            'password': 'pbkdf2_sha256$600000$test$test'  # Hash dummy
        }
    )
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds() * 1000  # em milissegundos
    
    if created:
        print(f"✅ Usuário criado em {duration:.2f} milissegundos")
    else:
        print(f"✅ Usuário já existia - consulta em {duration:.2f} milissegundos")
    
    # Teste de criação de pet
    start_time = datetime.now()
    
    test_pet, created = Pet.objects.get_or_create(
        nome='Pet Teste',
        defaults={
            'doador': test_user,
            'especie': 'Cão',
            'porte': 'Médio',
            'sexo': 'Macho',
            'idade_meses': 12,
            'descricao': 'Pet de teste para verificar performance',
            'cidade': 'São Paulo',
            'estado': 'SP'
        }
    )
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds() * 1000
    
    if created:
        print(f"✅ Pet criado em {duration:.2f} milissegundos")
    else:
        print(f"✅ Pet já existia - consulta em {duration:.2f} milissegundos")
    
    # Contar novamente
    usuarios_final = User.objects.count()
    pets_final = Pet.objects.count()
    
    print(f"\n📈 Resultado final:")
    print(f"   Usuários: {usuarios_count} → {usuarios_final}")
    print(f"   Pets: {pets_count} → {pets_final}")
    
    print(f"\n🎉 Banco de dados funcionando perfeitamente!")
    print(f"⚡ Velocidade: Operações em milissegundos")
    
except Exception as e:
    print(f"❌ Erro: {e}")
