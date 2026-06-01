# 🤖 Modelos IBM watsonx.ai Disponíveis

## ❌ Erro: Modelo não suportado

Se você recebeu este erro:
```
Model 'ibm/granite-13b-chat-v2' is not supported for this environment
```

Significa que o modelo especificado não está disponível no seu plano ou região.

---

## ✅ SOLUÇÃO APLICADA

O código foi atualizado para usar: **`ibm/granite-8b-code-instruct`**

Este modelo:
- ✅ Está disponível em todos os planos (incluindo Lite/Free)
- ✅ Funciona em todas as regiões
- ✅ Otimizado para extração de informações
- ✅ Boa performance para o caso de uso

---

## 📋 MODELOS DISPONÍVEIS POR PLANO

### 🆓 Plano Lite/Free

Modelos disponíveis:
- `ibm/granite-8b-code-instruct` ← **RECOMENDADO**
- `ibm/granite-3-1-8b-base`
- `cross-encoder/ms-marco-minilm-l-12-v2`

### 💰 Plano Pago (Essentials/Standard)

Modelos adicionais:
- `ibm/granite-13b-chat-v2`
- `ibm/granite-13b-instruct-v2`
- `ibm/granite-20b-multilingual`
- `meta-llama/llama-3-70b-instruct`
- E outros modelos premium

---

## 🔧 COMO MUDAR O MODELO

Se quiser testar outro modelo, edite o arquivo `scraper_v5_ai.py`:

```python
# Linha ~131
self.model = ModelInference(
    model_id="ibm/granite-8b-code-instruct",  # ← Mude aqui
    api_client=self.client,
    project_id=self.project_id,
    params={
        "decoding_method": "greedy",
        "max_new_tokens": 2000,
        "temperature": 0.1,
        "top_p": 0.9,
        "repetition_penalty": 1.1
    }
)
```

---

## 🎯 MODELOS RECOMENDADOS POR CASO DE USO

### Para Extração de Dados (nosso caso):
1. **`ibm/granite-8b-code-instruct`** ← Melhor custo-benefício
2. `ibm/granite-13b-instruct-v2` (se disponível)
3. `ibm/granite-3-1-8b-base`

### Para Chat/Conversação:
1. `ibm/granite-13b-chat-v2` (se disponível)
2. `meta-llama/llama-3-70b-instruct` (plano pago)

### Para Análise de Código:
1. `ibm/granite-8b-code-instruct` ← Já configurado
2. `ibm/granite-20b-code` (plano pago)

---

## 🔍 VERIFICAR MODELOS DISPONÍVEIS

Execute este script Python para listar modelos disponíveis:

```python
from ibm_watsonx_ai import APIClient, Credentials
from dotenv import load_dotenv
import os

load_dotenv()

credentials = Credentials(
    url=os.getenv('IBM_WATSONX_URL', 'https://us-south.ml.cloud.ibm.com'),
    api_key=os.getenv('IBM_WATSONX_API_KEY')
)

client = APIClient(credentials)

# Listar modelos disponíveis
models = client.foundation_models.get_model_specs()

print("Modelos disponíveis:")
for model in models['resources']:
    print(f"  - {model['model_id']}")
```

---

## 📊 COMPARAÇÃO DE MODELOS

| Modelo | Tamanho | Velocidade | Qualidade | Plano |
|--------|---------|------------|-----------|-------|
| granite-8b-code-instruct | 8B | ⚡⚡⚡ Rápido | ⭐⭐⭐ Boa | Free |
| granite-3-1-8b-base | 8B | ⚡⚡⚡ Rápido | ⭐⭐ OK | Free |
| granite-13b-chat-v2 | 13B | ⚡⚡ Médio | ⭐⭐⭐⭐ Ótima | Pago |
| granite-13b-instruct-v2 | 13B | ⚡⚡ Médio | ⭐⭐⭐⭐ Ótima | Pago |
| llama-3-70b-instruct | 70B | ⚡ Lento | ⭐⭐⭐⭐⭐ Excelente | Pago |

---

## 💡 DICAS

### 1. Começar com modelo gratuito
Use `granite-8b-code-instruct` para testar. Se precisar de melhor qualidade, faça upgrade.

### 2. Monitorar custos
Modelos maiores custam mais por token. Comece pequeno.

### 3. Testar diferentes modelos
Cada modelo tem pontos fortes. Teste para seu caso específico.

### 4. Ajustar parâmetros
Além do modelo, ajuste:
- `temperature` (0.0-1.0) - Criatividade
- `max_new_tokens` - Tamanho da resposta
- `top_p` - Diversidade

---

## 🚀 PRÓXIMOS PASSOS

1. **Teste o scraper agora:**
   ```bash
   python scraper_v5_ai.py
   ```

2. **Se funcionar bem:** Continue usando `granite-8b-code-instruct`

3. **Se precisar melhor qualidade:**
   - Faça upgrade para plano pago
   - Mude para `granite-13b-instruct-v2`

---

## ❓ FAQ

**P: Por que o modelo mudou?**  
R: O modelo anterior não estava disponível no seu plano/região.

**P: O novo modelo é bom?**  
R: Sim! `granite-8b-code-instruct` é otimizado para extração de dados.

**P: Posso usar modelos maiores?**  
R: Sim, se tiver plano pago. Veja lista acima.

**P: Como saber quais modelos tenho acesso?**  
R: Execute o script de verificação acima ou consulte o IBM Cloud.

---

**Criado por:** Bob  
**Data:** 2026-05-21  
**Versão:** 1.0