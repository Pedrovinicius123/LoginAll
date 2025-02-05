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
def set_user_(email):
    """ 
    Esta função faz o setup do e-mail do usuário
    toda a informação sensível é criptografada e 
    está segura de pessoas maliciosas.

    Args:
        email (string): o email do usuário
    """
    
    cipher = generate_cipher()
    # Criptografando o email
    encrypted_email = cipher.encrypt(email.encode())

    # Gravando nas variáveis de ambiente
    with open('.env', 'w') as file:
        file.write(f"EMAIL_KEYWORD={encrypted_email.decode()}\n")
        file.write(f"FERNET_KEY={key.decode()}")

    return cipher


# Função para acessar contas de qualquer site de maneira segura e confiável
@acess_cipher
def set_acess_account(plataform, url, password, cipher):
    """
    Adiciona as contas de qualquer site, usando criptografia e protegendo os
    seus dados em um banco de dados local do seu computador.

    Args:
        password (string): a senha para entrar no site
    """

    engine = create()

    # Encriptando a senha
    encrypted_key_password = cipher.encrypt(password.encode())
    ecrypted_url = cipher.encrypt(url.encode())
    
    # Usando banco de dados
    Session = sessionmaker(bind=engine)
    session = Session()

    session.add(User(plataform, encrypted_url, encrypted_key_password))
    session.commit()

    # Fechando a sessão    from sqlalchemy import update, Table, MetaData
    session.close()

def update_data_cipher(cipher_anterior, general_password):
    """
    Função para update da criptografia,
    tornando a palicação ainda mais segura

    Args:
        cipher_anterior (Fernet()): A antiga cifra da criptografia
    """

    # Criando novo cipher
    key = Fernet().generate_key()
    new_cipher = Fernet(key)

    # Criando conexão
    engine = create()
    conn = engine.connect()
    metadata = MetaData()

    # Criando sessão
    Session = sessionmaker(bind=engine)
    session = Session()

    # Criptografando dados
    for websites in session.query(User).all():

        url = cipher_anterior.decrypt(websites.url).decode()
        password = cipher_anterior.decrypt(websites.password).decode()

        websites.url = new_cipher.encrypt(url.encode())
        websites.password = new_cipher.encrypt(url.encode())
    
    # Retornando a cifra nova
    return new_cipher
    