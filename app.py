from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB_PATH = 'chatbot_saude.db'  # Certifique-se que o banco está na mesma pasta do app.py

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods=['GET', 'POST'])
def pagina1():
    if request.method == 'POST':
        id_paciente = request.form['id_paciente']
        conn = get_db_connection()
        paciente = conn.execute("SELECT * FROM paciente WHERE id_paciente = ?", (id_paciente,)).fetchone()
        conn.close()
        if paciente:
            return redirect(url_for('pagina2', id_paciente=id_paciente))
        else:
            return "Paciente não encontrado", 404
    return render_template('pagina1.html')

@app.route('/pagina2/<int:id_paciente>')
def pagina2(id_paciente):
    conn = get_db_connection()
    paciente = conn.execute("SELECT * FROM paciente WHERE id_paciente = ?", (id_paciente,)).fetchone()
    triagens = conn.execute("SELECT * FROM triagem WHERE id_paciente = ?", (id_paciente,)).fetchall()
    historico = conn.execute("SELECT * FROM historico_medico WHERE id_paciente = ?", (id_paciente,)).fetchone()
    conn.close()
    return render_template('pagina2.html', paciente=paciente, triagens=triagens, historico=historico)

@app.route('/pagina3/<int:id_paciente>', methods=['GET', 'POST'])
def pagina3(id_paciente):
    conn = get_db_connection()
    paciente = conn.execute("SELECT * FROM paciente WHERE id_paciente = ?", (id_paciente,)).fetchone()

    # PARA COLOCAR AS APIS
    ubs_proximas = [
        {"id": 1, "nome": "UBS Centro", "endereco": "Rua A, 123"},
        {"id": 2, "nome": "UBS Bairro", "endereco": "Rua B, 456"}
    ]

    if request.method == 'POST':
        ubs_nome = request.form['ubs']
        conn.execute("UPDATE triagem SET status_encaminhamento='agendado' WHERE id_paciente=?", (id_paciente,))
        conn.commit()
        conn.close()
        return f"Consulta marcada na UBS {ubs_nome}!"

    conn.close()
    return render_template('pagina3.html', paciente=paciente, ubs_proximas=ubs_proximas)

if __name__ == "__main__":
    app.run(debug=True)
