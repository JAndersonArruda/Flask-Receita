from app import db


class Receitas(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(90), nullable=False)
    ingrediente = db.Column(db.String(500), nullable=False)
    modo_preparo = db.Column(db.String(1000), nullable=False)
    autor = db.Column(db.String(90), nullable=False)

    def __repr__(self):
        return "<Name %r>" % self.nome


class Usuarios(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(90), nullable=False)
    username = db.Column(db.String(30), nullable=False)
    senha = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return "<Name %r>" % self.nome
    
    def __init__(self, nome, username, senha) -> None:
        self.nome = nome
        self.username = username
        self.senha = senha
        
    @staticmethod
    def create(nome, username, senha):
        new_user = Usuarios(nome, username, senha)
        db.session.add(new_user)
        db.session.commit()
        
        
def adiciona_usuario_adm():
    nome = "Anderson Arruda"
    username = "anderson"
    senha = "123adm123"
    Usuarios.create(nome, username, senha)

# Adicionando o usuário adm antes de iniciar a aplicação
adiciona_usuario_adm()