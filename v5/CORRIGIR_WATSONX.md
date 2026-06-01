# 🔧 Guia de Correção - IBM watsonx.ai

## 🎯 Objetivo
Este guia resolve os erros:
- `⚠️ ibm-watsonx-ai não instalado. Usando modo fallback.`
- `⚠️ IBM watsonx.ai não disponível`

---

## 📋 PASSO 1: Executar Diagnóstico

Primeiro, vamos identificar exatamente qual é o problema:

```bash
cd v5/
python test_watsonx.py
```

O script mostrará:
- ✅ O que está funcionando
- ❌ O que precisa ser corrigido
- 💡 Soluções específicas

---

## 🔧 PASSO 2: Corrigir Problemas Identificados

### Problema A: Pacote `ibm-watsonx-ai` não instalado

**Sintoma no diagnóstico:**
```
❌ ibm-watsonx-ai - NÃO INSTALADO
```

**Solução:**

```bash
# Opção 1: Instalar apenas o pacote watsonx
pip install ibm-watsonx-ai

# Opção 2: Instalar todas as dependências
pip install -r requirements.txt

# Verificar instalação
pip list | grep ibm-watsonx-ai
```

**Resultado esperado:**
```
ibm-watsonx-ai    0.2.0 (ou superior)
```

---

### Problema B: Arquivo `.env` não existe

**Sintoma no diagnóstico:**
```
❌ Arquivo .env NÃO ENCONTRADO
```

**Solução:**

```bash
# 1. Copiar o template
cp .env.example .env

# 2. Editar o arquivo
nano .env
# OU use seu editor preferido:
# code .env
# vim .env
```

**Conteúdo do `.env`:**
```env
# IBM watsonx.ai Credentials
IBM_WATSONX_API_KEY=sua_api_key_real_aqui
IBM_WATSONX_PROJECT_ID=seu_project_id_real_aqui
IBM_WATSONX_URL=https://us-south.ml.cloud.ibm.com
```

**⚠️ IMPORTANTE:**
- Substitua `sua_api_key_real_aqui` pela sua API Key real
- Substitua `seu_project_id_real_aqui` pelo seu Project ID real
- NÃO deixe espaços antes ou depois dos valores
- NÃO use aspas nos valores

---

### Problema C: Credenciais inválidas

**Sintoma no diagnóstico:**
```
❌ IBM_WATSONX_API_KEY: Não configurada ou usando valor padrão
❌ IBM_WATSONX_PROJECT_ID: Não configurado ou usando valor padrão
```

**Solução: Obter credenciais corretas**

#### 1. Obter API Key

1. Acesse: https://cloud.ibm.com/
2. Faça login na sua conta
3. Clique no ícone do seu perfil (canto superior direito)
4. Selecione "API keys"
5. Clique em "Create an IBM Cloud API key"
6. Dê um nome (ex: "watsonx-scraper")
7. Clique em "Create"
8. **COPIE A API KEY** (você não poderá vê-la novamente!)

**Formato esperado da API Key:**
```
aBcDeFgHiJkLmNoPqRsTuVwXyZ1234567890-_AbCdEf
```
- Tamanho: ~40-50 caracteres
- Contém letras, números, hífens e underscores

#### 2. Obter Project ID

1. Acesse: https://dataplatform.cloud.ibm.com/
2. Clique em "Projects" no menu lateral
3. Selecione seu projeto watsonx.ai (ou crie um novo)
4. Clique em "Manage" → "General"
5. Copie o **Project ID**

**Formato esperado do Project ID:**
```
12345678-abcd-1234-abcd-123456789abc
```
- Tamanho: 36 caracteres
- Formato UUID (8-4-4-4-12)

#### 3. Configurar no `.env`

Edite o arquivo `.env`:

```env
IBM_WATSONX_API_KEY=aBcDeFgHiJkLmNoPqRsTuVwXyZ1234567890-_AbCdEf
IBM_WATSONX_PROJECT_ID=12345678-abcd-1234-abcd-123456789abc
IBM_WATSONX_URL=https://us-south.ml.cloud.ibm.com
```

---

### Problema D: Erro de conexão (401 Unauthorized)

**Sintoma no diagnóstico:**
```
❌ Erro na conexão: Unauthorized
💡 Possível causa: API Key inválida
```

**Soluções:**

1. **Verificar se a API Key está correta:**
   - Sem espaços extras
   - Copiada completamente
   - Não expirada

2. **Gerar nova API Key:**
   - Siga os passos da seção "Obter API Key" acima
   - Delete a API Key antiga se necessário

3. **Verificar permissões:**
   - A API Key deve ter acesso ao watsonx.ai
   - Verifique no IBM Cloud IAM

---

### Problema E: Erro de conexão (404 Not Found)

**Sintoma no diagnóstico:**
```
❌ Erro na conexão: Not Found
💡 Possível causa: Project ID inválido ou URL incorreta
```

**Soluções:**

1. **Verificar Project ID:**
   - Copie novamente do watsonx.ai
   - Verifique se é o ID correto (não o nome)

2. **Verificar URL:**
   - Use a URL correta para sua região:
     - US South: `https://us-south.ml.cloud.ibm.com`
     - EU: `https://eu-de.ml.cloud.ibm.com`
     - UK: `https://eu-gb.ml.cloud.ibm.com`

3. **Verificar se o serviço está ativo:**
   - Acesse https://cloud.ibm.com/
   - Vá em "Resource list"
   - Verifique se watsonx.ai está ativo

---

### Problema F: Erro de conexão (403 Forbidden)

**Sintoma no diagnóstico:**
```
❌ Erro na conexão: Forbidden
💡 Possível causa: Sem permissão ou serviço não ativado
```

**Soluções:**

1. **Ativar watsonx.ai:**
   - Acesse https://cloud.ibm.com/
   - Busque por "watsonx.ai"
   - Clique em "Create" se não tiver uma instância

2. **Verificar plano:**
   - Certifique-se de ter um plano ativo (Lite ou pago)
   - Verifique se não excedeu limites do plano gratuito

3. **Associar serviço ao projeto:**
   - No watsonx.ai, vá em "Manage" → "Services"
   - Associe o watsonx.ai Runtime ao projeto

---

## ✅ PASSO 3: Verificar Correção

Após fazer as correções, execute novamente o diagnóstico:

```bash
python test_watsonx.py
```

**Resultado esperado:**
```
✅ Python 3.x.x
✅ Selenium
✅ BeautifulSoup4
✅ Pandas
✅ OpenPyXL
✅ python-dotenv
✅ ibm-watsonx-ai
✅ Arquivo .env encontrado
✅ IBM_WATSONX_API_KEY: Configurada
✅ IBM_WATSONX_PROJECT_ID: Configurado
✅ Conexão estabelecida com sucesso!
```

---

## 🚀 PASSO 4: Testar o Scraper

Com tudo configurado, teste o scraper:

```bash
# Teste básico (com interface gráfica)
python scraper_v5_ai.py

# Teste headless (sem interface)
python scraper_v5_ai.py --headless

# Teste apenas com IA (sem fallback)
python scraper_v5_ai.py --ai-only
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

## 🐛 Problemas Comuns e Soluções Rápidas

### "ModuleNotFoundError: No module named 'ibm_watsonx_ai'"

```bash
pip install ibm-watsonx-ai
```

### "FileNotFoundError: [Errno 2] No such file or directory: '.env'"

```bash
cp .env.example .env
# Depois edite o .env com suas credenciais
```

### "Credenciais IBM watsonx.ai não configuradas"

Verifique se o arquivo `.env` tem as credenciais corretas:
```bash
cat .env
```

### "API Key inválida"

1. Gere nova API Key no IBM Cloud
2. Copie completamente (sem espaços)
3. Cole no `.env`

### "Rate limit exceeded"

- Aguarde alguns minutos
- Considere upgrade para plano pago
- Use `--headless` para processar mais rápido

---

## 📞 Suporte Adicional

Se ainda tiver problemas:

1. **Execute o diagnóstico completo:**
   ```bash
   python test_watsonx.py > diagnostico.txt
   ```

2. **Verifique os logs:**
   - Arquivo Excel gerado tem aba "Log"
   - Mostra erros detalhados por órgão

3. **Consulte a documentação:**
   - `README_V5.md` - Documentação completa
   - `GUIA_INSTALACAO.md` - Guia de instalação
   - `COMPARACAO_VERSOES.md` - Diferenças entre versões

4. **Teste com versão anterior:**
   ```bash
   cd ../v4/
   python scraper_v4_universal.py
   ```

---

## ✅ Checklist Final

Antes de executar o scraper, verifique:

- [ ] Python 3.8+ instalado
- [ ] Pacote `ibm-watsonx-ai` instalado
- [ ] Arquivo `.env` criado
- [ ] API Key configurada no `.env`
- [ ] Project ID configurado no `.env`
- [ ] Diagnóstico executado com sucesso
- [ ] Conexão com watsonx.ai testada
- [ ] Arquivo `orgaos.txt` configurado

---

**Documento criado por:** Bob  
**Data:** 2026-05-21  
**Versão:** 1.0