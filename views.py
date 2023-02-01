from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from app import app, db
from models import Receitas, Usuarios
import os

from helpers import FormularioNewReceita, FormularioUsuario

@app.route('/')
def home():
    lista = Receitas.query.order_by(Receitas.id)
    
    user_instance = Usuarios
    usuario = user_instance.username
    
    capa_receita = recupera_imagem(Receitas.id)
    return render_template('home.html', titulo='Receitas', receitas=lista, capa=capa_receita, usuario=usuario)

@app.route('/cadastro')
def cadastro():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('cadastro')))
    
    form = FormularioNewReceita()
    return render_template('cadastro.html', titulo='Add Receitas', form=form)

@app.route('/criar', methods=['POST',])
def criar():
    form = FormularioNewReceita(request.form)
    
    if not form.validate_on_submit():
        return redirect(url_for('cadastro'))
    
    nome = form.nome.data
    ingrediente = form.ingrediente.data
    modo_preparo = form.modo_preparo.data
    autor = form.autor.data

    receita = Receitas.query.filter_by(nome=nome).first()

    if receita:
        flash(f'A Receita de {nome} já existe em nossa platafomar! Caso haja alguma mudança na receita, tente edita-lá.')
        return redirect(url_for('home'))

    nova_receita = Receitas(nome=nome, ingrediente=ingrediente, modo_preparo=modo_preparo, autor=autor)

    db.session.add(nova_receita)
    db.session.commit()

    capa = request.files['capa']
    upload_path = app.config['UPLOAD_PATH']
    capa.save(f'{upload_path}/capa{nova_receita.id}.jpg')

    flash(f'A Receita de {nome} adicionada com sucesso!')
    return redirect(url_for('home'))

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar')))
    receita = Receitas.query.filter_by(id=id).first()
    capa_receita = recupera_imagem(id)
    print(receita)
    return render_template('editar.html', titulo='Editar Receita', receita=receita, capa=capa_receita)

@app.route('/atualizar', methods=['POST',])
def atualizar():
    receita = Receitas.query.filter_by(id=request.form['id']).first()
    receita.nome = request.form['nome']
    receita.ingrediente = request.form['ingrediente']
    receita.modo_preparo = request.form['modo_preparo']
    receita.autor = request.form['autor']

    db.session.add(receita)
    db.session.commit()

    capa = request.files['capa']
    upload_path = app.config['UPLOAD_PATH']
    deleta_arquivo(id=receita.id)
    capa.save(f'{upload_path}/capa{receita.id}.jpg')

    flash(f'A receita de {receita.nome} foi atualizada com sucesso!')
    return redirect(url_for('home'))

@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    
    Receitas.query.filter_by(id=id).delete()
    db.session.commit()
    flash(f'A receita foi deletada com sucesso!')
    deleta_arquivo(id) # funcção para deletar o os uploads

    return redirect(url_for('home'))


@app.route('/deletar/<int:id>', methods=['POST'])
def deletar_confirm(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    
    if request.form.get('confirm') == 'Confirmar':
        Receitas.query.filter_by(id=id).delete()
        db.session.commit()
        flash(f'A receita foi deletada com sucesso!')
        deleta_arquivo(id) # funcção para deletar o os uploads

    return redirect(url_for('home'))
'''
'''

@app.route('/visualizar/<int:id>')
def visualizar(id):
    receita = Receitas.query.filter_by(id=id).first()
    ingredientes = receita.ingrediente
    modo_de_preparo = receita.modo_preparo
    capa_receita = recupera_imagem(id)
    return render_template('receita.html', receita=receita, ingredientes=ingredientes.split("\n"), modo_de_preparo=modo_de_preparo.split("\n"), capa=capa_receita)

@app.route('/login')
def login():
    form_User = FormularioUsuario()
    
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima, titulo='SigIn', form=form_User)

@app.route('/autenticar', methods=['POST',])
def autenticar():
    form_User = FormularioUsuario(request.form)
    
    usuario = Usuarios.query.filter_by(username=form_User.username.data).first()
    if usuario:
        if form_User.senha.data == usuario.senha:
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
    flash('SingUt efetuado com sucesso!')
    return redirect(url_for('home'))

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)

def recupera_imagem(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f"capa{id}" in nome_arquivo:
            return nome_arquivo
        
    return "receita.jpg"

def deleta_arquivo(id):
    arquivo = recupera_imagem(id)
    print(arquivo)
    if arquivo != 'receita.jpg':
        os.remove(os.path.join(app.config['UPLOAD_PATH'], arquivo))

