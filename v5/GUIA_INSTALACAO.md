# Guia de Instalação - Scraper V5 AI-Powered 🚀

## 📋 Pré-requisitos

- Python 3.8 ou superior
- Google Chrome instalado
- Conta IBM Cloud (para watsonx.ai)
- Conexão com internet

---

## 🔧 Instalação Passo a Passo

### 1. Clonar/Baixar o Projeto

```bash
cd v5/
```

### 2. Criar Ambiente Virtual (Recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

**Dependências principais:**
- `selenium` - Automação do navegador
- `beautifulsoup4` - Parsing de HTML
- `pandas` - Manipulação de dados
- `ibm-watsonx-ai` - Integração com IBM AI
- `python-dotenv` - Gerenciamento de variáveis de ambiente

---

## 🔑 Configurar IBM watsonx.ai

### Passo 1: Criar Conta IBM Cloud

1. Acesse: https://cloud.ibm.com/
2. Clique em "Create an account" (ou faça login)
3. Complete o cadastro

### Passo 2: Ativar watsonx.ai

1. No dashboard IBM Cloud, busque por "watsonx.ai"
2. Clique em "Create" para criar uma instância
3. Escolha o plano:
   - **Lite** (gratuito) - Limitado, bom para testes
   - **Essentials** (pago) - Recomendado para produção

### Passo 3: Obter Credenciais

1. Acesse seu projeto watsonx.ai
2. Vá em "Manage" → "Access (IAM)"
3. Clique em "API keys" → "Create"
4. Copie a **API Key** gerada
5. Anote o **Project ID** (encontrado nas configurações do projeto)

### Passo 4: Configurar Variáveis de Ambiente

1. Copie o arquivo de exemplo:
```bash
cp .env.example .env
```

2. Edite o arquivo `.env`:
```env
IBM_WATSONX_API_KEY=sua_api_key_aqui
IBM_WATSONX_PROJECT_ID=seu_project_id_aqui
IBM_WATSONX_URL=https://us-south.ml.cloud.ibm.com
```

**⚠️ IMPORTANTE:** Nunca compartilhe seu arquivo `.env` ou faça commit dele no Git!

---

## 📝 Configurar Lista de Órgãos

Edite o arquivo `orgaos.txt`:

```
SIGLA|Nome do Órgão|URL
GOVERNO-PR|Governo do Estado do Paraná|https://www.parana.pr.gov.br/Pagina/Quemequem
TCE-PR|Tribunal de Contas do Estado do Paraná|https://www.tce.pr.gov.br/
```

**Formato:**
- Cada linha representa um órgão
- Campos separados por `|` (pipe)
- Linhas começando com `#` são ignoradas

---

## ▶️ Executar o Scraper

### Modo Básico (com interface gráfica)

```bash
python scraper_v5_ai.py
```

### Modo Headless (sem interface)

```bash
python scraper_v5_ai.py --headless
```

### Modo AI-Only (apenas IA, sem fallback)

```bash
python scraper_v5_ai.py --ai-only
```

### Modo Debug (verbose)

```bash
python scraper_v5_ai.py --debug
```

### Combinando Opções

```bash
python scraper_v5_ai.py --headless --ai-only
```

---

## 📊 Saída

O scraper gera um arquivo Excel com timestamp:
```
contatos_v5_ai_20260521_120000.xlsx
```

**Abas do Excel:**
1. **Contatos TI** - Dados extraídos
   - Órgão Nome
   - Órgão Sigla
   - Nome da Pessoa
   - Cargo / Setor
   - E-mail
   - Telefone
   - Confiança IA (0.0 a 1.0)
   - Método (IA ou Fallback)

2. **Log** - Registro de processamento
   - Órgão Sigla
   - Status
   - Método
   - Detalhes
   - Timestamp

---

## 🔍 Verificar Instalação

Execute este script de teste:

```python
# test_installation.py
import sys

print("Verificando instalação...")

# Verificar Python
print(f"✓ Python {sys.version}")

# Verificar pacotes
try:
    import selenium
    print(f"✓ Selenium {selenium.__version__}")
except:
    print("✗ Selenium não instalado")

try:
    import bs4
    print(f"✓ BeautifulSoup4 instalado")
except:
    print("✗ BeautifulSoup4 não instalado")

try:
    import pandas
    print(f"✓ Pandas {pandas.__version__}")
except:
    print("✗ Pandas não instalado")

try:
    from ibm_watsonx_ai import APIClient
    print(f"✓ IBM watsonx.ai instalado")
except:
    print("✗ IBM watsonx.ai não instalado")

try:
    from dotenv import load_dotenv
    print(f"✓ python-dotenv instalado")
except:
    print("✗ python-dotenv não instalado")

# Verificar .env
import os
load_dotenv()
if os.getenv('IBM_WATSONX_API_KEY'):
    print("✓ API Key configurada")
else:
    print("✗ API Key não configurada")

if os.getenv('IBM_WATSONX_PROJECT_ID'):
    print("✓ Project ID configurado")
else:
    print("✗ Project ID não configurado")

print("\nInstalação verificada!")
```

Execute:
```bash
python test_installation.py
```

---

## 🐛 Problemas Comuns

### Erro: "ModuleNotFoundError: No module named 'ibm_watsonx_ai'"

**Solução:**
```bash
pip install ibm-watsonx-ai
```

### Erro: "ChromeDriver not found"

**Solução:**
O `webdriver-manager` baixa automaticamente. Se falhar:
```bash
pip install --upgrade webdriver-manager
```

### Erro: "API Key inválida"

**Solução:**
1. Verifique se copiou a API Key completa
2. Verifique se não há espaços extras no `.env`
3. Gere uma nova API Key no IBM Cloud

### Erro: "Rate limit exceeded"

**Solução:**
- Aguarde alguns minutos
- O scraper tem retry automático
- Considere usar plano pago para limites maiores

### Erro: "No module named 'dotenv'"

**Solução:**
```bash
pip install python-dotenv
```

---

## 💡 Dicas

### 1. Testar com Poucos Órgãos Primeiro

Edite `orgaos.txt` e deixe apenas 1-2 órgãos para teste inicial.

### 2. Monitorar Custos

- Acesse IBM Cloud Dashboard
- Vá em "Billing and usage"
- Configure alertas de custo

### 3. Usar Cache (Futuro)

Em versões futuras, haverá cache de respostas para economizar.

### 4. Modo Headless para Servidores

Use `--headless` quando executar em servidores sem interface gráfica.

### 5. Logs Detalhados

Use `--debug` para ver logs detalhados durante desenvolvimento.

---

## 🔄 Atualização

Para atualizar o scraper:

```bash
# Atualizar dependências
pip install --upgrade -r requirements.txt

# Baixar nova versão do código
# (substituir arquivos)
```

---

## 📞 Suporte

Em caso de problemas:

1. Verifique este guia
2. Consulte o `README_V5.md`
3. Execute `test_installation.py`
4. Verifique os logs no Excel (aba "Log")

---

## ✅ Checklist de Instalação

- [ ] Python 3.8+ instalado
- [ ] Chrome instalado
- [ ] Ambiente virtual criado
- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] Conta IBM Cloud criada
- [ ] watsonx.ai ativado
- [ ] API Key obtida
- [ ] Project ID obtido
- [ ] Arquivo `.env` configurado
- [ ] Arquivo `orgaos.txt` configurado
- [ ] Teste de instalação executado
- [ ] Primeiro teste realizado

---

**Documento criado por:** Bob (Advanced Mode)  
**Data:** 2026-05-21  
**Versão:** 1.0