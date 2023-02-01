from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, validators


class FormularioNewReceita(FlaskForm):
    nome = StringField('Nome', [validators.DataRequired(), validators.Length(min=1, max=90)]) #colocar os dados do de acracteres dos models
    ingrediente = TextAreaField('Ingrediente', [validators.DataRequired(), validators.Length(min=1, max=500)])
    modo_preparo = TextAreaField('Modo de Preparo', [validators.DataRequired(), validators.Length(min=1, max=1000)])
    autor = StringField('Autor', [validators.DataRequired(), validators.Length(min=1, max=90)])
    
    salvar = SubmitField('Salvar')
    
    
class FormularioUsuario(FlaskForm):
    username = StringField('Nome de usuário', [validators.DataRequired(), validators.Length(min=1, max=30)])
    senha = PasswordField('Senha', [validators.DataRequired(), validators.Length(min=1, max=30)])
    
    login = SubmitField('Entrar')
