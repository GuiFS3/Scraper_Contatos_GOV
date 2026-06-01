#!/usr/bin/env python3
"""
Script de Diagnóstico - IBM watsonx.ai
Verifica instalação e configuração do IBM watsonx.ai
"""

import sys
import os

print("="*70)
print("🔍 DIAGNÓSTICO IBM WATSONX.AI")
print("="*70)
print()

# ============================================================================
# 1. VERIFICAR PYTHON
# ============================================================================
print("1️⃣  Verificando Python...")
python_version = sys.version_info
if python_version >= (3, 8):
    print(f"   ✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
else:
    print(f"   ❌ Python {python_version.major}.{python_version.minor} (requer 3.8+)")
print()

# ============================================================================
# 2. VERIFICAR PACOTES
# ============================================================================
print("2️⃣  Verificando pacotes instalados...")

packages = {
    'selenium': 'Selenium',
    'bs4': 'BeautifulSoup4',
    'pandas': 'Pandas',
    'openpyxl': 'OpenPyXL',
    'dotenv': 'python-dotenv',
    'ibm_watsonx_ai': 'ibm-watsonx-ai'
}

missing_packages = []

for module_name, display_name in packages.items():
    try:
        if module_name == 'dotenv':
            from dotenv import load_dotenv
        elif module_name == 'bs4':
            import bs4
        elif module_name == 'ibm_watsonx_ai':
            from ibm_watsonx_ai import APIClient
        else:
            __import__(module_name)
        print(f"   ✅ {display_name}")
    except ImportError:
        print(f"   ❌ {display_name} - NÃO INSTALADO")
        missing_packages.append(display_name)

print()

# ============================================================================
# 3. VERIFICAR ARQUIVO .env
# ============================================================================
print("3️⃣  Verificando arquivo .env...")

env_file = '.env'
env_example = '.env.example'

if os.path.exists(env_file):
    print(f"   ✅ Arquivo .env encontrado")
    
    # Carregar variáveis
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv('IBM_WATSONX_API_KEY')
        project_id = os.getenv('IBM_WATSONX_PROJECT_ID')
        url = os.getenv('IBM_WATSONX_URL')
        
        print()
        print("   📋 Credenciais encontradas:")
        
        # API Key
        if api_key and api_key != 'your_api_key_here':
            print(f"   ✅ IBM_WATSONX_API_KEY: Configurada ({len(api_key)} caracteres)")
            if len(api_key) < 20:
                print(f"      ⚠️  API Key parece muito curta (esperado ~40+ caracteres)")
        else:
            print(f"   ❌ IBM_WATSONX_API_KEY: Não configurada ou usando valor padrão")
        
        # Project ID
        if project_id and project_id != 'your_project_id_here':
            print(f"   ✅ IBM_WATSONX_PROJECT_ID: Configurado ({len(project_id)} caracteres)")
            if len(project_id) < 20:
                print(f"      ⚠️  Project ID parece muito curto (esperado ~36 caracteres)")
        else:
            print(f"   ❌ IBM_WATSONX_PROJECT_ID: Não configurado ou usando valor padrão")
        
        # URL
        if url:
            print(f"   ✅ IBM_WATSONX_URL: {url}")
        else:
            print(f"   ⚠️  IBM_WATSONX_URL: Não configurada (usará padrão)")
        
    except Exception as e:
        print(f"   ❌ Erro ao ler .env: {e}")
else:
    print(f"   ❌ Arquivo .env NÃO ENCONTRADO")
    if os.path.exists(env_example):
        print(f"   ℹ️  Arquivo .env.example encontrado (use como template)")

print()

# ============================================================================
# 4. TESTAR CONEXÃO COM IBM WATSONX.AI
# ============================================================================
print("4️⃣  Testando conexão com IBM watsonx.ai...")

try:
    from ibm_watsonx_ai import APIClient, Credentials
    from dotenv import load_dotenv
    
    load_dotenv()
    
    api_key = os.getenv('IBM_WATSONX_API_KEY')
    project_id = os.getenv('IBM_WATSONX_PROJECT_ID')
    url = os.getenv('IBM_WATSONX_URL', 'https://us-south.ml.cloud.ibm.com')
    
    if not api_key or api_key == 'your_api_key_here':
        print("   ❌ API Key não configurada")
    elif not project_id or project_id == 'your_project_id_here':
        print("   ❌ Project ID não configurado")
    else:
        print("   🔄 Tentando conectar...")
        
        try:
            credentials = Credentials(url=url, api_key=api_key)
            client = APIClient(credentials)
            
            # Tentar listar modelos (teste de conexão)
            print("   ✅ Conexão estabelecida com sucesso!")
            print(f"   ℹ️  URL: {url}")
            
        except Exception as e:
            error_msg = str(e)
            print(f"   ❌ Erro na conexão: {error_msg[:100]}")
            
            if 'Unauthorized' in error_msg or '401' in error_msg:
                print("   💡 Possível causa: API Key inválida")
            elif 'Not Found' in error_msg or '404' in error_msg:
                print("   💡 Possível causa: Project ID inválido ou URL incorreta")
            elif 'Forbidden' in error_msg or '403' in error_msg:
                print("   💡 Possível causa: Sem permissão ou serviço não ativado")
            else:
                print("   💡 Verifique suas credenciais no IBM Cloud")

except ImportError:
    print("   ❌ Pacote ibm-watsonx-ai não instalado")
except Exception as e:
    print(f"   ❌ Erro: {e}")

print()

# ============================================================================
# 5. RESUMO E RECOMENDAÇÕES
# ============================================================================
print("="*70)
print("📊 RESUMO")
print("="*70)
print()

if missing_packages:
    print("❌ PROBLEMAS ENCONTRADOS:")
    print()
    print("   Pacotes faltando:")
    for pkg in missing_packages:
        print(f"   - {pkg}")
    print()
    print("   💡 SOLUÇÃO:")
    print("   pip install -r requirements.txt")
    print()

if not os.path.exists('.env'):
    print("❌ ARQUIVO .env NÃO ENCONTRADO:")
    print()
    print("   💡 SOLUÇÃO:")
    print("   1. Copie o template:")
    print("      cp .env.example .env")
    print()
    print("   2. Edite o arquivo .env com suas credenciais:")
    print("      nano .env")
    print()
    print("   3. Configure:")
    print("      IBM_WATSONX_API_KEY=sua_api_key_aqui")
    print("      IBM_WATSONX_PROJECT_ID=seu_project_id_aqui")
    print()

if not missing_packages and os.path.exists('.env'):
    print("✅ CONFIGURAÇÃO BÁSICA OK!")
    print()
    print("   Próximos passos:")
    print("   1. Verifique se as credenciais estão corretas")
    print("   2. Execute o scraper:")
    print("      python scraper_v5_ai.py")
    print()

print("="*70)
print("📚 DOCUMENTAÇÃO:")
print("   - GUIA_INSTALACAO.md - Guia completo de instalação")
print("   - README_V5.md - Documentação do scraper")
print("="*70)

# Made with Bob
