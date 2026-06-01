"""
Web Scraper V5 - AI-Powered with IBM watsonx.ai
Scraper inteligente que usa IA para ler e interpretar páginas web
"""

import os
import json
import time
import re
import warnings
from datetime import datetime
from typing import List, Dict, Optional, Any
from urllib.parse import urljoin

# Suprimir warnings de deprecation da API (não afeta funcionamento)
warnings.filterwarnings('ignore', category=UserWarning, module='ibm_watsonx_ai')

# Selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# Data processing
from bs4 import BeautifulSoup
import pandas as pd

# IBM watsonx.ai
try:
    from ibm_watsonx_ai import APIClient
    from ibm_watsonx_ai import Credentials
    from ibm_watsonx_ai.foundation_models import ModelInference
    from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
    WATSONX_AVAILABLE = True
except ImportError as e:
    WATSONX_AVAILABLE = False
    print("="*70)
    print("⚠️  IBM WATSONX.AI NÃO DISPONÍVEL")
    print("="*70)
    print("❌ Pacote 'ibm-watsonx-ai' não está instalado.")
    print()
    print("💡 SOLUÇÃO:")
    print("   pip install ibm-watsonx-ai")
    print()
    print("   OU instale todas as dependências:")
    print("   pip install -r requirements.txt")
    print()
    print("📋 Para diagnóstico completo, execute:")
    print("   python test_watsonx.py")
    print("="*70)
    print()
    print("🔄 Continuando em modo fallback (sem IA)...")
    print()

# Environment variables
from dotenv import load_dotenv
load_dotenv()

#-----------------------------------------------------------------------
# COMPONENTE 1: IBM WATSONX.AI CLIENT
#-----------------------------------------------------------------------

class IBMWatsonxClient:
    """Cliente para integração com IBM watsonx.ai"""
    
    def __init__(self):
        """Inicializa cliente IBM watsonx.ai"""
        self.available = WATSONX_AVAILABLE
        self.client = None
        self.model = None
        
        if not self.available:
            return
        
        # Carregar credenciais
        self.api_key = os.getenv('IBM_WATSONX_API_KEY')
        self.project_id = os.getenv('IBM_WATSONX_PROJECT_ID')
        self.url = os.getenv('IBM_WATSONX_URL', 'https://us-south.ml.cloud.ibm.com')
        
        # Validar credenciais
        if not self.api_key or self.api_key == 'your_api_key_here':
            print("="*70)
            print("❌ API KEY NÃO CONFIGURADA")
            print("="*70)
            print("A variável IBM_WATSONX_API_KEY não está configurada no arquivo .env")
            print()
            print("💡 SOLUÇÃO:")
            print("   1. Verifique se o arquivo .env existe na pasta v5/")
            print("   2. Abra o arquivo .env e configure:")
            print("      IBM_WATSONX_API_KEY=sua_api_key_real_aqui")
            print()
            print("📋 Para obter sua API Key:")
            print("   1. Acesse: https://cloud.ibm.com/")
            print("   2. Vá em perfil → API keys → Create")
            print("   3. Copie a chave gerada")
            print()
            print("📖 Consulte: CORRIGIR_WATSONX.md para guia completo")
            print("="*70)
            print()
            self.available = False
            return
        
        if not self.project_id or self.project_id == 'your_project_id_here':
            print("="*70)
            print("❌ PROJECT ID NÃO CONFIGURADO")
            print("="*70)
            print("A variável IBM_WATSONX_PROJECT_ID não está configurada no arquivo .env")
            print()
            print("💡 SOLUÇÃO:")
            print("   1. Abra o arquivo .env e configure:")
            print("      IBM_WATSONX_PROJECT_ID=seu_project_id_real_aqui")
            print()
            print("📋 Para obter seu Project ID:")
            print("   1. Acesse: https://dataplatform.cloud.ibm.com/")
            print("   2. Vá em Projects → Seu projeto")
            print("   3. Manage → General → Copie o Project ID")
            print()
            print("📖 Consulte: CORRIGIR_WATSONX.md para guia completo")
            print("="*70)
            print()
            self.available = False
            return
        
        try:
            # Inicializar cliente
            credentials = Credentials(
                url=self.url,
                api_key=self.api_key
            )
            
            self.client = APIClient(credentials)
            
            # Configurar modelo (Granite 4 H Small - suporta geração de texto)
            # Parâmetros ajustados para garantir geração de resposta
            self.model = ModelInference(
                model_id="ibm/granite-4-h-small",
                api_client=self.client,
                project_id=self.project_id,
                params={
                    "max_new_tokens": 1000,  # Reduzido para resposta mais focada
                    "min_new_tokens": 50,     # Garantir mínimo de tokens
                    "temperature": 0.3,       # Aumentado para mais criatividade
                    "top_p": 0.95,
                    "repetition_penalty": 1.2
                }
            )
            
            print("✓ IBM watsonx.ai inicializado")
            
        except Exception as e:
            error_msg = str(e)
            print("="*70)
            print("❌ ERRO AO CONECTAR COM IBM WATSONX.AI")
            print("="*70)
            print(f"Erro: {error_msg[:200]}")
            print()
            
            # Diagnóstico específico baseado no erro
            if 'Unauthorized' in error_msg or '401' in error_msg:
                print("💡 CAUSA PROVÁVEL: API Key inválida")
                print()
                print("SOLUÇÕES:")
                print("   1. Verifique se a API Key está correta no .env")
                print("   2. Gere uma nova API Key em: https://cloud.ibm.com/")
                print("   3. Certifique-se de copiar a chave completa (sem espaços)")
                
            elif 'Not Found' in error_msg or '404' in error_msg:
                print("💡 CAUSA PROVÁVEL: Project ID inválido ou URL incorreta")
                print()
                print("SOLUÇÕES:")
                print("   1. Verifique o Project ID no .env")
                print("   2. Copie o ID correto de: https://dataplatform.cloud.ibm.com/")
                print("   3. Verifique se a URL está correta para sua região")
                
            elif 'Forbidden' in error_msg or '403' in error_msg:
                print("💡 CAUSA PROVÁVEL: Sem permissão ou serviço não ativado")
                print()
                print("SOLUÇÕES:")
                print("   1. Ative o watsonx.ai em: https://cloud.ibm.com/")
                print("   2. Verifique se tem um plano ativo (Lite ou pago)")
                print("   3. Associe o watsonx.ai Runtime ao seu projeto")
                
            elif 'Connection' in error_msg or 'Network' in error_msg:
                print("💡 CAUSA PROVÁVEL: Problema de conexão com internet")
                print()
                print("SOLUÇÕES:")
                print("   1. Verifique sua conexão com internet")
                print("   2. Verifique se não há firewall bloqueando")
                print("   3. Tente novamente em alguns minutos")
                
            else:
                print("💡 CAUSA: Erro desconhecido")
                print()
                print("SOLUÇÕES:")
                print("   1. Execute o diagnóstico: python test_watsonx.py")
                print("   2. Consulte: CORRIGIR_WATSONX.md")
                print("   3. Verifique se todas as credenciais estão corretas")
            
            print()
            print("📋 Para diagnóstico completo:")
            print("   python test_watsonx.py")
            print("="*70)
            print()
            
            self.available = False
    
    def extract_contacts(self, html_content: str, context: str = "") -> Dict[str, Any]:
        """
        Extrai contatos usando IA
        
        Args:
            html_content: Conteúdo HTML da página
            context: Contexto adicional (nome do órgão, etc)
        
        Returns:
            Dict com contatos extraídos e metadados
        """
        if not self.available:
            return {"success": False, "error": "IA não disponível"}
        
        try:
            # Limpar HTML (remover scripts, styles, etc)
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Remover elementos desnecessários
            for tag in soup(['script', 'style', 'nav', 'footer', 'header']):
                tag.decompose()
            
            # Extrair texto limpo
            text_content = soup.get_text(separator='\n', strip=True)
            
            # Buscar links e textos de contato
            links_contato = []
            for link in soup.find_all('a', href=True):
                href = link.get('href', '')
                text = link.get_text(strip=True)
                if any(palavra in href.lower() or palavra in text.lower()
                       for palavra in ['contato', 'fale', 'ouvidoria', 'atendimento', 'equipe', 'diretoria', 'ti', 'tecnologia']):
                    links_contato.append(f"{text}: {href}")
            
            # Priorizar seções com palavras-chave de TI e contato
            lines = text_content.split('\n')
            relevant_lines = []
            ti_keywords = ['tecnologia', 'informação', 'informática', 'ti', 'tic',
                          'sistemas', 'digital', 'dados', 'contato', 'email', 'telefone',
                          'diretor', 'coordenador', 'gerente', 'chefe', '@']
            
            for line in lines:
                line_lower = line.lower()
                # Priorizar linhas com palavras-chave
                if any(kw in line_lower for kw in ti_keywords):
                    relevant_lines.append(line)
                elif len(line.strip()) > 10:  # Ignorar linhas muito curtas
                    relevant_lines.append(line)
            
            # Adicionar links de contato encontrados
            if links_contato:
                relevant_lines.extend(["\n=== LINKS DE CONTATO ==="] + links_contato)
            
            # Limitar tamanho para API (aumentado para 5000 chars)
            text_content = '\n'.join(relevant_lines[:300])[:5000]
            
            # Criar prompt
            prompt = self._create_extraction_prompt(text_content, context)
            
            # Chamar IA
            print("   🤖 Consultando IBM watsonx.ai...")
            response = self.model.generate_text(prompt=prompt)
            
            # Parsear resposta
            result = self._parse_response(response)
            
            return result
            
        except Exception as e:
            print(f"   ❌ Erro na IA: {str(e)[:100]}")
            return {"success": False, "error": str(e)}
    
    def _create_extraction_prompt(self, content: str, context: str) -> str:
        """Cria prompt otimizado para extração agressiva"""
        
        prompt = f"""Encontre QUALQUER pessoa relacionada a TI/Tecnologia/Informática no texto.

ACEITE dados parciais:
- Nome sozinho (sem email/telefone)
- Email sozinho (sem nome)
- Qualquer menção a cargo de TI

Busque por:
- Nomes de pessoas (2-4 palavras)
- Emails (@gov.br, @.br)
- Telefones ((XX) XXXX-XXXX)
- Cargos: Diretor, Coordenador, Gerente, Chefe, Analista, Técnico
- Áreas: TI, TIC, Tecnologia, Informática, Sistemas, Digital

Retorne JSON:
{{
  "contatos": [
    {{"nome": "Nome", "cargo": "Cargo TI", "email": "email", "telefone": "tel", "confianca": 0.5}}
  ]
}}

Texto:
{content}

JSON:"""

        return prompt
    
    def _parse_response(self, response: str) -> Dict[str, Any]:
        """Parseia resposta da IA"""
        try:
            # Tentar extrair JSON da resposta
            # A IA pode retornar texto antes/depois do JSON
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            
            if json_match:
                json_str = json_match.group(0)
                data = json.loads(json_str)
                
                # Validar estrutura
                if 'contatos' in data and isinstance(data['contatos'], list):
                    return {
                        "success": True,
                        "contatos": data['contatos'],
                        "raw_response": response
                    }
            
            # Se não conseguiu parsear, retornar erro
            return {
                "success": False,
                "error": "Resposta inválida da IA",
                "raw_response": response
            }
            
        except json.JSONDecodeError as e:
            return {
                "success": False,
                "error": f"Erro ao parsear JSON: {e}",
                "raw_response": response
            }
    
    def validate_contact(self, nome: str, cargo: str, context: str = "") -> float:
        """
        Valida um contato usando IA (retorna score de confiança)
        
        Args:
            nome: Nome da pessoa
            cargo: Cargo/setor
            context: Contexto adicional
        
        Returns:
            Score de confiança (0.0 a 1.0)
        """
        if not self.available:
            return 0.5  # Confiança média se IA não disponível
        
        try:
            prompt = f"""Analise se o seguinte é um contato válido de uma pessoa real da área de TI:

Nome: {nome}
Cargo: {cargo}
Contexto: {context}

Responda APENAS com um número de 0.0 a 1.0 indicando a confiança:
- 1.0 = Certamente uma pessoa real de TI
- 0.5 = Incerto
- 0.0 = Certamente NÃO é uma pessoa real

Resposta (apenas o número):"""

            response = self.model.generate_text(prompt=prompt)
            
            # Extrair número da resposta
            match = re.search(r'0\.\d+|1\.0', response)
            if match:
                return float(match.group(0))
            
            return 0.5
            
        except:
            return 0.5

#-----------------------------------------------------------------------
# COMPONENTE 2: VALIDADOR (Fallback do V4)
#-----------------------------------------------------------------------

class ValidadorDadosRigoroso:
    """Validação rigorosa para fallback quando IA não disponível"""
    
    PALAVRAS_PROIBIDAS_NOMES = {
        'coordenadoria', 'diretoria', 'secretaria', 'assessoria',
        'superintendência', 'gerência', 'coordenação', 'gabinete',
        'núcleo', 'divisão', 'setor', 'departamento', 'seção',
        'superintendencia', 'gerencia', 'coordenacao', 'nucleo', 'divisao'
    }
    
    @staticmethod
    def eh_nome_pessoa_real(texto):
        """Valida se texto é nome de pessoa real"""
        if not texto or not isinstance(texto, str):
            return False
        
        texto = texto.strip()
        if len(texto) < 6:
            return False
        
        palavras = texto.split()
        if not (2 <= len(palavras) <= 4):
            return False
        
        # Verificar palavras proibidas
        texto_lower = texto.lower()
        for palavra_proibida in ValidadorDadosRigoroso.PALAVRAS_PROIBIDAS_NOMES:
            if palavra_proibida in texto_lower:
                return False
        
        # Cada palavra deve começar com maiúscula
        for palavra in palavras:
            if not palavra or not palavra[0].isupper():
                return False
        
        return True
    
    @staticmethod
    def validar_email(email):
        """Valida formato de email"""
        if not email:
            return False
        padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(padrao, email.lower().strip()))
    
    @staticmethod
    def validar_telefone(telefone):
        """Valida formato de telefone brasileiro"""
        if not telefone:
            return False
        digitos = re.sub(r'[^\d]', '', telefone)
        return 10 <= len(digitos) <= 11

#-----------------------------------------------------------------------
# COMPONENTE 3: SCRAPER V5 AI-POWERED
#-----------------------------------------------------------------------

class ScraperV5AI:
    """Scraper V5 com IA"""
    
    def __init__(self, headless=False, ai_only=False):
        """
        Inicializa scraper
        
        Args:
            headless: Executar sem interface gráfica
            ai_only: Usar apenas IA (sem fallback)
        """
        # Configurar Chrome
        chrome_options = Options()
        if headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Inicializar componentes
            self.ai_client = IBMWatsonxClient()
            self.validador = ValidadorDadosRigoroso()
            self.ai_only = ai_only
            
            self.dados_coletados = []
            self.log_processamento = []
            
            print("✓ Scraper V5 AI-Powered inicializado")
            
            if not self.ai_client.available and ai_only:
                print("⚠️ Modo AI-only ativado mas IA não disponível!")
                print("   Desative --ai-only ou configure credenciais IBM watsonx.ai")
            
        except Exception as e:
            print(f"❌ Erro ao inicializar: {e}")
            raise
    
    def adicionar_log(self, orgao_sigla, status, detalhes, metodo=""):
        """Adiciona entrada no log"""
        self.log_processamento.append({
            'Órgão Sigla': orgao_sigla,
            'Status': status,
            'Método': metodo,
            'Detalhes': detalhes,
            'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    
    def obter_orgaos(self):
        """Lê órgãos do arquivo orgaos.txt"""
        orgaos = []
        
        try:
            # Tentar v5/orgaos.txt primeiro, depois ../orgaos.txt
            caminhos = ['orgaos.txt', '../orgaos.txt']
            
            for caminho in caminhos:
                if os.path.exists(caminho):
                    with open(caminho, 'r', encoding='utf-8') as f:
                        for linha in f:
                            linha = linha.strip()
                            if linha and not linha.startswith('#'):
                                partes = linha.split('|')
                                if len(partes) == 3:
                                    orgaos.append({
                                        'sigla': partes[0].strip(),
                                        'nome': partes[1].strip(),
                                        'url': partes[2].strip()
                                    })
                    break
            
            if orgaos:
                print(f"✓ {len(orgaos)} órgãos carregados")
            else:
                print("❌ Nenhum órgão encontrado em orgaos.txt")
            
            return orgaos
            
        except Exception as e:
            print(f"❌ Erro ao ler orgaos.txt: {e}")
            return []
    
    def processar_orgao(self, orgao):
        """Processa um órgão usando IA"""
        print(f"\n{'='*70}")
        print(f"🏢 [{orgao['sigla']}] {orgao['nome']}")
        print(f"{'='*70}")
        
        try:
            # Navegar para a página
            print(f"   🌐 Acessando: {orgao['url']}")
            self.driver.get(orgao['url'])
            time.sleep(5)  # Aguardar carregamento
            
            # Expandir elementos (accordions, etc)
            self._expandir_elementos()
            
            # Obter HTML completo
            html_content = self.driver.page_source
            
            # Tentar extração com IA primeiro
            if self.ai_client.available:
                print(f"   🤖 Método: IBM watsonx.ai")
                result = self.ai_client.extract_contacts(
                    html_content,
                    context=f"{orgao['nome']} ({orgao['sigla']})"
                )
                
                # Debug: mostrar resultado da IA
                print(f"   📊 IA retornou: success={result.get('success')}")
                
                if result.get('success'):
                    contatos = result.get('contatos', [])
                    print(f"   📊 Total de contatos retornados: {len(contatos)}")
                    
                    # Debug: mostrar scores de confiança
                    if contatos:
                        scores = [c.get('confianca', 0) for c in contatos]
                        print(f"   📊 Scores de confiança: min={min(scores):.2f}, max={max(scores):.2f}, média={sum(scores)/len(scores):.2f}")
                    
                    # Aceitar TODOS os contatos (remover filtro de confiança por enquanto)
                    contatos_validos = contatos
                    print(f"   📊 Contatos aceitos: {len(contatos_validos)}")
                    
                    # Se encontrou contatos válidos, usar IA
                    if contatos_validos:
                        # Salvar dados
                        for contato in contatos_validos:
                            self.dados_coletados.append({
                                'Órgão Nome': orgao['nome'],
                                'Órgão Sigla': orgao['sigla'],
                                'Nome da Pessoa': contato.get('nome') or 'Não encontrado',
                                'Cargo / Setor': contato.get('cargo') or 'Não encontrado',
                                'E-mail': contato.get('email') or 'Não encontrado',
                                'Telefone': contato.get('telefone') or 'Não encontrado',
                                'Método': 'IA'
                            })
                        
                        print(f"   ✅ {len(contatos_validos)} contatos extraídos (IA)")
                        self.adicionar_log(orgao['sigla'], 'SUCESSO',
                                         f"{len(contatos_validos)} contatos", "IA")
                        return
                    else:
                        print(f"   ⚠️  IA não encontrou contatos com confiança suficiente")
                else:
                    print(f"   ⚠️  IA falhou: {result.get('error', 'Erro desconhecido')}")
                    if 'raw_response' in result:
                        print(f"   📝 Resposta da IA (primeiros 200 chars): {result['raw_response'][:200]}")
            
            # Tentar IA novamente com prompt mais agressivo se não encontrou nada
            if not self.ai_only:
                print(f"   🔄 Tentando IA novamente com busca mais agressiva...")
                
                # Criar prompt ainda mais simples e direto
                simple_prompt = f"""Liste QUALQUER nome de pessoa ou email encontrado no texto relacionado a tecnologia, TI, informática ou sistemas.

Formato JSON:
{{"contatos": [{{"nome": "Nome", "cargo": "TI", "email": "", "telefone": "", "confianca": 0.5}}]}}

Texto:
{html_content[:4000]}

JSON:"""
                
                try:
                    response = self.ai_client.model.generate_text(prompt=simple_prompt)
                    result2 = self.ai_client._parse_response(response)
                    
                    if result2.get('success') and result2.get('contatos'):
                        contatos2 = result2.get('contatos', [])
                        print(f"   📊 Segunda tentativa: {len(contatos2)} contatos")
                        
                        for contato in contatos2:
                            self.dados_coletados.append({
                                'Órgão Nome': orgao['nome'],
                                'Órgão Sigla': orgao['sigla'],
                                'Nome da Pessoa': contato.get('nome') or 'Não encontrado',
                                'Cargo / Setor': contato.get('cargo') or 'Não encontrado',
                                'E-mail': contato.get('email') or 'Não encontrado',
                                'Telefone': contato.get('telefone') or 'Não encontrado',
                                'Método': 'IA-Retry'
                            })
                        
                        print(f"   ✅ {len(contatos2)} contatos extraídos (IA-Retry)")
                        self.adicionar_log(orgao['sigla'], 'SUCESSO',
                                         f"{len(contatos2)} contatos", "IA-Retry")
                        return
                except:
                    pass
                
                # Se IA falhou mesmo após retry, usar fallback
                print(f"   ⚠️ IA não encontrou contatos, usando Fallback...")
                contatos_fallback = self._extrair_fallback(html_content)
                
                for contato in contatos_fallback:
                    self.dados_coletados.append({
                        'Órgão Nome': orgao['nome'],
                        'Órgão Sigla': orgao['sigla'],
                        'Nome da Pessoa': contato.get('nome') or 'Não encontrado',
                        'Cargo / Setor': contato.get('cargo') or 'Não encontrado',
                        'E-mail': contato.get('email') or 'Não encontrado',
                        'Telefone': contato.get('telefone') or 'Não encontrado',
                        'Método': 'Fallback'
                    })
                
                print(f"   ✅ {len(contatos_fallback)} contatos extraídos (Fallback)")
                self.adicionar_log(orgao['sigla'], 'SUCESSO',
                                 f"{len(contatos_fallback)} contatos", "Fallback")
            else:
                print(f"   ⚠️ IA falhou e modo AI-only ativado")
                self.adicionar_log(orgao['sigla'], 'FALHA',
                                 "IA falhou, AI-only ativado", "IA")
            
        except Exception as e:
            print(f"   ❌ Erro: {str(e)[:100]}")
            self.adicionar_log(orgao['sigla'], 'ERRO', str(e)[:200], "")
    
    def _expandir_elementos(self):
        """Expande elementos clicáveis da página"""
        try:
            self.driver.execute_script("""
                const seletores = [
                    '[class*="accordion"]',
                    '[class*="collapse"]',
                    '[data-toggle="collapse"]',
                    'button[aria-expanded="false"]'
                ];
                
                seletores.forEach(seletor => {
                    document.querySelectorAll(seletor).forEach(el => {
                        try { el.click(); } catch(e) {}
                    });
                });
            """)
            time.sleep(2)
        except:
            pass
    
    def _extrair_fallback(self, html_content):
        """Extração usando padrões V4 (fallback)"""
        soup = BeautifulSoup(html_content, 'html.parser')
        contatos = []
        
        # Buscar em texto livre
        texto = soup.get_text(separator='\n')
        linhas = [l.strip() for l in texto.split('\n') if l.strip()]
        
        palavras_ti = ['tecnologia', 'informação', 'informática', 'ti', 'tic', 'sistemas']
        
        for i, linha in enumerate(linhas):
            linha_lower = linha.lower()
            
            # Se linha menciona TI
            if any(palavra in linha_lower for palavra in palavras_ti):
                # Procurar nome nas próximas linhas
                for j in range(i, min(i+5, len(linhas))):
                    if self.validador.eh_nome_pessoa_real(linhas[j]):
                        contatos.append({
                            'nome': linhas[j],
                            'cargo': linha,
                            'email': '',
                            'telefone': ''
                        })
                        break
        
        return contatos[:10]  # Limitar a 10
    
    def salvar_excel(self):
        """Salva dados em Excel"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"contatos_v5_ai_{timestamp}.xlsx"
        
        with pd.ExcelWriter(nome_arquivo, engine='openpyxl') as writer:
            # Sempre criar sheet de contatos (mesmo que vazia)
            if self.dados_coletados:
                df = pd.DataFrame(self.dados_coletados)
                df = df.drop_duplicates()
            else:
                # Criar DataFrame vazio com colunas
                df = pd.DataFrame(columns=[
                    'Órgão Nome', 'Órgão Sigla', 'Nome da Pessoa',
                    'Cargo / Setor', 'E-mail', 'Telefone', 'Método'
                ])
            
            df.to_excel(writer, index=False, sheet_name='Contatos TI')
            
            # Ajustar largura das colunas
            if len(df) > 0:
                worksheet = writer.sheets['Contatos TI']
                for idx, col in enumerate(df.columns):
                    max_length = max(df[col].astype(str).apply(len).max(), len(col)) + 2
                    worksheet.column_dimensions[chr(65 + idx)].width = min(max_length, 50)
            
            # Sempre criar sheet de log
            if self.log_processamento:
                df_log = pd.DataFrame(self.log_processamento)
            else:
                df_log = pd.DataFrame(columns=['Órgão Sigla', 'Status', 'Método', 'Detalhes', 'Timestamp'])
            
            df_log.to_excel(writer, index=False, sheet_name='Log')
        
        print(f"\n{'='*70}")
        print(f"💾 Arquivo: {nome_arquivo}")
        if self.dados_coletados:
            df = pd.DataFrame(self.dados_coletados)
            print(f"📊 Total: {len(df)} registros")
            print(f"🤖 Via IA: {len(df[df['Método'] == 'IA'])}")
            print(f"🔄 Via Fallback: {len(df[df['Método'] == 'Fallback'])}")
        print(f"{'='*70}")
        
        return nome_arquivo
    
    def executar(self):
        """Executa scraper para todos os órgãos"""
        print("\n" + "="*70)
        print("🚀 SCRAPER V5 - AI-POWERED")
        print("="*70)
        
        try:
            orgaos = self.obter_orgaos()
            print(f"\n📋 Órgãos: {len(orgaos)}")
            
            for i, orgao in enumerate(orgaos, 1):
                print(f"\n{'#'*70}")
                print(f"# {i}/{len(orgaos)}")
                print(f"{'#'*70}")
                self.processar_orgao(orgao)
                time.sleep(2)
            
            self.salvar_excel()
            print(f"\n✅ Concluído!")
            
        except Exception as e:
            print(f"\n❌ Erro: {e}")
            if self.dados_coletados:
                self.salvar_excel()
        finally:
            self.driver.quit()

#-----------------------------------------------------------------------
# MAIN
#-----------------------------------------------------------------------

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Scraper V5 - AI-Powered')
    parser.add_argument('--headless', action='store_true', help='Executar sem interface gráfica')
    parser.add_argument('--ai-only', action='store_true', help='Usar apenas IA (sem fallback)')
    parser.add_argument('--debug', action='store_true', help='Modo debug (verbose)')
    
    args = parser.parse_args()
    
    try:
        scraper = ScraperV5AI(headless=args.headless, ai_only=args.ai_only)
        scraper.executar()
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}")

if __name__ == "__main__":
    main()

# Made with Bob - Scraper V5 AI-Powered