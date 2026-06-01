# 🔴 ERRO CRÍTICO: Python 3.9 Incompatível

## ❌ O Problema

Você está usando **Python 3.9**, mas o pacote `ibm-watsonx-ai` requer **Python 3.10 ou superior**.

**Erro encontrado:**
```
SyntaxError: invalid syntax
match run_details['entity']['results_reference']['type']:
```

A sintaxe `match/case` foi introduzida apenas no Python 3.10.

---

## ✅ SOLUÇÕES

### 🎯 SOLUÇÃO 1: Atualizar Python (RECOMENDADO)

#### macOS (seu sistema):

**Opção A: Usando Homebrew**
```bash
# Instalar Homebrew (se não tiver)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instalar Python 3.11
brew install python@3.11

# Verificar instalação
python3.11 --version
```

**Opção B: Download direto**
1. Acesse: https://www.python.org/downloads/
2. Baixe Python 3.11 ou 3.12
3. Instale o pacote .pkg
4. Verifique: `python3.11 --version`

#### Recriar ambiente virtual com Python 3.11:

```bash
cd "/Users/guilhermefreitas/Desktop/Scraper Órgãos GOV"

# Remover ambiente virtual antigo
rm -rf .venv

# Criar novo com Python 3.11
python3.11 -m venv .venv

# Ativar
source .venv/bin/activate

# Instalar dependências
cd v5/
pip install -r requirements.txt
```

---

### 🎯 SOLUÇÃO 2: Usar Versão Antiga do Pacote (TEMPORÁRIO)

Se não puder atualizar o Python agora, use uma versão mais antiga do pacote:

```bash
# Ativar ambiente virtual
source .venv/bin/activate

# Instalar versão compatível com Python 3.9
pip install ibm-watson-machine-learning==1.0.335

# Instalar outras dependências
cd v5/
pip install selenium beautifulsoup4 pandas openpyxl python-dotenv webdriver-manager
```

**⚠️ ATENÇÃO:** Esta versão antiga pode não ter todos os recursos do watsonx.ai mais recente.

---

### 🎯 SOLUÇÃO 3: Usar pyenv (MELHOR PARA MÚLTIPLAS VERSÕES)

Se você trabalha com vários projetos Python:

```bash
# Instalar pyenv
brew install pyenv

# Adicionar ao shell (bash/zsh)
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc

# Recarregar shell
source ~/.zshrc

# Instalar Python 3.11
pyenv install 3.11.7

# Usar no projeto
cd "/Users/guilhermefreitas/Desktop/Scraper Órgãos GOV"
pyenv local 3.11.7

# Recriar ambiente virtual
rm -rf .venv
python -m venv .venv
source .venv/bin/activate

# Instalar dependências
cd v5/
pip install -r requirements.txt
```

---

## 🔍 VERIFICAR VERSÃO DO PYTHON

```bash
# Verificar versão atual
python --version
python3 --version
python3.9 --version
python3.11 --version

# Verificar qual Python o venv está usando
source .venv/bin/activate
python --version
```

---

## 📋 PASSO A PASSO COMPLETO (RECOMENDADO)

### 1. Instalar Python 3.11

```bash
# Via Homebrew
brew install python@3.11

# Verificar
python3.11 --version
# Deve mostrar: Python 3.11.x
```

### 2. Remover ambiente virtual antigo

```bash
cd "/Users/guilhermefreitas/Desktop/Scraper Órgãos GOV"
rm -rf .venv
```

### 3. Criar novo ambiente com Python 3.11

```bash
python3.11 -m venv .venv
```

### 4. Ativar ambiente

```bash
source .venv/bin/activate
```

### 5. Atualizar pip

```bash
pip install --upgrade pip
```

### 6. Instalar dependências

```bash
cd v5/
pip install -r requirements.txt
```

### 7. Verificar instalação

```bash
python test_watsonx.py
```

---

## 🎯 ALTERNATIVA: Usar Docker

Se não quiser instalar Python 3.11 no sistema:

```bash
# Criar Dockerfile
cat > Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

# Instalar Chrome
RUN apt-get update && apt-get install -y \
    wget \
    gnup \
    unzip \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Copiar arquivos
COPY v5/ /app/

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "scraper_v5_ai.py", "--headless"]
EOF

# Construir imagem
docker build -t scraper-v5 .

# Executar
docker run -v $(pwd)/v5:/app scraper-v5
```

---

## ❓ POR QUE ESTE ERRO?

O pacote `ibm-watsonx-ai` usa recursos modernos do Python:

1. **`match/case`** (Python 3.10+) - Pattern matching
2. **Type hints avançados** (Python 3.10+)
3. **Outras features modernas**

Python 3.9 não suporta essas funcionalidades.

---

## 📊 COMPARAÇÃO DE VERSÕES

| Python | ibm-watsonx-ai | Status |
|--------|----------------|--------|
| 3.9 | ❌ Incompatível | Erro de sintaxe |
| 3.10 | ✅ Compatível | Funciona |
| 3.11 | ✅ Recomendado | Melhor performance |
| 3.12 | ✅ Compatível | Mais recente |

---

## 🚀 APÓS CORRIGIR

1. **Verificar Python:**
   ```bash
   python --version
   # Deve mostrar 3.10+ 
   ```

2. **Testar instalação:**
   ```bash
   python test_watsonx.py
   ```

3. **Executar scraper:**
   ```bash
   python scraper_v5_ai.py
   ```

---

**Criado por:** Bob  
**Data:** 2026-05-21  
**Versão:** 1.0