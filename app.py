from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from math import radians, cos, sin, sqrt, atan2

app = Flask(__name__)
app.secret_key = "senha_super_secreta"

DB_PATH_PACIENTE = r"chatbot_saude.db"
DB_PATH_UBS = r"ubs_sp.db"

def get_db_connection(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1))*cos(radians(lat2))*sin(dlon/2)**2
    c = 2*atan2(sqrt(a), sqrt(1-a))
    return R*c

def ubs_mais_proximas(lat_paciente, lon_paciente, limite=5):
    conn = get_db_connection(DB_PATH_UBS)
    ubs_lista = conn.execute("SELECT * FROM ubs").fetchall()
    conn.close()
    ubs_dist = []
    for u in ubs_lista:
        if u['LAT'] and u['LONG']:
            dist = haversine(lat_paciente, lon_paciente, u['LAT'], u['LONG'])
            ubs_dist.append((dist, dict(u)))
    ubs_dist.sort(key=lambda x: x[0])
    return [u[1] for u in ubs_dist[:limite]]
@app.route('/', methods=['GET', 'POST'])
def login():
    erro = None
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
        if usuario == 'unisa' and senha == '1234':
            session['logado'] = True
            return redirect(url_for('buscar_paciente'))
        else:
            erro = "Usuário ou senha incorretos!"
    return render_template('login.html', erro=erro)

@app.route('/pagina2', methods=['GET', 'POST'])
def buscar_paciente():
    if not session.get('logado'):
        return redirect(url_for('login'))
    erro = None
    if request.method == 'POST':
        id_paciente = request.form['id_paciente']
        conn = get_db_connection(DB_PATH_PACIENTE)
        paciente = conn.execute("SELECT * FROM paciente WHERE id_paciente=?", (id_paciente,)).fetchone()
        triagem = conn.execute("SELECT * FROM triagem WHERE id_paciente=?", (id_paciente,)).fetchone()
        conn.close()
        if paciente and triagem:
            sintomas = triagem['resumo_sintomas'] or "Nenhum sintoma registrado"
            lat = triagem['lat'] if 'lat' in triagem.keys() else -23.659
            lon = triagem['lon'] if 'lon' in triagem.keys() else -46.713
            session['id_paciente'] = id_paciente
            session['paciente_nome'] = paciente['nome_completo']
            session['lat'] = lat
            session['lon'] = lon
            return render_template('pagina3.html', paciente=paciente, sintomas=sintomas)
        else:
            erro = "Paciente não encontrado!"
    return render_template('pagina2.html', erro=erro)

@app.route('/escolher_ubs', methods=['GET', 'POST'])
def escolher_ubs():
    if not session.get('logado'):
        return redirect(url_for('login'))
    lat = session.get('lat')
    lon = session.get('lon')
    paciente_nome = session.get('paciente_nome')
    ubs_proximas = ubs_mais_proximas(lat, lon)
    erro = None
    if request.method == 'POST':
        ubs_selecionada = request.form.get('ubs')
        if not ubs_selecionada:
            erro = "Selecione uma UBS antes de confirmar!"
        else:
            return render_template('confirmacao.html', paciente_nome=paciente_nome, ubs_nome=ubs_selecionada)
    return render_template('escolher_ubs.html', ubs_proximas=ubs_proximas, paciente={'nome_completo': paciente_nome}, erro=erro)

if __name__ == "__main__":
    app.run(debug=True)
