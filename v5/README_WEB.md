# 🌐 Interface Web - Scraper V5 AI-Powered

## 📋 Visão Geral

Interface web moderna para o Scraper V5 com:
- ✅ Upload de arquivo orgaos.txt via drag & drop
- ✅ Acompanhamento em tempo real via WebSocket
- ✅ Estatísticas ao vivo
- ✅ Download do Excel gerado
- ✅ Interface responsiva e moderna

---

## 🚀 Instalação

### 1. Instalar Dependências

```bash
cd v5/
pip install -r requirements.txt
```

**Novas dependências para web:**
- `flask` - Framework web
- `flask-socketio` - WebSocket para tempo real
- `python-socketio` - Cliente Socket.IO

### 2. Configurar Credenciais

Certifique-se de que o arquivo `.env` está configurado:

```bash
cp .env.example .env
# Edite .env com suas credenciais IBM watsonx.ai
```

---

## ▶️ Executar Interface Web

```bash
cd v5/
python app.py
```

**Saída esperada:**
```
======================================================================
🌐 SCRAPER V5 - WEB INTERFACE
======================================================================

Acesse: http://localhost:5000

Pressione Ctrl+C para parar
======================================================================
```

---

## 🖥️ Como Usar

### Passo 1: Acessar Interface

Abra o navegador em: **http://localhost:5000**

### Passo 2: Upload do Arquivo

1. Clique na área de upload OU
2. Arraste o arquivo `orgaos.txt` para a área

**Formato do arquivo:**
```
SIGLA|Nome do Órgão|URL
GOVERNO-PR|Governo do Estado do Paraná|https://www.parana.pr.gov.br/Pagina/Quemequem
TCE-PR|Tribunal de Contas do Estado do Paraná|https://www.tce.pr.gov.br/
```

### Passo 3: Iniciar Scraper

1. Após upload, clique em **"🚀 Iniciar Scraper"**
2. Acompanhe o progresso em tempo real

### Passo 4: Download do Excel

1. Aguarde conclusão (100%)
2. Clique em **"📥 Download Excel"**
3. Arquivo será baixado automaticamente

---

## 📊 Funcionalidades

### 1. Upload Inteligente
- ✅ Drag & drop
- ✅ Validação automática
- ✅ Contagem de órgãos
- ✅ Feedback visual

### 2. Acompanhamento em Tempo Real
- ✅ Barra de progresso
- ✅ Log detalhado
- ✅ Estatísticas ao vivo:
  - Total de órgãos
  - Órgãos processados
  - Contatos via IA

### 3. Interface Moderna
- ✅ Design responsivo
- ✅ Animações suaves
- ✅ Cores gradientes
- ✅ Ícones intuitivos

### 4. WebSocket
- ✅ Atualizações instantâneas
- ✅ Sem necessidade de refresh
- ✅ Conexão persistente

---

## 🔧 Arquitetura

### Backend (Flask)

```
app.py
├── Upload endpoint (/upload)
├── Start endpoint (/start/<id>)
├── Status endpoint (/status/<id>)
├── Download endpoint (/download/<id>)
└── WebSocket events
    ├── status_update
    └── orgao_update
```

### Frontend (HTML/JS)

```
templates/index.html
├── Upload area (drag & drop)
├── Progress tracking
├── Real-time logs
├── Statistics cards
└── Download button
```

### Scraper Integration

```python
class ScraperV5AIWeb(ScraperV5AI):
    """Versão web que emite eventos"""
    
    def processar_orgao(self, orgao):
        # Emite evento via WebSocket
        socketio.emit('orgao_update', {...})
        
        # Processa normalmente
        super().processar_orgao(orgao)
```

---

## 📁 Estrutura de Arquivos

```
v5/
├── app.py                  # Aplicação Flask
├── scraper_v5_ai.py       # Scraper (backend)
├── templates/
│   └── index.html         # Interface web
├── uploads/               # Arquivos enviados (criado automaticamente)
├── .env                   # Credenciais
└── requirements.txt       # Dependências
```

---

## 🎨 Interface

### Tela Inicial
```
┌─────────────────────────────────────┐
│   🤖 Scraper V5 AI-Powered         │
│   Interface Web com IBM watsonx.ai  │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  📤 Upload do Arquivo               │
│                                     │
│  ┌───────────────────────────────┐ │
│  │         📁                    │ │
│  │  Clique ou arraste o arquivo  │ │
│  │  orgaos.txt aqui              │ │
│  │                               │ │
│  │  Formato: SIGLA|Nome|URL      │ │
│  └───────────────────────────────┘ │
└─────────────────────────────────────┘
```

### Durante Execução
```
┌─────────────────────────────────────┐
│  📊 Status da Execução              │
│                                     │
│  ┌─────┐  ┌─────┐  ┌─────┐        │
│  │  7  │  │  3  │  │ 11  │        │
│  │Total│  │Proc.│  │ IA  │        │
│  └─────┘  └─────┘  └─────┘        │
│                                     │
│  ████████████░░░░░░░░░░░░ 43%     │
│                                     │
│  [12:34:56] 🚀 Scraper iniciado!   │
│  [12:34:58] 🔄 Processando GOVERNO │
│  [12:35:02] ✓ GOVERNO-PR concluído │
│  [12:35:04] 🔄 Processando TCE-PR  │
└─────────────────────────────────────┘
```

---

## 🔒 Segurança

### Validações Implementadas

1. **Upload:**
   - Apenas arquivos .txt
   - Tamanho máximo: 16MB
   - Validação de formato

2. **Execução:**
   - ID único por execução
   - Isolamento de arquivos
   - Timeout automático

3. **Download:**
   - Verificação de conclusão
   - Arquivo temporário
   - Limpeza automática

---

## 🐛 Troubleshooting

### Erro: "Address already in use"

**Causa:** Porta 5000 já está em uso

**Solução:**
```bash
# Mudar porta no app.py (última linha)
socketio.run(app, port=5001)  # Usar porta 5001
```

### Erro: "Module 'flask' not found"

**Causa:** Dependências não instaladas

**Solução:**
```bash
pip install flask flask-socketio python-socketio
```

### WebSocket não conecta

**Causa:** Firewall ou proxy

**Solução:**
```bash
# Testar localmente primeiro
curl http://localhost:5000
```

---

## 🚀 Melhorias Futuras

### Planejadas:
- [ ] Autenticação de usuários
- [ ] Histórico de execuções
- [ ] Agendamento de tarefas
- [ ] API REST completa
- [ ] Dashboard com gráficos
- [ ] Exportar para CSV/JSON
- [ ] Filtros e busca
- [ ] Comparação de resultados

---

## 📞 Suporte

**Problemas com a interface web?**

1. Verifique se Flask está instalado:
   ```bash
   pip list | grep -i flask
   ```

2. Teste o scraper CLI primeiro:
   ```bash
   python scraper_v5_ai.py
   ```

3. Verifique logs do Flask no terminal

4. Consulte documentação:
   - `README_V5.md` - Scraper
   - `GUIA_INSTALACAO.md` - Instalação
   - `CORRIGIR_WATSONX.md` - Troubleshooting

---

## 💡 Dicas

### Desenvolvimento

```bash
# Modo debug (auto-reload)
export FLASK_ENV=development
python app.py
```

### Produção

```bash
# Usar servidor WSGI (gunicorn)
pip install gunicorn
gunicorn -k eventlet -w 1 app:app
```

### Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

---

**Criado por:** Bob  
**Data:** 2026-05-21  
**Versão:** 1.0