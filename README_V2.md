# 🤖 Web Scraper de Contatos de TI - Governo SC

Script automatizado para extrair informações de contato do setor de TI dos órgãos governamentais de Santa Catarina.

## 📋 Pré-requisitos

```bash
pip3 install selenium webdriver-manager beautifulsoup4 pandas openpyxl
```

## 🚀 Como Usar

### 1. Adicionar/Editar Órgãos

Edite o arquivo **`orgaos.txt`** com os órgãos que deseja processar:

```
SIGLA|Nome Completo do Órgão|URL do Site
```

**Exemplo:**
```
CGE|Controladoria-Geral do Estado|https://www.cge.sc.gov.br/
SCTI|Secretaria de Estado da Ciência, Tecnologia e Inovação|https://www.scti.sc.gov.br/
SEF|Secretaria de Estado da Fazenda|https://www.sef.sc.gov.br/
```

**Dicas:**
- Uma linha por órgão
- Use `|` (pipe) para separar os campos
- Linhas começando com `#` são ignoradas (comentários)
- Linhas vazias são ignoradas

### 2. Executar o Script

```bash
python3 scraper_v2_refatorado.py
```

### 3. Resultado

O script irá:
- ✅ Ler órgãos de `orgaos.txt`
- ✅ Acessar o site de cada órgão
- ✅ Buscar páginas de organograma/equipe/estrutura
- ✅ Extrair nomes, cargos, emails e telefones do setor de TI
- ✅ Gerar arquivo Excel: `contatos_v2_refatorado_[timestamp].xlsx`

## 📊 Formato do Arquivo Excel

O arquivo gerado contém 2 abas:

### Aba 1: Contatos TI
| Órgão Nome | Órgão Sigla | Nome da Pessoa | Cargo / Setor | E-mail | Telefone |
|------------|-------------|----------------|---------------|--------|----------|
| Secretaria... | SCTI | André Brito | Diretor de TI | email@... | (48) 3665-... |

### Aba 2: Log
Detalhes do processamento de cada órgão (sucessos, erros, páginas visitadas)

## ⚙️ Configurações

### Modo Headless (sem abrir navegador)

Edite `scraper_v2_refatorado.py` linha 540:

```python
scraper = ScraperV2(headless=True)  # True = não abre navegador
```

### Limitar Número de Links por Órgão

Linha 408:
```python
for idx, link in enumerate(links[:5], 1):  # Processa top 5 links
```

### Tempo de Espera entre Páginas

Linha 413:
```python
time.sleep(1)  # Aguarda 1 segundo entre páginas
```

## 🔍 Como Funciona

1. **Mapeamento de Links:** Analisa o site e atribui pontuação para cada link
   - +10pts: "organograma", "quem é quem"
   - +7pts: "estrutura", "equipe"
   - +8pts: "tecnologia", "TI"
   - -10pts: "notícias", "documentos"

2. **Extração Inteligente:** 
   - Valida se texto é nome válido (2-5 palavras, começa com maiúscula)
   - Valida se texto é cargo válido (contém palavras-chave)
   - Separa corretamente cargo, nome, email e telefone
   - Filtra dados inválidos (endereços, protocolos, etc)

3. **Salvamento:** Gera Excel com dados limpos e log detalhado

## 📝 Exemplos de Uso

### Adicionar Novo Órgão

Adicione uma linha em `orgaos.txt`:
```
NOVA|Secretaria Nova|https://www.nova.sc.gov.br/
```

### Comentar Órgão (não processar)

Adicione `#` no início da linha:
```
#CGE|Controladoria-Geral do Estado|https://www.cge.sc.gov.br/
```

### Processar Apenas Alguns Órgãos

Comente os que não quer processar:
```
SCTI|Secretaria de Estado da Ciência, Tecnologia e Inovação|https://www.scti.sc.gov.br/
SEF|Secretaria de Estado da Fazenda|https://www.sef.sc.gov.br/
#SES|Secretaria de Estado da Saúde|https://www.saude.sc.gov.br/
```

## ⚠️ Observações

- O script respeita delays entre requisições (1-2 segundos)
- Navegador Chrome é necessário
- ChromeDriver é baixado automaticamente
- Tempo estimado: ~2-3 minutos por órgão
- Para 21 órgãos: ~40-60 minutos total

## 🐛 Solução de Problemas

### "Arquivo orgaos.txt não encontrado"
- Certifique-se que `orgaos.txt` está na mesma pasta do script

### "ChromeDriver não encontrado"
- Execute: `pip3 install webdriver-manager`
- O ChromeDriver será baixado automaticamente

### "Nenhum contato encontrado"
- Verifique se o site do órgão está acessível
- Alguns órgãos podem não ter página de organograma
- Veja o log no Excel para detalhes

## 📧 Contato

Script desenvolvido por Bob AI Assistant
Data: 2026-05-19