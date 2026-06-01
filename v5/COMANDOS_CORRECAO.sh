#!/bin/bash
# Script de Correção Automática - IBM watsonx.ai
# Execute: bash COMANDOS_CORRECAO.sh

echo "========================================================================"
echo "🔧 CORREÇÃO AUTOMÁTICA - IBM WATSONX.AI"
echo "========================================================================"
echo ""

# Verificar versão do Python
echo "1️⃣  Verificando versão do Python..."
PYTHON_VERSION=$(python3 --version 2>&1 | grep -oE '[0-9]+\.[0-9]+' | head -1)
MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

echo "   Python detectado: $PYTHON_VERSION"

if [ "$MAJOR" -lt 3 ] || ([ "$MAJOR" -eq 3 ] && [ "$MINOR" -lt 10 ]); then
    echo "   ❌ Python $PYTHON_VERSION é incompatível!"
    echo "   ⚠️  IBM watsonx.ai requer Python 3.10 ou superior"
    echo ""
    echo "   💡 SOLUÇÕES:"
    echo ""
    echo "   A) Instalar Python 3.11 via Homebrew:"
    echo "      brew install python@3.11"
    echo ""
    echo "   B) Baixar de: https://www.python.org/downloads/"
    echo ""
    echo "   C) Usar versão antiga do pacote (temporário):"
    echo "      pip install ibm-watson-machine-learning==1.0.335"
    echo ""
    echo "   📖 Consulte: ERRO_PYTHON_39.md para guia completo"
    echo ""
    exit 1
else
    echo "   ✅ Python $PYTHON_VERSION é compatível!"
fi

echo ""

# Verificar se está em ambiente virtual
echo "2️⃣  Verificando ambiente virtual..."
if [ -z "$VIRTUAL_ENV" ]; then
    echo "   ⚠️  Ambiente virtual não ativado"
    echo ""
    echo "   💡 Ativando ambiente virtual..."
    
    # Tentar ativar .venv
    if [ -d "../.venv" ]; then
        source ../.venv/bin/activate
        echo "   ✅ Ambiente virtual ativado!"
    elif [ -d ".venv" ]; then
        source .venv/bin/activate
        echo "   ✅ Ambiente virtual ativado!"
    else
        echo "   ❌ Ambiente virtual não encontrado"
        echo ""
        echo "   💡 Criando ambiente virtual..."
        cd ..
        python3 -m venv .venv
        source .venv/bin/activate
        cd v5
        echo "   ✅ Ambiente virtual criado e ativado!"
    fi
else
    echo "   ✅ Ambiente virtual já ativado: $VIRTUAL_ENV"
fi

echo ""

# Atualizar pip
echo "3️⃣  Atualizando pip..."
pip install --upgrade pip --quiet
echo "   ✅ pip atualizado!"

echo ""

# Instalar dependências
echo "4️⃣  Instalando dependências..."
echo "   (Isso pode levar alguns minutos...)"
echo ""

pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "   ✅ Dependências instaladas com sucesso!"
else
    echo ""
    echo "   ❌ Erro ao instalar dependências"
    echo ""
    echo "   💡 Se o erro for relacionado ao Python 3.9:"
    echo "      1. Instale Python 3.11: brew install python@3.11"
    echo "      2. Recrie o ambiente virtual com Python 3.11"
    echo "      3. Execute este script novamente"
    echo ""
    echo "   📖 Consulte: ERRO_PYTHON_39.md"
    exit 1
fi

echo ""

# Verificar arquivo .env
echo "5️⃣  Verificando arquivo .env..."
if [ ! -f ".env" ]; then
    echo "   ⚠️  Arquivo .env não encontrado"
    echo ""
    echo "   💡 Criando .env a partir do template..."
    cp .env.example .env
    echo "   ✅ Arquivo .env criado!"
    echo ""
    echo "   ⚠️  IMPORTANTE: Edite o arquivo .env com suas credenciais:"
    echo "      - IBM_WATSONX_API_KEY"
    echo "      - IBM_WATSONX_PROJECT_ID"
    echo ""
    echo "   📖 Consulte: SOLUCAO_RAPIDA.md para obter credenciais"
else
    echo "   ✅ Arquivo .env encontrado!"
    
    # Verificar se credenciais estão configuradas
    if grep -q "your_api_key_here" .env; then
        echo "   ⚠️  API Key ainda não configurada (usando valor padrão)"
        echo ""
        echo "   💡 Edite o .env e configure sua API Key real"
    fi
    
    if grep -q "your_project_id_here" .env; then
        echo "   ⚠️  Project ID ainda não configurado (usando valor padrão)"
        echo ""
        echo "   💡 Edite o .env e configure seu Project ID real"
    fi
fi

echo ""

# Executar diagnóstico
echo "6️⃣  Executando diagnóstico..."
echo ""
python test_watsonx.py

echo ""
echo "========================================================================"
echo "✅ CORREÇÃO CONCLUÍDA!"
echo "========================================================================"
echo ""
echo "📋 PRÓXIMOS PASSOS:"
echo ""
echo "   1. Se o diagnóstico mostrou erros, corrija-os"
echo "   2. Configure suas credenciais no arquivo .env"
echo "   3. Execute o scraper:"
echo "      python scraper_v5_ai.py"
echo ""
echo "📚 DOCUMENTAÇÃO:"
echo "   - SOLUCAO_RAPIDA.md - Guia rápido (3 passos)"
echo "   - ERRO_PYTHON_39.md - Solução para Python 3.9"
echo "   - CORRIGIR_WATSONX.md - Guia completo"
echo ""
echo "========================================================================"

# Made with Bob
