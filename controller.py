from curses import echo
from model import Pessoa, Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import hashlib

def retorna_session():
    CONN = "sqlite:///projeto2.db"
    engine = create_engine(CONN, echo=True)
    Session = sessionmaker(bind=engine)
    return Session()


class ControllerCadastro():
    @classmethod
    def verifica_dados(cls, nome, email, senha ):
        if len(nome) > 50 or len(nome) < 3:
            return 2
        if len(email) > 200:
            return 3
        if len(senha) > 100 or len(senha) < 6:
            return 4
        
        return 1

    @classmethod
    def cadastrar(cls, nome, email, senha):
        session = retorna_session()
        usuario = session.query(Pessoa).filter(Pessoa.email == email).all()
        
        if len(usuario) > 0:
            return 5
        
        dados_verificados = cls.verifica_dados(nome, email, senha)

        if dados_verificados != 1:
            return dados_verificados
        
        try:
            senha = (hashlib.sha256(senha.encode()).hexdigest())
            p1 = Pessoa(nome=nome, email=email, senha=senha)
            session.add(p1)
            session.commit()
            return 1
        except:
            return 6

#ControllerCadastro.cadastrar('Flavio Siqueira', 'alexandred@alex.com', 'Alex123456')

class ControllerLogin():
    @classmethod
    def login(cls, email, senha):
        session = retorna_session()
        senha =  (hashlib.sha256(senha.encode()).hexdigest())
        logado = session.query(Pessoa).filter(Pessoa.email == email).filter(Pessoa.senha==senha).all()
        #Abre sessão busca na tabela pessoa, e filtra o email for igual ao email recebido por parâmetro e .all traz tudo
        if len(logado) == 1:
            return {'logado': True, 'id': logado[0].id}
        else:
            return False

#print(ControllerCadastro.cadastrar('Alex', 'meuemail@gmail.com', 'minhasenha'))
#print(ControllerLogin.login('meuemail@gmail.com', 'minhasenha'))


