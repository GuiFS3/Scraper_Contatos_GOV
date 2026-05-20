"""
Web Scraper V2 - Refatorado com Lógica Robusta
Separação correta de Cargo, Nome, Email e Telefone
"""
#-----------------------------------------------------------------------

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
from datetime import datetime
from urllib.parse import urljoin, urlparse

#-----------------------------------------------------------------------

class ExtractorDados:
    """Classe para extração limpa e estruturada de dados"""
    
    @staticmethod
    def extrair_emails(texto):
        """Extrai apenas emails válidos"""
        padrao = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(padrao, texto)
        return list(set([e.lower() for e in emails if '@' in e and '.' in e]))
    
    @staticmethod
    def extrair_telefones(texto):
        """Extrai apenas telefones válidos"""
        padroes = [
            r'\(?\d{2}\)?\s?\d{4,5}[-\s]?\d{4}',
        ]
        telefones = set()
        for padrao in padroes:
            matches = re.findall(padrao, texto)
            for match in matches:
                # Limpar e validar
                digitos = re.sub(r'[^\d]', '', match)
                if 10 <= len(digitos) <= 11:  # Telefone brasileiro válido
                    telefones.add(match)
        return list(telefones)
    
    @staticmethod
    def eh_nome_valido(texto):
        """Verifica se um texto parece um nome de pessoa"""
        if not texto or len(texto) < 3:
            return False
        
        # Remover espaços extras
        texto = ' '.join(texto.split())
        
        # Não pode ser muito longo (provavelmente é descrição)
        if len(texto) > 60:
            return False
        
        # Deve ter 2-5 palavras
        palavras = texto.split()
        if not (2 <= len(palavras) <= 5):
            return False
        
        # Primeira letra deve ser maiúscula
        if not texto[0].isupper():
            return False
        
        # Não pode conter palavras-chave que indicam que não é nome
        palavras_invalidas = [
            'email', 'e-mail', 'telefone', 'fone', 'tel', 'contato',
            'diretor', 'gerente', 'coordenador', 'chefe', 'assessor',
            'diretoria', 'gerência', 'coordenação', 'setor', 'departamento',
            'rua', 'avenida', 'av.', 'cep', 'andar', 'sala', 'edifício',
            'protocolo', 'serviço', 'componente', 'plano', 'programa'
        ]
        
        texto_lower = texto.lower()
        if any(palavra in texto_lower for palavra in palavras_invalidas):
            return False
        
        # Não pode ter @ ou números demais
        if '@' in texto or texto.count('(') > 1:
            return False
        
        return True
    
    @staticmethod
    def eh_cargo_valido(texto):
        """Verifica se um texto parece um cargo/setor"""
        if not texto or len(texto) < 5:
            return False
        
        # Remover espaços extras
        texto = ' '.join(texto.split())
        
        # Não pode ser muito longo (provavelmente é descrição/endereço)
        if len(texto) > 150:
            return False
        
        texto_lower = texto.lower()
        
        # Deve conter palavras-chave de cargo/setor
        palavras_cargo = [
            'diretor', 'gerente', 'gerência', 'coordenador', 'coordenação',
            'chefe', 'assessor', 'superintendente', 'diretoria',
            'setor', 'departamento', 'núcleo', 'divisão', 'secretário'
        ]
        
        tem_palavra_cargo = any(palavra in texto_lower for palavra in palavras_cargo)
        
        # Não pode começar com "E-mail:" ou "Telefone:"
        if texto_lower.startswith(('e-mail:', 'email:', 'telefone:', 'fone:', 'tel:')):
            return False
        
        # Não pode ter @ (é email, não cargo)
        if '@' in texto:
            return False
        
        # Não pode ser endereço completo
        if any(palavra in texto_lower for palavra in ['cep', 'andar', 'sala', 'edifício', 'rua', 'avenida']):
            return False
        
        return tem_palavra_cargo
    
    @staticmethod
    def limpar_cargo(texto):
        """Limpa e normaliza texto de cargo"""
        if not texto:
            return ''
        
        # Remover prefixos comuns
        texto = re.sub(r'^(Cargo:|Função:|Setor:)\s*', '', texto, flags=re.I)
        
        # Remover espaços extras
        texto = ' '.join(texto.split())
        
        # Limitar tamanho
        if len(texto) > 100:
            texto = texto[:100] + '...'
        
        return texto
    
    @staticmethod
    def extrair_dados_estruturados(soup, palavras_ti):
        """Extrai dados de forma estruturada e limpa"""
        dados = []
        
        # Obter todo o texto
        texto_completo = soup.get_text(separator='\n')
        linhas = [l.strip() for l in texto_completo.split('\n') if l.strip()]
        
        i = 0
        while i < len(linhas):
            linha_atual = linhas[i]
            linha_lower = linha_atual.lower()
            
            # Verificar se linha menciona TI e parece um cargo
            if any(palavra in linha_lower for palavra in palavras_ti):
                if ExtractorDados.eh_cargo_valido(linha_atual):
                    
                    cargo = ExtractorDados.limpar_cargo(linha_atual)
                    nome = ''
                    email = ''
                    telefone = ''
                    
                    # Analisar próximas 15 linhas
                    for j in range(i+1, min(i+16, len(linhas))):
                        linha_seg = linhas[j]
                        linha_seg_lower = linha_seg.lower()
                        
                        # Parar se encontrou outro cargo
                        if j > i+3 and ExtractorDados.eh_cargo_valido(linha_seg):
                            break
                        
                        # Extrair nome (padrão "Nome: Fulano" ou linha com nome válido)
                        if linha_seg_lower.startswith('nome:'):
                            nome_extraido = linha_seg.split(':', 1)[1].strip()
                            if ExtractorDados.eh_nome_valido(nome_extraido):
                                nome = nome_extraido
                        elif not nome and ExtractorDados.eh_nome_valido(linha_seg):
                            # Verificar se não é a próxima linha que já é outro campo
                            if not linha_seg_lower.startswith(('e-mail:', 'email:', 'telefone:', 'fone:')):
                                nome = linha_seg
                        
                        # Extrair email (padrão "E-mail: email@domain" ou email solto)
                        if 'e-mail:' in linha_seg_lower or 'email:' in linha_seg_lower:
                            emails_linha = ExtractorDados.extrair_emails(linha_seg)
                            if emails_linha and not email:
                                email = emails_linha[0]
                        elif not email:
                            emails_linha = ExtractorDados.extrair_emails(linha_seg)
                            if emails_linha:
                                email = emails_linha[0]
                        
                        # Extrair telefone (padrão "Telefone: (XX) XXXX-XXXX" ou telefone solto)
                        if 'telefone:' in linha_seg_lower or 'fone:' in linha_seg_lower:
                            telefones_linha = ExtractorDados.extrair_telefones(linha_seg)
                            if telefones_linha and not telefone:
                                telefone = telefones_linha[0]
                        elif not telefone:
                            telefones_linha = ExtractorDados.extrair_telefones(linha_seg)
                            if telefones_linha:
                                telefone = telefones_linha[0]
                    
                    # Salvar se encontrou dados relevantes
                    if email or telefone or nome:
                        dados.append({
                            'nome': nome if nome else '-',
                            'cargo': cargo,
                            'email': email,
                            'telefone': telefone
                        })
            
            i += 1
        
        return dados

#-----------------------------------------------------------------------

class ScraperV2:
    """Scraper refatorado com lógica robusta"""
    
    def __init__(self, headless=False):
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
            self.wait = WebDriverWait(self.driver, 10)
            self.extractor = ExtractorDados()
            self.dados_coletados = []
            self.log_processamento = []
            print("✓ Selenium inicializado")
        except Exception as e:
            print(f"❌ Erro: {e}")
            raise
    
    def adicionar_log(self, orgao_sigla, status, detalhes):
        self.log_processamento.append({
            'Órgão Sigla': orgao_sigla,
            'Status': status,
            'Detalhes': detalhes,
            'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    
    def obter_orgaos(self):
        """Lê órgãos do arquivo orgaos.txt"""
        orgaos = []
        
        try:
            with open('orgaos.txt', 'r', encoding='utf-8') as f:
                for linha in f:
                    linha = linha.strip()
                    if linha and not linha.startswith('#'):  # Ignora linhas vazias e comentários
                        partes = linha.split('|')
                        if len(partes) == 3:
                            orgaos.append({
                                'sigla': partes[0].strip(),
                                'nome': partes[1].strip(),
                                'url': partes[2].strip()
                            })
            
            print(f"✓ {len(orgaos)} órgãos carregados de orgaos.txt")
            return orgaos
            
        except FileNotFoundError:
            print("❌ Arquivo orgaos.txt não encontrado!")
            print("   Crie o arquivo com formato: SIGLA|Nome do Órgão|URL")
            return []
        except Exception as e:
            print(f"❌ Erro ao ler orgaos.txt: {e}")
            return []
    
    def calcular_score_link(self, link_elem, url_base):
        score = 0
        try:
            href = link_elem.get('href', '')
            texto = link_elem.get_text(strip=True).lower()
            
            if not href or not texto:
                return 0
            
            # Alta prioridade
            if any(p in texto or p in href.lower() for p in ['organograma', 'quem é quem', 'quem-e-quem']):
                score += 10
            
            # Média prioridade
            if any(p in texto or p in href.lower() for p in ['estrutura', 'equipe', 'pessoas', 'diretoria']):
                score += 7
            
            # TI
            if any(p in texto or p in href.lower() for p in ['tecnologia', 'informática', 'ti', 'sistemas']):
                score += 8
            
            # Penalizar irrelevantes
            if any(p in texto or p in href.lower() for p in ['notícia', 'documento', 'licitação']):
                score -= 10
            
            # Bonus menu principal
            if link_elem.find_parent(['nav', 'header']):
                score += 3
            
        except:
            return 0
        
        return score
    
    def mapear_links(self, url_base, sigla_orgao):
        print(f"   🔍 Mapeando links...")
        
        try:
            self.driver.get(url_base)
            time.sleep(3)
            
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            
            links_com_score = []
            urls_vistas = set()
            
            for link in soup.find_all('a', href=True):
                href = link.get('href', '')
                if not href:
                    continue
                
                url_completa = urljoin(url_base, href)
                
                if urlparse(url_base).netloc not in urlparse(url_completa).netloc:
                    continue
                
                if url_completa in urls_vistas:
                    continue
                
                urls_vistas.add(url_completa)
                score = self.calcular_score_link(link, url_base)
                
                if score > 0:
                    links_com_score.append({
                        'texto': link.get_text(strip=True),
                        'url': url_completa,
                        'score': score
                    })
            
            links_com_score.sort(key=lambda x: x['score'], reverse=True)
            top_links = links_com_score[:10]
            
            print(f"   ✓ {len(top_links)} links relevantes")
            
            if top_links:
                print(f"   📊 Top 3:")
                for i, link in enumerate(top_links[:3], 1):
                    print(f"      {i}. [{link['score']}pts] {link['texto'][:50]}")
            
            return top_links
            
        except Exception as e:
            print(f"   ⚠️ Erro: {str(e)[:80]}")
            return []
    
    def extrair_dados_pagina(self, url, nome_orgao, sigla_orgao):
        print(f"   → Analisando: {url[:80]}...")
        
        try:
            self.driver.get(url)
            time.sleep(3)
            
            if "404" in self.driver.title:
                print(f"      ⚠️ Página 404")
                return 0
            
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            
            palavras_ti = ['tecnologia', 'informação', 'informática', 'ti', 'sistemas',
                          'digital', 'dados', 'tic', 'tecnológica']
            
            texto_pagina = soup.get_text().lower()
            if not any(palavra in texto_pagina for palavra in palavras_ti):
                print(f"      ⚠️ Sem menção a TI")
                return 0
            
            print(f"      ✓ Página contém TI")
            
            # Extrair dados estruturados
            dados = self.extractor.extrair_dados_estruturados(soup, palavras_ti)
            
            for dado in dados:
                self.dados_coletados.append({
                    'Órgão Nome': nome_orgao,
                    'Órgão Sigla': sigla_orgao,
                    'Nome da Pessoa': dado['nome'],
                    'Cargo / Setor': dado['cargo'],
                    'E-mail': dado['email'],
                    'Telefone': dado['telefone']
                })
            
            if dados:
                print(f"      ✅ {len(dados)} contato(s) extraído(s)")
                self.adicionar_log(sigla_orgao, "SUCESSO", f"{len(dados)} contatos de {url}")
            else:
                print(f"      ⚠️ Nenhum contato estruturado")
                self.adicionar_log(sigla_orgao, "SEM_DADOS", f"Sem dados estruturados em {url}")
            
            return len(dados)
            
        except Exception as e:
            print(f"      ❌ Erro: {str(e)[:80]}")
            return 0
    
    def processar_orgao(self, orgao):
        print(f"\n{'='*70}")
        print(f"🏢 [{orgao['sigla']}] {orgao['nome']}")
        print(f"{'='*70}")
        
        try:
            links = self.mapear_links(orgao['url'], orgao['sigla'])
            
            if not links:
                links = [{'texto': 'Página Principal', 'url': orgao['url'], 'score': 0}]
            
            total = 0
            for idx, link in enumerate(links[:5], 1):
                print(f"\n   [{idx}/5] {link['texto'][:60]}")
                contatos = self.extrair_dados_pagina(link['url'], orgao['nome'], orgao['sigla'])
                total += contatos
                time.sleep(1)
                
                if total >= 5:
                    print(f"   ✓ Dados suficientes")
                    break
            
            print(f"\n   ✅ Total: {total} contato(s)")
            
        except Exception as e:
            print(f"\n   ❌ Erro: {str(e)[:100]}")
    
    def salvar_excel(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"contatos_v2_refatorado_{timestamp}.xlsx"
        
        with pd.ExcelWriter(nome_arquivo, engine='openpyxl') as writer:
            if self.dados_coletados:
                df = pd.DataFrame(self.dados_coletados)
                df = df.drop_duplicates()
                df.to_excel(writer, index=False, sheet_name='Contatos TI')
                
                worksheet = writer.sheets['Contatos TI']
                for idx, col in enumerate(df.columns):
                    max_length = max(df[col].astype(str).apply(len).max(), len(col)) + 2
                    worksheet.column_dimensions[chr(65 + idx)].width = min(max_length, 50)
            
            if self.log_processamento:
                df_log = pd.DataFrame(self.log_processamento)
                df_log.to_excel(writer, index=False, sheet_name='Log')
        
        print(f"\n{'='*70}")
        print(f"💾 Arquivo: {nome_arquivo}")
        if self.dados_coletados:
            df = pd.DataFrame(self.dados_coletados)
            print(f"📊 Registros: {len(df)}")
            print(f"👤 Com nome: {df[df['Nome da Pessoa'] != '-'].shape[0]}")
            print(f"📧 Com email: {df[df['E-mail'] != ''].shape[0]}")
            print(f"📞 Com telefone: {df[df['Telefone'] != ''].shape[0]}")
        print(f"{'='*70}")
        
        return nome_arquivo
    
    def executar(self):
        print("\n" + "="*70)
        print("🚀 SCRAPER V2 REFATORADO")
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

def main():
    try:
        scraper = ScraperV2(headless=False)
        scraper.executar()
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}")

if __name__ == "__main__":
    main()

# Made with Bob
