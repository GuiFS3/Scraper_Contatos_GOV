# 🔍 Diagnóstico de Erros - IBM watsonx.ai

## ❌ Erros Reportados

```
⚠️ ibm-watsonx-ai não instalado. Usando modo fallback.
⚠️ IBM watsonx.ai não disponível
```

## 🔎 Problemas Identificados e Soluções

### 1️⃣ **Versão do Python Incompatível**

**Problema:**
- O pacote `ibm-watsonx-ai` requer **Python 3.10 ou superior**
- Usa sintaxe `match/case` (pattern matching) introduzida no Python 3.10
- Se você tem Python 3.9 ou inferior, o pacote não funciona

**Como Verificar:**
```bash
python --version
# ou
python3 --version
```

**Solução:**
```bash
# macOS com Homebrew
brew install python@3.11
python3.11 -m venv venv
source venv/bin/activate

# Reinstalar dependências
pip install -r requirements.txt
```

**Documentação:** Veja `ERRO_PYTHON_39.md` para guia completo

---

### 2️⃣ **Modelo Incompatível ou Indisponível**

**Problema:**
- Modelos testados que **NÃO funcionaram**:
  - ❌ `granite-13b-chat-v2` - Não disponível no plano
  - ❌ `granite-8b-code-instruct` - Deprecated
  - ❌ `granite-3-1-8b-instruct` - Não disponível
  - ❌ `granite-3-1-8b-base` - Não suporta geração de texto

**Solução:**
- ✅ Usar `ibm/granite-4-h-small` (modelo que funciona)

**Código Correto:**
```python
self.model = ModelInference(
    model_id="ibm/granite-4-h-small",  # ← Modelo correto
    api_client=self.client,
    project_id=self.project_id,
    params={
        "max_new_tokens": 1000,
        "min_new_tokens": 50,
        "temperature": 0.3,
        "top_p": 0.95,
        "repetition_penalty": 1.2
    }
)
```

**Documentação:** Veja `MODELOS_DISPONIVEIS.md` para lista completa

---

### 3️⃣ **Arquivo .env Ausente ou Incorreto**

**Problema:**
- Arquivo `.env` não existe
- Variáveis de ambiente não configuradas
- API Key ou Project ID inválidos

**Como Verificar:**
```bash
# Verificar se .env existe
ls -la v5/.env

# Verificar conteúdo
cat v5/.env
```

**Solução:**
```bash
# Criar .env a partir do template
cp v5/.env.example v5/.env

# Editar com suas credenciais
nano v5/.env
```

**Conteúdo do .env:**
```env
IBM_WATSONX_API_KEY=sua_api_key_aqui
IBM_WATSONX_PROJECT_ID=seu_project_id_aqui
IBM_WATSONX_URL=https://us-south.ml.cloud.ibm.com
```

**Onde Encontrar:**
- API Key: https://cloud.ibm.com/iam/apikeys
- Project ID: https://dataplatform.cloud.ibm.com/projects/ (clique no projeto → Settings → General)

---

### 4️⃣ **Pacote Não Instalado Corretamente**

**Problema:**
- `ibm-watsonx-ai` não foi instalado
- Versão incompatível instalada
- Conflito de dependências

**Como Verificar:**
```bash
pip list | grep ibm-watsonx-ai
```

**Solução:**
```bash
# Desinstalar versão antiga
pip uninstall ibm-watsonx-ai -y

# Reinstalar versão correta
pip install ibm-watsonx-ai==1.1.20

# Ou instalar todas as dependências
pip install -r requirements.txt
```

---

### 5️⃣ **Credenciais Inválidas**

**Problema:**
- API Key expirada ou inválida
- Project ID incorreto
- Serviço watsonx.ai não associado ao projeto

**Como Verificar:**
```bash
# Executar script de diagnóstico
python v5/test_watsonx.py
```

**Solução:**
1. **Verificar API Key:**
   - Acesse: https://cloud.ibm.com/iam/apikeys
   - Crie nova API Key se necessário
   - Copie e cole no `.env`

2. **Verificar Project ID:**
   - Acesse: https://dataplatform.cloud.ibm.com/projects/
   - Clique no projeto
   - Settings → General → copie o Project ID
   - Cole no `.env`

3. **Associar watsonx.ai Runtime:**
   - No projeto, vá em "Manage" → "Services & integrations"
   - Clique em "Associate service"
   - Selecione "Watson Machine Learning"
   - Escolha sua instância do watsonx.ai
   - Clique em "Associate"

---

## 🛠️ Script de Diagnóstico Automático

Execute este comando para identificar o problema:

```bash
python v5/test_watsonx.py
```

**O que ele verifica:**
- ✅ Versão do Python
- ✅ Pacote `ibm-watsonx-ai` instalado
- ✅ Arquivo `.env` existe
- ✅ Variáveis de ambiente configuradas
- ✅ Conexão com watsonx.ai
- ✅ Modelo disponível e funcional

---

## 📋 Checklist de Correção

Use este checklist para garantir que tudo está configurado:

- [ ] **Python 3.10+** instalado (`python --version`)
- [ ] **Virtual environment** ativado (`source venv/bin/activate`)
- [ ] **Dependências** instaladas (`pip install -r requirements.txt`)
- [ ] **Arquivo .env** criado e configurado
- [ ] **API Key** válida no `.env`
- [ ] **Project ID** correto no `.env`
- [ ] **watsonx.ai Runtime** associado ao projeto
- [ ] **Modelo correto** no código (`ibm/granite-4-h-small`)
- [ ] **Script de diagnóstico** executado com sucesso

---

## 🚀 Solução Rápida (Passo a Passo)

Se você quer corrigir tudo de uma vez:

```bash
# 1. Verificar Python
python --version  # Deve ser 3.10+

# 2. Criar/ativar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# 3. Instalar dependências
pip install -r v5/requirements.txt

# 4. Configurar .env
cp v5/.env.example v5/.env
nano v5/.env  # Adicionar suas credenciais

# 5. Testar configuração
python v5/test_watsonx.py

# 6. Executar scraper
python v5/scraper_v5_ai.py
```

---

## 📚 Documentação Adicional

- **Erro Python 3.9:** `ERRO_PYTHON_39.md`
- **Modelos Disponíveis:** `MODELOS_DISPONIVEIS.md`
- **Guia Completo:** `CORRIGIR_WATSONX.md`
- **Solução Rápida:** `SOLUCAO_RAPIDA.md`
- **Script Automático:** `COMANDOS_CORRECAO.sh`

---

## 💡 Dicas Importantes

1. **Sempre use Python 3.10+** - Versões antigas não funcionam
2. **Use ambiente virtual** - Evita conflitos de dependências
3. **Verifique o modelo** - Use `ibm/granite-4-h-small`
4. **Associe o serviço** - watsonx.ai Runtime deve estar no projeto
5. **Execute o diagnóstico** - `test_watsonx.py` identifica problemas

---

## 🆘 Ainda Não Funciona?

Se após seguir todos os passos ainda não funcionar:

1. Execute o diagnóstico: `python v5/test_watsonx.py`
2. Copie a saída completa do erro
3. Verifique os logs detalhados
4. Confirme que todas as etapas do checklist foram concluídas

---

**Última atualização:** 2026-05-21