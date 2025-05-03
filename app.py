from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from dotenv import load_dotenv
import pymysql
import os
import bleach
from flask_session import Session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect
import bcrypt
import logging

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")  # Secret key for sessions

# Logging configuration
logging.basicConfig(level=logging.INFO)
app.logger.info("Application initialized successfully!")

# CSRF protection
csrf = CSRFProtect(app)

# Rate limiting
limiter = Limiter(get_remote_address, app=app, default_limits=["5 per minute"])

# Session configuration
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Database connection function
def conectar_bd():
    return pymysql.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "sua_senha"),
        database=os.getenv("DB_NAME", "torneio"),
        cursorclass=pymysql.cursors.DictCursor
    )

# Utility functions
def is_admin():
    return "usuario" in session and session.get("tipo") == "administrador"

# Routes
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]

        conn = conectar_bd()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM usuarios WHERE usuario=%s", (usuario,))
            user = cursor.fetchone()
        conn.close()

        if user and bcrypt.checkpw(senha.encode('utf-8'), user["senha"].encode('utf-8')):
            session["usuario"] = usuario
            session["tipo"] = user.get("tipo", "usuario")
            return redirect(url_for("home"))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("usuario", None)
    session.pop("tipo", None)
    return redirect(url_for("home"))

@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]

        # Hash the password
        senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())

        conn = conectar_bd()
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES (%s, %s)", (usuario, senha_hash))
            conn.commit()
        conn.close()
        return redirect(url_for("login"))
    return render_template("registro.html")

@app.route("/registro_admin", methods=["GET", "POST"])
def registro_admin():
    if not is_admin():
        return redirect(url_for("login"))

    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]

        # Hash the password
        senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())

        conn = conectar_bd()
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO usuarios (usuario, senha, tipo) VALUES (%s, %s, 'administrador')",
                (usuario, senha_hash)
            )
            conn.commit()
        conn.close()
        return redirect(url_for("home"))
    return render_template("registro_admin.html")

@app.route("/gerenciar_usuarios", methods=["GET", "POST"])
def gerenciar_usuarios():
    if not is_admin():
        return redirect(url_for("login"))

    conn = conectar_bd()
    with conn.cursor() as cursor:
        cursor.execute("SELECT id, usuario, tipo FROM usuarios")
        usuarios = cursor.fetchall()
    conn.close()
    return render_template("gerenciar_usuarios.html", usuarios=usuarios)

@app.route("/alterar_usuario", methods=["POST"])
def alterar_usuario():
    if not is_admin():
        return redirect(url_for("login"))

    usuario_id = request.form["usuario_id"]
    novo_tipo = request.form["tipo"]

    conn = conectar_bd()
    with conn.cursor() as cursor:
        cursor.execute("UPDATE usuarios SET tipo=%s WHERE id=%s", (novo_tipo, usuario_id))
        conn.commit()
    conn.close()

    return redirect(url_for("gerenciar_usuarios"))

@app.route("/excluir_usuario", methods=["POST"])
def excluir_usuario():
    if not is_admin():
        return redirect(url_for("login"))

    usuario_id = request.form["usuario_id"]

    conn = conectar_bd()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM usuarios WHERE id=%s", (usuario_id,))
        conn.commit()
    conn.close()

    return redirect(url_for("gerenciar_usuarios"))

@app.route("/partidas")
def partidas():
    conn = conectar_bd()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM partidas ORDER BY horario ASC")
        partidas = cursor.fetchall()
    conn.close()
    return render_template("partidas.html", partidas=partidas)

@app.route("/adicionar_partida", methods=["GET", "POST"])
def adicionar_partida():
    if request.method == "POST":
        categoria = request.form["categoria"]
        jogador1 = request.form["jogador1"]
        jogador2 = request.form["jogador2"]
        horario = request.form["horario"]
        resultado = request.form["resultado"]

        conn = conectar_bd()
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO partidas (categoria, jogador1, jogador2, horario, resultado) VALUES (%s, %s, %s, %s, %s)",
                (categoria, jogador1, jogador2, horario, resultado)
            )
            conn.commit()
        conn.close()
        return redirect(url_for("partidas"))
    return render_template("adicionar_partida.html")

@app.route("/classificacao")
def classificacao():
    categoria = request.args.get("categoria", "Simples Masculino")
    conn = conectar_bd()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM classificacao WHERE categoria=%s ORDER BY pontos DESC", (categoria,))
        classificacao = cursor.fetchall()
    conn.close()
    return render_template("classificacao.html", classificacao=classificacao, categoria=categoria)

@app.route("/comentarios", methods=["GET", "POST"])
def comentarios():
    if request.method == "POST":
        usuario = session.get("usuario", "Anônimo")
        comentario = bleach.clean(request.form["comentario"])

        conn = conectar_bd()
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO comentarios (usuario, comentario) VALUES (%s, %s)", (usuario, comentario))
            conn.commit()
        conn.close()

    conn = conectar_bd()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM comentarios")
        comentarios = cursor.fetchall()
    conn.close()
    return render_template("comentarios.html", comentarios=comentarios)

@app.route("/notificacoes")
def notificacoes():
    conn = conectar_bd()
    with conn.cursor() as cursor:
        cursor.execute("SELECT nome, data, descricao FROM eventos WHERE data >= CURDATE() ORDER BY data ASC")
        eventos = cursor.fetchall()
    conn.close()
    return jsonify(eventos)

@app.route("/galeria")
def galeria():
    conn = conectar_bd()
    with conn.cursor() as cursor:
        cursor.execute("SELECT categoria, nome, foto_url, video_url FROM melhores_do_ano")
        midias = cursor.fetchall()
    conn.close()
    return render_template("galeria.html", midias=midias)

@app.route("/dados_graficos")
def dados_graficos():
    conn = conectar_bd()
    with conn.cursor() as cursor:
        cursor.execute("SELECT jogador, pontos FROM classificacao ORDER BY pontos DESC")
        classificacao = cursor.fetchall()

        cursor.execute("SELECT categoria, COUNT(*) AS total FROM partidas GROUP BY categoria")
        partidas_por_categoria = cursor.fetchall()
    conn.close()
    return jsonify({"classificacao": classificacao, "historico": partidas_por_categoria})

@app.route("/historia")
def historia():
    return render_template("historia.html")

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
