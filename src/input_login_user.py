from cryptography.fernet import Fernet
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from user import User, Base
from dotenv import load_dotenv

import os

def create():
    engine = create_engine("sqlite://user.db")
    return engine

# Inicialização do banco de dados
def setup():
    # Criando a base do banco de dados e o própio    
    
    engine = create()
    Base.metadata.create_all(engine)
    
    return engine    

def generate_cipher():
    key = Fernet().generate_key()
    cipher = Fernet(key)

    return cipher

# Função para definir o e-mail de usuário
def set_user_(email=None):
    """ 
    Esta função faz o setup do e-mail do usuário
    toda a informação sensível é criptografada e 
    está segura de pessoas maliciosas.

    Args:
        email (string): o email do usuário
    """
    
    cipher = generate_cipher()
    
    if email:
        # Criptografando o email
        encrypted_email = cipher.encrypt(email.encode())

        # Gravando nas variáveis de ambiente
        with open('.env', 'w') as file:
            file.write(f"EMAIL_KEYWORD={encrypted_email.decode()}\n")
            file.write(f"FERNET_KEY={key.decode()}")

    return cipher


# Função para acessar contas de qualquer site de maneira segura e confiável
def set_acess_account(plataform, password, cipher):
    """
    Adiciona as contas de qualquer site, usando criptografia e protegendo os
    seus dados em um banco de dados local do seu computador.

    Args:
        password (string): a senha para entrar no site
    """

    engine = create()

    # Encriptando a senha
    encrypted_key_password = cipher.encrypt(password.encode())
    
    # Usando banco de dados
    Session = sessionmaker(bind=engine)
    session = Session()

    session.add(User(plataform, encrypted_key_password))
    session.commit()

    # Fechando a sessão
    session.close()


# NOTA: O github é um software livre e de ótima qualidade; este código
# visa apenas proteger de possíveis ataques hakers e também descentralizar o controle e
# armazenamento das senhas pelo google

def acess_account_github(cipher):
    from softwares.login_github import login

    load_dotenv()

    engine_account = create()
    
    Session = sessionmaker(bind=engine_account)
    session = Session()

    plataforms = session.query(User).all()

    for column in plataforms:
        if "Github" == column.plataform:
            encrypted_email = os.getenv("EMAIL_KEYWORD")
            email = cipher.decrypt(encrypted_email).decode()
            password = cipher.decrypt(column.password).decode()
            
            login(email, password)

            
