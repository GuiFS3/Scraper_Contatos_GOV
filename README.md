# 🏛️ Scraper de Contatos - Órgãos Governamentais

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Selenium](https://img.shields.io/badge/Selenium-4.0+-green.svg)](https://www.selenium.dev/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Sistema automatizado para extração de contatos (nomes, cargos, emails e telefones) de sites de órgãos governamentais, com foco em profissionais da área de TI.

## 📋 Índice

- [Características](#-características)
- [Versões Disponíveis](#-versões-disponíveis)
- [Instalação](#-instalação)
- [Configuração](#-configuração)
- [Uso](#-uso)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Resultados](#-resultados)
- [Troubleshooting](#-troubleshooting)
- [Contribuindo](#-contribuindo)
- [Licença](#-licença)

## ✨ Características

- 🎯 **Extração Inteligente**: Identifica automaticamente páginas relevantes (organogramas, equipes, estrutura)
- 🔍 **Validação de Dados**: Filtra e valida nomes, cargos, emails e telefones
- 📊 **Sistema de Pontuação**: Prioriza links mais relevantes para otimizar busca
- 🚀 **Processamento Paralelo**: Versão V3 processa múltiplos órgãos simultaneamente
- 📁 **Configuração Simples**: Arquivo `orgaos.txt` para gerenciar lista de órgãos
- 📈 **Relatórios Detalhados**: Exporta dados em Excel com log de processamento
- 🛡️ **Robusto**: Tratamento de erros e recuperação automática

## 🔧 Versões Disponíveis

### V2 - Refatorado (Sequencial)
- **Arquivo**: `scraper_v2_refatorado.py`
- **Tempo**: ~40-60 minutos para 21 órgãos
- **Uso**: Processamento sequencial, mais estável
- **Recomendado para**: Primeira execução, testes, máquinas com poucos recursos

### V3 - Paralelo (Recomendado) ⚡
- **Arquivo**: `scraper_v3_paralelo.py`
- **Tempo**: ~10-15 minutos para 21 órgãos (4x mais rápido)
- **Uso**: Processamento paralelo com 4 workers simultâneos
- **Recomendado para**: Produção, grandes volumes (100+ órgãos)

## 📦 Instalação

### 1. Pré-requisitos

- Python 3.8 ou superior
- Google Chrome instalado
- pip (gerenciador de pacotes Python)

### 2. Clonar Repositório

```bash
git clone https://github.com/seu-usuario/scraper-orgaos-gov.git
cd scraper-orgaos-gov
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

**Conteúdo do `requirements.txt`:**
```
selenium>=4.0.0
webdriver-manager>=3.8.0
beautifulsoup4>=4.11.0
pandas>=1.5.0
openpyxl>=3.0.0
```

## ⚙️ Configuração

### Arquivo `orgaos.txt`

Configure os órgãos a serem processados no arquivo `orgaos.txt`:

```
SIGLA|Nome Completo do Órgão|URL do Site
```

**Exemplo:**
```
CGE|Controladoria-Geral do Estado|https://www.cge.sc.gov.br/
SEF|Secretaria de Estado da Fazenda|https://www.sef.sc.gov.br/
SCTI|Secretaria de Ciência, Tecnologia e Inovação|https://www.scti.sc.gov.br/
```

**Dicas:**
- Uma linha por órgão
- Use `#` no início da linha para comentar/desabilitar um órgão
- Mantenha o formato `SIGLA|Nome|URL` (separado por pipe `|`)
- URLs devem incluir `https://`

**Exemplo com comentários:**
```
# Órgãos prioritários
SEF|Secretaria de Estado da Fazenda|https://www.sef.sc.gov.br/
SCTI|Secretaria de Ciência, Tecnologia e Inovação|https://www.scti.sc.gov.br/

# Temporariamente desabilitado
#SES|Secretaria de Estado da Saúde|https://www.saude.sc.gov.br/
```

## 🚀 Uso

### Versão V3 (Sequencial)

```bash
python3 scraper_v2_refatorado.py
```

**Características:**
- Processa um órgão por vez
- Mais estável e previsível
- Ideal para testes iniciais

### Versão V3 (Paralelo) - Recomendado

```bash
python3 scraper_v3_paralelo.py
```

**Características:**
- Processa 4 órgãos simultaneamente (padrão)
- 4x mais rápido que V2
- Ideal para grandes volumes

**Ajustar número de workers:**

Edite o arquivo `scraper_v3_paralelo.py` na linha 551:

```python
# 4 workers (padrão) - ~10-15min para 21 órgãos
scraper = ScraperV3Paralelo(max_workers=4, headless=True)

# 6 workers (mais rápido) - ~8-12min para 21 órgãos
scraper = ScraperV3Paralelo(max_workers=6, headless=True)

# 2 workers (mais conservador) - ~20-25min para 21 órgãos
scraper = ScraperV3Paralelo(max_workers=2, headless=True)
```

**Modo com interface gráfica (debug):**

```python
scraper = ScraperV3Paralelo(max_workers=4, headless=False)
```

## 📁 Estrutura do Projeto

```
scraper-orgaos-gov/
├── README.md                      # Este arquivo
├── requirements.txt               # Dependências Python
├── orgaos.txt                     # Lista de órgãos (configuração)
├── scraper_v2_refatorado.py      # Versão sequencial
├── scraper_v3_paralelo.py        # Versão paralela (recomendado)
└── contatos_v3_paralelo_*.xlsx   # Arquivos de saída (gerados)
```

## 📊 Resultados

### Arquivo Excel Gerado

O scraper gera um arquivo Excel com timestamp:
```
contatos_v3_paralelo_20260519_183045.xlsx
```

**Estrutura:**

#### Aba 1: "Contatos TI"
| Órgão Nome | Órgão Sigla | Nome da Pessoa | Cargo / Setor | E-mail | Telefone |
|------------|-------------|----------------|---------------|--------|----------|
| Secretaria da Fazenda | SEF | João Silva | Diretor de TI | joao@sef.sc.gov.br | (48) 3665-1234 |

#### Aba 2: "Log"
| Órgão Sigla | Status | Detalhes | Timestamp |
|-------------|--------|----------|-----------|
| SEF | SUCESSO | 5 contatos extraídos | 2026-05-19 18:30:45 |

### Estatísticas no Console

```
💾 Arquivo: contatos_v3_paralelo_20260519_183045.xlsx
📊 Registros: 87
👤 Com nome: 65
📧 Com email: 78
📞 Com telefone: 52
```

## 🔧 Troubleshooting

### Problema: "Arquivo orgaos.txt não encontrado"

**Solução:**
```bash
# Certifique-se de estar no diretório correto
cd /caminho/para/scraper-orgaos-gov

# Verifique se o arquivo existe
ls -la orgaos.txt

# Crie o arquivo se necessário
touch orgaos.txt
```

### Problema: "ChromeDriver não encontrado"

**Solução:**
O `webdriver-manager` baixa automaticamente o ChromeDriver. Se houver erro:

```bash
# Reinstalar webdriver-manager
pip install --upgrade webdriver-manager

# Limpar cache
rm -rf ~/.wdm
```

### Problema: Poucos contatos extraídos

**Possíveis causas:**
1. Site não possui estrutura clara de contatos
2. Informações em formato não estruturado (imagens, PDFs)
3. Conteúdo protegido por JavaScript dinâmico

**Soluções:**
- Verifique manualmente o site do órgão
- Ajuste palavras-chave de busca no código (linha 382)
- Use modo `headless=False` para debug visual

### Problema: Scraper muito lento

**Soluções:**
1. Use a versão V3 (paralela)
2. Aumente `max_workers` (cuidado com recursos da máquina)
3. Reduza delays no código (linhas 291, 331)

### Problema: Bloqueio por anti-bot

**Sintomas:**
- Muitos erros 403/429
- Páginas em branco
- CAPTCHAs

**Soluções:**
1. Reduza `max_workers` (menos requisições simultâneas)
2. Aumente delays entre requisições
3. Use VPN ou proxy
4. Execute em horários de menor tráfego

## 🎯 Boas Práticas

### Performance

- **Pequenos volumes (< 30 órgãos)**: Use V2 ou V3 com 2-4 workers
- **Médios volumes (30-100 órgãos)**: Use V3 com 4-6 workers
- **Grandes volumes (> 100 órgãos)**: Use V3 com 6-8 workers + delays reduzidos

### Ética e Legalidade

- ✅ Respeite `robots.txt` dos sites
- ✅ Use delays adequados entre requisições
- ✅ Não sobrecarregue servidores públicos
- ✅ Use dados apenas para fins legítimos
- ❌ Não faça scraping agressivo (muitas requisições/segundo)
- ❌ Não ignore bloqueios ou CAPTCHAs

### Manutenção

- Atualize `orgaos.txt` regularmente
- Verifique mudanças nos sites (estrutura HTML)
- Mantenha dependências atualizadas: `pip install --upgrade -r requirements.txt`

## 📝 Changelog

### v3.0.0 (2026-05-19)
- ✨ Implementação de processamento paralelo
- ⚡ Redução de tempo: 40-60min → 10-15min
- 🔧 Configuração via `orgaos.txt`
- 📊 Melhorias no sistema de log

### v2.0.0 (2026-05-18)
- 🎯 Refatoração completa da lógica de extração
- ✅ Validação robusta de dados (nomes, cargos, emails)
- 🔍 Sistema de pontuação de links
- 📈 Extração estruturada de dados

### v1.0.0 (2026-05-17)
- 🚀 Versão inicial
- 🔧 Scraping básico com Selenium

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👨‍💻 Autor

**Desenvolvido com IBM Bob

- GitHub: (https://github.com/GuiFS3)

---

**⚠️ Aviso Legal**: Este projeto é apenas para fins educacionais e de pesquisa. Use de forma responsável e ética. O autor não se responsabiliza pelo uso indevido desta ferramenta.

**🔒 Privacidade**: Todos os dados extraídos são públicos e disponibilizados pelos próprios órgãos governamentais em seus sites oficiais.
