from cryptography.fernet import Fernet
from dotenv import load_dotenv

import sqlite3
import os

# Função para definir o e-mail de usuário
def set_user_(email):
    """ 
    Esta função faz o setup do e-mail do usuário
    toda a informação sensível é criptografada e 
    está segura de pessoas maliciosas.

    Args:
        email (string): o email do usuário
    """

# Função para acessar contas de qualquer site de maneira segura e confiável
def set_acess_account(password):
    """
    Adiciona as contas de qualquer site, usando criptografia e protegendo os
    seus dados em um banco de dados local do seu computador.

    Args:
        password (string): a senha para entrar no site
    """
    
    # Gerando chave secreta
    key = Fernet.generate_key()
    chipher_suite = Fernet(key)

    # Encriptando a senha
    encrypted_key_password = chipher_suite.encrypt(password.encode())

    # Gravando nas variáveis de ambiente
    with open('.env', 'w') as file:
        file.write(f"KEY_PASSWORD={encrypted_key_password.decode()}\n")
        file.write(f"FERNET_KEY={key.decode}")
