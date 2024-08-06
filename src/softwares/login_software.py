# Importando bibliotecas
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.firefox.service import Sevice as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from sqlalchemy import session_maker
from ..user import User, Base
from ..input_login_user import create
from dotenv import load_dotenv
import os

def login(plataform, cipher):
    found = False
    enc_url, enc_password = None, None

    # Realizando connecção com o banco de dados
    Session = session_maker(bind=create())
    session = Session()

    for item in session.query(User).all():
        if item.plataform == plataform:
        
            found = True
            enc_url = item.url
            enc_password = item.password

            break

    if not found:
        raise Exception("Plataform not found on database. Please ensure adding it before log-in")

    # Usando caminho do dotenv
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')

    # Acessando variável de ambiente 
    load_dotenv(path)

    # Acessando dados
    url = cipher.decrypt(enc_url).decode()
    password = cipher.decrypt(enc_password).decode()
    email = cipher.decrypt(os.getenv("EMAIL_KEYWORD")).decode()  

    # Realizando conecção com o software
    driver = webdriver.Firefox(service=FirefoxService(GeckDriverManager().install()))
    driver.get(url)

    # Automação do login
    driver.find_element(By.NAME, 'username').send_key(email)
    driver.find_element(By.NAME, 'password').send_key(password)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
