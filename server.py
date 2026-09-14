from flask import Flask, request, send_file, send_from_directory
import qrcode, io, socket, os

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def obter_ip_local():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # não envia dados de verdade, só usa a tabela de rotas
        # para descobrir qual interface seria usada
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

palavras = []
proximo_id = 1

#QRcode
@app.route('/qrcode.png')

def qrcode_png():
    ip = obter_ip_local()
    url = f"http://{ip}:5000/"
    img = qrcode.make(url)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

#Formulário
@app.route('/')
def pagina_enviar():
    return send_from_directory(BASE_DIR, 'enviar.html')

@app.route('/enviar', methods=['POST'])
def enviar():
    global proximo_id
    dados = request.get_json()
    texto = (dados.get('texto') or '').strip()
    if not texto:
        return {'erro': 'texto vazio'}, 400
    palavras.append({'id': proximo_id, 'texto': texto})
    proximo_id += 1
    return {'ok': True}, 200

#Projeção
@app.route('/projecao')
def pagina_projecao():
    if request.method == 'GET':
        since = request.args.get('since', 0, type=int)
        novas = [p for p in palavras if p['id'] > since]
        return send_from_directory(BASE_DIR, 'projecao.html')
    return send_from_directory(BASE_DIR, 'projecao.html')

@app.route('/palavras')
def listar_palavras():
    since = request.args.get('since', 0, type=int)
    novas = [p for p in palavras if p['id'] > since]
    return novas

@app.route('/limpar', methods=['POST'])
def limpar():
    palavras.clear()
    return {'ok': True}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)