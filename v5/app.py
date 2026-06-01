"""
Web Interface para Scraper V5 AI-Powered
Interface web para upload de orgaos.txt e acompanhamento em tempo real
"""

from flask import Flask, render_template, request, jsonify, send_file, session
from flask_socketio import SocketIO, emit
import os
import threading
import time
from datetime import datetime
from werkzeug.utils import secure_filename
import uuid

# Importar scraper
from scraper_v5_ai import ScraperV5AI

app = Flask(__name__)
app.config['SECRET_KEY'] = 'scraper-v5-secret-key-2026'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

socketio = SocketIO(app, cors_allowed_origins="*")

# Criar pasta de uploads
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Armazenar status das execuções
execucoes = {}

class ScraperThread(threading.Thread):
    """Thread para executar scraper em background"""
    
    def __init__(self, execution_id, orgaos_file):
        threading.Thread.__init__(self)
        self.execution_id = execution_id
        self.orgaos_file = orgaos_file
        self.daemon = True
        
    def run(self):
        """Executa o scraper"""
        try:
            # Atualizar status
            execucoes[self.execution_id]['status'] = 'running'
            execucoes[self.execution_id]['start_time'] = datetime.now().isoformat()
            
            socketio.emit('status_update', {
                'execution_id': self.execution_id,
                'status': 'running',
                'message': 'Iniciando scraper...'
            })
            
            # Criar scraper customizado que emite eventos
            scraper = ScraperV5AIWeb(self.execution_id, self.orgaos_file)
            scraper.executar()
            
            # Atualizar status final
            execucoes[self.execution_id]['status'] = 'completed'
            execucoes[self.execution_id]['end_time'] = datetime.now().isoformat()
            execucoes[self.execution_id]['excel_file'] = scraper.excel_file
            
            socketio.emit('status_update', {
                'execution_id': self.execution_id,
                'status': 'completed',
                'message': 'Scraper concluído!',
                'excel_file': scraper.excel_file
            })
            
        except Exception as e:
            execucoes[self.execution_id]['status'] = 'error'
            execucoes[self.execution_id]['error'] = str(e)
            
            socketio.emit('status_update', {
                'execution_id': self.execution_id,
                'status': 'error',
                'message': f'Erro: {str(e)}'
            })


class ScraperV5AIWeb(ScraperV5AI):
    """Versão do scraper que emite eventos para web"""
    
    def __init__(self, execution_id, orgaos_file):
        # Temporariamente copiar arquivo para orgaos.txt
        import shutil
        shutil.copy(orgaos_file, 'orgaos.txt')
        
        super().__init__(headless=True)
        self.execution_id = execution_id
        self.excel_file = None
        
    def processar_orgao(self, orgao):
        """Override para emitir eventos"""
        # Emitir evento de início
        socketio.emit('orgao_update', {
            'execution_id': self.execution_id,
            'orgao': orgao['sigla'],
            'status': 'processing',
            'message': f"Processando {orgao['nome']}..."
        })
        
        # Processar normalmente
        super().processar_orgao(orgao)
        
        # Emitir evento de conclusão
        socketio.emit('orgao_update', {
            'execution_id': self.execution_id,
            'orgao': orgao['sigla'],
            'status': 'completed',
            'message': f"{orgao['sigla']} concluído"
        })
    
    def salvar_excel(self):
        """Override para salvar arquivo"""
        filename = super().salvar_excel()
        self.excel_file = filename
        return filename


@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    """Upload do arquivo orgaos.txt"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Nenhum arquivo enviado'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
        
        if not file.filename.endswith('.txt'):
            return jsonify({'error': 'Apenas arquivos .txt são permitidos'}), 400
        
        # Salvar arquivo
        execution_id = str(uuid.uuid4())
        filename = secure_filename(f"{execution_id}_orgaos.txt")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Validar arquivo
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]
                orgaos_count = len([l for l in lines if '|' in l])
                
                if orgaos_count == 0:
                    os.remove(filepath)
                    return jsonify({'error': 'Arquivo não contém órgãos válidos'}), 400
        except Exception as e:
            os.remove(filepath)
            return jsonify({'error': f'Erro ao ler arquivo: {str(e)}'}), 400
        
        # Criar execução
        execucoes[execution_id] = {
            'id': execution_id,
            'filename': file.filename,
            'filepath': filepath,
            'orgaos_count': orgaos_count,
            'status': 'pending',
            'created_at': datetime.now().isoformat()
        }
        
        return jsonify({
            'execution_id': execution_id,
            'orgaos_count': orgaos_count,
            'message': f'{orgaos_count} órgãos encontrados'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/start/<execution_id>', methods=['POST'])
def start_execution(execution_id):
    """Inicia a execução do scraper"""
    try:
        if execution_id not in execucoes:
            return jsonify({'error': 'Execução não encontrada'}), 404
        
        if execucoes[execution_id]['status'] != 'pending':
            return jsonify({'error': 'Execução já iniciada'}), 400
        
        # Iniciar thread
        thread = ScraperThread(execution_id, execucoes[execution_id]['filepath'])
        thread.start()
        
        return jsonify({
            'execution_id': execution_id,
            'status': 'started',
            'message': 'Scraper iniciado'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/status/<execution_id>')
def get_status(execution_id):
    """Retorna status da execução"""
    if execution_id not in execucoes:
        return jsonify({'error': 'Execução não encontrada'}), 404
    
    return jsonify(execucoes[execution_id])


@app.route('/download/<execution_id>')
def download_file(execution_id):
    """Download do arquivo Excel"""
    try:
        if execution_id not in execucoes:
            return jsonify({'error': 'Execução não encontrada'}), 404
        
        if execucoes[execution_id]['status'] != 'completed':
            return jsonify({'error': 'Execução não concluída'}), 400
        
        excel_file = execucoes[execution_id].get('excel_file')
        if not excel_file or not os.path.exists(excel_file):
            return jsonify({'error': 'Arquivo não encontrado'}), 404
        
        return send_file(
            excel_file,
            as_attachment=True,
            download_name=f"contatos_{execution_id[:8]}.xlsx"
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@socketio.on('connect')
def handle_connect():
    """Cliente conectado"""
    print('Cliente conectado')
    emit('connected', {'message': 'Conectado ao servidor'})


@socketio.on('disconnect')
def handle_disconnect():
    """Cliente desconectado"""
    print('Cliente desconectado')


if __name__ == '__main__':
    print("="*70)
    print("🌐 SCRAPER V5 - WEB INTERFACE")
    print("="*70)
    print()
    print("Acesse: http://localhost:5000")
    print()
    print("Pressione Ctrl+C para parar")
    print("="*70)
    
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)

# Made with Bob
