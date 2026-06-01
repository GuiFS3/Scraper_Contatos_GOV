# ⚡ Solução Rápida - Erros IBM watsonx.ai

## 🎯 Você está vendo estes erros?

```
⚠️ ibm-watsonx-ai não instalado. Usando modo fallback.
⚠️ IBM watsonx.ai não disponível
```

---

## ✅ SOLUÇÃO EM 3 PASSOS

### 📍 PASSO 1: Instalar o Pacote

```bash
cd v5/
pip install ibm-watsonx-ai
```

**OU** instale todas as dependências:

```bash
pip install -r requirements.txt
```

---

### 📍 PASSO 2: Criar Arquivo .env

```bash
# Copiar o template
cp .env.example .env
```

Edite o arquivo `.env` com suas credenciais:

```env
IBM_WATSONX_API_KEY=sua_api_key_real_aqui
IBM_WATSONX_PROJECT_ID=seu_project_id_real_aqui
IBM_WATSONX_URL=https://us-south.ml.cloud.ibm.com
```

**⚠️ IMPORTANTE:**
- Substitua `sua_api_key_real_aqui` pela sua API Key REAL
- Substitua `seu_project_id_real_aqui` pelo seu Project ID REAL
- NÃO deixe os valores padrão!

---

### 📍 PASSO 3: Obter Credenciais

#### 🔑 API Key

1. Acesse: https://cloud.ibm.com/
2. Login → Perfil (canto superior direito) → **API keys**
3. Clique em **"Create an IBM Cloud API key"**
4. Dê um nome (ex: "watsonx-scraper")
5. **COPIE A CHAVE** (você não poderá vê-la novamente!)

**Formato esperado:**
```
aBcDeFgHiJkLmNoPqRsTuVwXyZ1234567890-_AbCdEf
```
(~40-50 caracteres)

#### 🆔 Project ID

1. Acesse: https://dataplatform.cloud.ibm.com/
2. Clique em **"Projects"** no menu lateral
3. Selecione seu projeto (ou crie um novo)
4. **Manage** → **General**
5. Copie o **Project ID**

**Formato esperado:**
```
12345678-abcd-1234-abcd-123456789abc
```
(36 caracteres, formato UUID)

---

## 🔍 VERIFICAR SE FUNCIONOU

Execute o diagnóstico:

```bash
python test_watsonx.py
```

**Resultado esperado:**
```
✅ Python 3.x.x
✅ ibm-watsonx-ai
✅ Arquivo .env encontrado
✅ IBM_WATSONX_API_KEY: Configurada
✅ IBM_WATSONX_PROJECT_ID: Configurado
✅ Conexão estabelecida com sucesso!
```

---

## 🚀 TESTAR O SCRAPER

```bash
python scraper_v5_ai.py
```

**Saída esperada:**
```
✓ IBM watsonx.ai inicializado
✓ Scraper V5 AI-Powered inicializado
🚀 SCRAPER V5 - AI-POWERED
...
🤖 Consultando IBM watsonx.ai...
✅ X contatos extraídos (IA)
```

---

## ❌ AINDA NÃO FUNCIONA?

### Erro: "API Key inválida"

**Solução:**
1. Gere uma NOVA API Key
2. Copie COMPLETAMENTE (sem espaços)
3. Cole no `.env`
4. Salve o arquivo

### Erro: "Project ID inválido"

**Solução:**
1. Verifique se copiou o **ID** (não o nome)
2. Deve ter 36 caracteres
3. Formato: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`

### Erro: "Forbidden" ou "403"

**Solução:**
1. Ative o watsonx.ai em: https://cloud.ibm.com/
2. Crie um plano (Lite é gratuito)
3. Associe o **watsonx.ai Runtime** ao projeto

### Erro: "ModuleNotFoundError"

**Solução:**
```bash
pip install ibm-watsonx-ai
```

---

## 📚 DOCUMENTAÇÃO COMPLETA

- **CORRIGIR_WATSONX.md** - Guia detalhado com todos os problemas
- **test_watsonx.py** - Script de diagnóstico automático
- **GUIA_INSTALACAO.md** - Guia completo de instalação
- **README_V5.md** - Documentação do scraper

---

## 💡 DICA PRO

Sempre execute o diagnóstico primeiro:

```bash
python test_watsonx.py
```

Ele identifica EXATAMENTE qual é o problema e mostra a solução específica!

---

**Criado por:** Bob  
**Versão:** 1.0  
**Data:** 2026-05-21