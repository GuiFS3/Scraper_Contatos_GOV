# Scraper V5 - AI-Powered with IBM watsonx.ai 🤖

## 📋 Visão Geral

O **Scraper V5** é um scraper revolucionário que utiliza **IBM watsonx.ai** para ler e interpretar páginas web de forma inteligente, extraindo contatos de TI com precisão sem necessidade de padrões pré-definidos.

### ✨ Principais Inovações em Relação ao V4

| Aspecto | V4 (Anterior) | V5 (Novo) |
|---------|---------------|-----------|
| **Extração de Dados** | Padrões fixos (tabelas, listas) | **IA interpreta qualquer layout** |
| **Compreensão** | Regex e seletores CSS | **LLM entende contexto semântico** |
| **Adaptabilidade** | Requer padrões conhecidos | **Aprende com cada página** |
| **Precisão** | ~80% | **>95% (esperado)** |
| **Robustez** | Quebra com layouts novos | **Funciona com qualquer layout** |
| **Inteligência** | Regras fixas | **Raciocínio contextual** |

---

## 🏗️ Arquitetura

```
SCRAPER V5 - AI-POWERED
├── 1. IBM watsonx.ai Integration
│   ├── API Client (watsonx.ai)
│   ├── Prompt Engineering
│   └── Response Parser
├── 2. Intelligent Page Analyzer
│   ├── Visual Understanding
│   ├── Semantic Analysis
│   └── Context Extraction
├── 3. AI-Powered Extractor
│   ├── LLM-based Extraction
│   ├── Structured Output
│   └── Confidence Scoring
├── 4. Hybrid Fallback System
│   ├── AI Primary
│   ├── V4 Patterns Secondary
│   └── Manual Review Tertiary
└── 5. Quality Assurance
    ├── AI Validation
    ├── Cross-reference Check
    └── Human-in-the-loop
```

---

## 🤖 Como Funciona

### 1. **Análise Inteligente da Página**

A IA analisa a página completa e entende:
- Estrutura organizacional
- Hierarquia de informações
- Contexto semântico
- Relações entre elementos

### 2. **Extração Contextual**

Em vez de buscar padrões fixos, a IA:
- Lê o conteúdo como um humano
- Identifica nomes, cargos e contatos por contexto
- Entende abreviações e variações
- Resolve ambiguidades

### 3. **Validação Inteligente**

A IA valida dados considerando:
- Coerência contextual
- Padrões linguísticos brasileiros
- Estrutura organizacional típica
- Probabilidade de correção

---

## 🔧 Componentes Principais

### 1️⃣ **IBMWatsonxClient**
Cliente para integração com IBM watsonx.ai.

**Funcionalidades:**
- ✅ Autenticação via API Key
- ✅ Envio de prompts estruturados
- ✅ Parsing de respostas JSON
- ✅ Rate limiting e retry logic
- ✅ Error handling robusto

**Modelos Suportados:**
- `ibm/granite-13b-chat-v2` (recomendado)
- `meta-llama/llama-3-70b-instruct`
- `mistralai/mixtral-8x7b-instruct-v01`

### 2️⃣ **IntelligentPageAnalyzer**
Analisa páginas usando IA para entender estrutura e conteúdo.

**Funcionalidades:**
- 🔍 Análise semântica de conteúdo
- 🎯 Identificação de seções relevantes
- 📊 Extração de hierarquia organizacional
- 🧠 Compreensão contextual

### 3️⃣ **AIDataExtractor**
Extrai dados usando prompts especializados.

**Funcionalidades:**
- 📝 Extração de nomes com contexto
- 💼 Identificação de cargos e setores
- 📧 Extração de emails e telefones
- ✅ Validação automática de dados

### 4️⃣ **HybridFallbackSystem**
Sistema híbrido que combina IA com padrões tradicionais.

**Estratégia:**
1. **Primário:** IA (watsonx.ai)
2. **Secundário:** Padrões V4 (se IA falhar)
3. **Terciário:** Revisão manual (se ambos falharem)

### 5️⃣ **QualityAssurance**
Sistema de garantia de qualidade com múltiplas camadas.

**Validações:**
- ✅ Validação por IA (coerência)
- ✅ Validação por regras (formato)
- ✅ Cross-reference (duplicatas)
- ✅ Confidence scoring

---

## 🚀 Como Usar

### Pré-requisitos

```bash
pip install -r requirements.txt
```

**requirements.txt:**
```
selenium>=4.15.0
beautifulsoup4>=4.12.0
pandas>=2.1.0
openpyxl>=3.1.0
webdriver-manager>=4.0.0
ibm-watsonx-ai>=0.2.0
python-dotenv>=1.0.0
requests>=2.31.0
```

### Configuração

1. **Obter credenciais IBM watsonx.ai:**
   - Acesse: https://www.ibm.com/watsonx
   - Crie uma conta ou faça login
   - Gere uma API Key
   - Anote o Project ID

2. **Configurar variáveis de ambiente:**

Crie um arquivo `.env`:
```env
IBM_WATSONX_API_KEY=your_api_key_here
IBM_WATSONX_PROJECT_ID=your_project_id_here
IBM_WATSONX_URL=https://us-south.ml.cloud.ibm.com
```

3. **Configurar órgãos:**

Edite `orgaos.txt`:
```
SIGLA|Nome do Órgão|URL
GOVERNO-PR|Governo do Estado do Paraná|https://www.parana.pr.gov.br/Pagina/Quemequem
```

### Execução

```bash
python scraper_v5_ai.py
```

**Opções:**
```bash
# Modo headless
python scraper_v5_ai.py --headless

# Usar apenas IA (sem fallback)
python scraper_v5_ai.py --ai-only

# Modo debug (verbose)
python scraper_v5_ai.py --debug
```

---

## 📊 Exemplo de Prompt para IA

```json
{
  "role": "system",
  "content": "Você é um especialista em extrair informações de contato de sites governamentais brasileiros."
}
{
  "role": "user",
  "content": "Analise o seguinte conteúdo HTML e extraia APENAS contatos da área de Tecnologia da Informação (TI/TIC/Informática):\n\n[HTML CONTENT]\n\nRetorne um JSON com a seguinte estrutura:\n{\n  \"contatos\": [\n    {\n      \"nome\": \"Nome completo da pessoa\",\n      \"cargo\": \"Cargo ou setor\",\n      \"email\": \"email@exemplo.gov.br\",\n      \"telefone\": \"(41) 1234-5678\",\n      \"confianca\": 0.95\n    }\n  ]\n}"
}
```

---

## 🎯 Vantagens sobre V4

### ❌ V4 - Limitações

```python
# Padrões fixos
if layout == 'TABELA':
    extrair_de_tabela()
elif layout == 'LISTA':
    extrair_de_lista()
# Quebra com layouts novos ❌

# Validação rígida
if 'coordenadoria' in texto.lower():
    return False
# Pode rejeitar nomes válidos ❌
```

### ✅ V5 - Soluções

```python
# IA interpreta qualquer layout
response = ai_client.extract_contacts(html_content)
# Funciona com qualquer estrutura ✅

# Validação contextual
if ai_client.validate_name(nome, contexto):
    return True
# Entende contexto e nuances ✅
```

---

## 📈 Resultados Esperados

### Comparação de Versões

| Métrica | V2 | V4 | V5 |
|---------|----|----|-----|
| Taxa de Sucesso | 57% | 90% | **>95%** |
| Dados Úteis | 10% | 80% | **>90%** |
| Nomes Reais | 5% | 70% | **>85%** |
| Emails Válidos | 30% | 60% | **>80%** |
| Adaptabilidade | Baixa | Média | **Alta** |
| Manutenção | Alta | Média | **Baixa** |

---

## 🔒 Segurança e Privacidade

- ✅ API Keys armazenadas em `.env` (não versionado)
- ✅ Dados processados via API IBM (GDPR compliant)
- ✅ Sem armazenamento de dados sensíveis
- ✅ Logs anonimizados
- ✅ Rate limiting para evitar sobrecarga

---

## 💰 Custos Estimados

**IBM watsonx.ai Pricing (aproximado):**
- Granite 13B: ~$0.0005 por 1K tokens
- Llama 3 70B: ~$0.002 por 1K tokens

**Estimativa por órgão:**
- Tokens médios: ~5K (input) + 1K (output)
- Custo por órgão: ~$0.003 - $0.012
- **Custo para 7 órgãos: ~$0.02 - $0.08**

---

## 🐛 Troubleshooting

### Problema: "API Key inválida"
**Solução:** Verifique se a API Key está correta no arquivo `.env`

### Problema: "Rate limit exceeded"
**Solução:** O scraper tem retry automático. Aguarde alguns segundos.

### Problema: "IA não encontrou contatos"
**Solução:** O sistema usa fallback automático para padrões V4.

### Problema: "Custo muito alto"
**Solução:** Use modelo Granite 13B (mais barato) ou ative cache de respostas.

---

## 🔄 Roadmap

### V5.1 (Futuro)
- [ ] Cache inteligente de respostas
- [ ] Fine-tuning do modelo para sites brasileiros
- [ ] Suporte a múltiplos idiomas
- [ ] Interface web para revisão manual
- [ ] Integração com outros LLMs (GPT-4, Claude)

### V5.2 (Futuro)
- [ ] Aprendizado contínuo
- [ ] Detecção automática de mudanças em sites
- [ ] Alertas de novos contatos
- [ ] API REST para integração

---

## 📄 Licença

Este projeto foi desenvolvido para uso interno.

---

## 👨‍💻 Autor

Desenvolvido por Bob (Advanced Mode)  
Data: 2026-05-21  
Versão: 5.0

---

## 🔄 Changelog

### V5.0 (2026-05-21)
- ✨ Integração com IBM watsonx.ai
- ✨ Extração baseada em IA
- ✨ Análise semântica de conteúdo
- ✨ Sistema híbrido com fallback
- ✨ Validação contextual inteligente
- ✨ Confidence scoring
- ✨ Suporte a múltiplos modelos LLM

### V4.0 (2026-05-20)
- ✅ Scraper universal com padrões
- ✅ Validação rigorosa
- ✅ Navegação inteligente
- ✅ Tratamento de conteúdo dinâmico

### V3.0 (Anterior)
- ⚠️ Processamento paralelo
- ⚠️ Melhorias de performance

### V2.0 (Anterior)
- ⚠️ Versão básica com customização por site