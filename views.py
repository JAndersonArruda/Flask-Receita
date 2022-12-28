from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from app import app, db
from models import Livros, Usuarios
import os
import time

@app.route('/')
def home():
    lista = Livros.query.order_by(Livros.id)
    return render_template('lista.html', titulo='Livros', livros=lista)

@app.route('/cadastro')
def cadastro():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('cadastro')))
    return render_template('cadastro.html', titulo='Novo Livro')

@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    genero = request.form['genero']
    autor = request.form['autor']
    num_paginas = request.form['num_paginas']

    livro = Livros.query.filter_by(nome=nome).first()

    if livro:
        flash('Livro já existente!')
        return redirect(url_for('home'))

    novo_livro = Livros(nome=nome, genero=genero, autor=autor, num_paginas=num_paginas)

    db.session.add(novo_livro)
    db.session.commit()

    capa = request.files['capa']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    capa.save(f'{upload_path}/capa{novo_livro.id}-{timestamp}.jpg')

    flash('Livro criado com sucesso!')
    return redirect(url_for('home'))

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar')))
    livro = Livros.query.filter_by(id=id).first()
    print(livro)
    return render_template('editar.html', titulo='Editar Livro', livro=livro)

@app.route('/atualizar', methods=['POST',])
def atualizar():
    livro = Livros.query.filter_by(id=request.form['id']).first()
    livro.nome = request.form['nome']
    livro.genero = request.form['genero']
    livro.autor = request.form['autor']
    livro.num_paginas = request.form['num_paginas']

    db.session.add(livro)
    db.session.commit()

    capa = request.files['capa']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    deleta_arquivo(livro.id)
    capa.save(f'{upload_path}/capa{livro.id}-{timestamp}.jpg')

    flash('Livro atualizado com sucesso!')
    return redirect(url_for('home'))

@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))

    Livros.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Livro deletado com sucesso!')

    return redirect(url_for('home'))

@app.route('/visualizar/<int:id>')
def visualizar(id):
    livro = Livros.query.filter_by(id=id).first()
    capa_livro = recupera_imagem(id)
    return render_template('livro.html', livro=livro, capa=capa_livro)

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima, titulo='Login')

@app.route('/autenticar', methods=['POST',])
def autenticar():
    usuario = Usuarios.query.filter_by(username=request.form['usuario']).first()
    if usuario:
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.username
            flash(usuario.username + ' logado com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
        else:
            flash('Usuário não logado com sucesso!')
            return redirect(url_for('login'))
    else:
        flash('Usuário não logado com sucesso!')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('home'))

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)

def recupera_imagem(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'capa{id}' in nome_arquivo:
            return nome_arquivo

    return 'receita.jpg'

def deleta_arquivo(id):
    arquivo = recupera_imagem(id)
    print(arquivo)
    if arquivo != 'livro.png':
        os.remove(os.path.join(app.config['UPLOAD_PATH'], arquivo))
