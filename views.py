from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from app import app, db
from models import Receitas, Usuarios
import os
import time

@app.route('/')
def home():
    lista = Receitas.query.order_by(Receitas.id)
    return render_template('lista.html', titulo='Receitas', receitas=lista)

@app.route('/cadastro')
def cadastro():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('cadastro')))
    return render_template('cadastro.html', titulo='Adicionar Receita')

@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    genero = request.form['genero']
    autor = request.form['autor']
    num_paginas = request.form['num_paginas']

    receita = Receitas.query.filter_by(nome=nome).first()

    if receita:
        flash(f'A Receita de {nome} já existe em nossa platafomar! Caso haja alguma mudança na receita, tente edita-lá.')
        return redirect(url_for('home'))

    nova_receita = Receitas(nome=nome, genero=genero, autor=autor, num_paginas=num_paginas)

    db.session.add(nova_receita)
    db.session.commit()

    capa = request.files['capa']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    capa.save(f'{upload_path}/capa{nova_receita.id}-{timestamp}.jpg')

    flash(f'A Receita de {nome} adicionada com sucesso!')
    return redirect(url_for('home'))

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar')))
    receita = Receitas.query.filter_by(id=id).first()
    print(receita)
    return render_template('editar.html', titulo='Editar Receita', receita=receita)

@app.route('/atualizar', methods=['POST',])
def atualizar():
    receita = Receitas.query.filter_by(id=request.form['id']).first()
    receita.nome = request.form['nome']
    receita.genero = request.form['genero']
    receita.autor = request.form['autor']
    receita.num_paginas = request.form['num_paginas']

    db.session.add(receita)
    db.session.commit()

    capa = request.files['capa']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    deleta_arquivo(receita.id)
    capa.save(f'{upload_path}/capa{receita.id}-{timestamp}.jpg')

    flash(f'A receita de {receita.nome} foi atualizada com sucesso!')
    return redirect(url_for('home'))

@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    Receitas.query.filter_by(id=id).delete()
    db.session.commit()
    flash(f'A receita foi deletada com sucesso!')

    return redirect(url_for('home'))

@app.route('/visualizar/<int:id>')
def visualizar(id):
    receita = Receitas.query.filter_by(id=id).first()
    capa_receita = recupera_imagem(id)
    return render_template('receita.html', receita=receita, capa=capa_receita)

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima, titulo='SigIn')

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
    flash('SigUt efetuado com sucesso!')
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
    if arquivo != 'receita.png':
        os.remove(os.path.join(app.config['UPLOAD_PATH'], arquivo))
