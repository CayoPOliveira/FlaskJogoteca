from flask import Flask, render_template, request, redirect, session, flash, url_for


class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console


jogo1 = Jogo('Tetris', 'Puzzle', 'Ataria')
jogo2 = Jogo('God of War', 'Rack n Slash', 'PS2')
jogo3 = Jogo('Mortal Kombat', 'Luta', 'PS2')
jogos = [jogo1, jogo2, jogo3]


class Usuario:
    def __init__(self, nome, nickname, senha):
        self.nome = nome
        self.nickname = nickname
        self.senha = senha


usuario1 = Usuario("Bruno Divino", "BD", "alohomora")
usuario2 = Usuario("Camila Ferreira", "Mila", "paozinho")
usuario3 = Usuario("Guilherme Louro", "Cake", "Python_eh_vida")

usuarios = {
    usuario1.nickname: usuario1,
    usuario2.nickname: usuario2,
    usuario3.nickname: usuario3
}

app = Flask(__name__)
app.secret_key = 'chavesecreta'


@app.route("/")
def inicio():
    return render_template('lista.html', titulo='Jogos', jogos=jogos)


@app.route("/novo")
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novojogo.html', titulo='Novo Jogo')


@app.route("/criar", methods=['POST', ])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    jogos.append(jogo)
    return app.redirect(url_for('inicio'))


@app.route("/login")
def login():
    proxima = request.args.get('proxima')
    return render_template("login.html", proxima=proxima)


@app.route("/autenticar", methods=['POST', ])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(f'{usuario.nickname.capitalize()} foi logado com sucesso!')
            proxima_pagina = request.form['proxima']
            if proxima_pagina[-5:] == "None":
                return redirect(url_for("inicio"))
            return redirect(proxima_pagina)
    else:
        flash(f"Usuário e/ou Senha inválido(s)")

        return app.redirect(url_for('login'))


@app.route("/logout")
def logout():
    session['usuario_logado'] = None
    flash("Logout efetuado!")
    return app.redirect(url_for('inicio'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
