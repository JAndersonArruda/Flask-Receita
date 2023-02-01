import hashlib
# from app import db

# nos models
class Usuarios(db.Model):
    
    # ...
    def __init__(self, nome, username, senha) -> None:
        self.nome = nome
        self.username = username
        self.senha = hashlib.sha256(senha.encode()).hexdigest()
        
    
    @staticmethod
    def create(nome, username, senha):
        senha_criptografada = hashlib.sha256(senha.encode()).hexdigest()
        new_user = Usuarios(nome, username, senha_criptografada)
        db.session.add(new_user)
        db.session.commit()
        


# nas views para descriptografar
# necessario importar o hashlib também

# No método create, adicione a seguinte linha:
self.senha = hashlib.sha256(senha.encode()).hexdigest()

# No método autenticar, adicione as seguintes linhas:
senha = hashlib.sha256(form_User.senha.data.encode()).hexdigest()
if form_User.senha.data == usuario.senha:
    ...