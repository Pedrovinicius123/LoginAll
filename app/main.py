from PySimpleGUI import PySimpleGUI as sg
from sqlalchemy import sessionmaker
from ..src.input_login_user import set_user_
from ..src.softwares.firefox import login as login_firefox
from ..src.input_login_user import setup as stp
from ..src.input_login_user import create
from ..src.user import User
from dotenv import load_dotenv

import passlib.pwd as pwd
import pickle
import os
import re

# Criando layouts
layout_init = [
    [sg.Text("Submit your email"), sg.InputText(key="email")],
    [sg.Text(key="error_message")],
    [sg.Button("Submit"), sg.Button("Cancel")]
]

layout_set_account = [
    [sg.Text("New software name"), sg.InputText(key="software")],
    [sg.Text("Password"), sg.InputText(key="password")],
    [sg.Button("Create link"), sg.Button("Config email"), sg.Button("Cancel")]
]

layout_enter_account = [
    [sg.Text("Software name"), sg.InputText(key="software")],
    [sg.Button("Login"), sg.Button("Config email"), sg.Button("Cancel")]
]

layout_config = [
    [sg.Text("Change email"), sg.InputText(key="email")],
    [sg.Button("Submit"), sg.Button("Cancel")]
]

layout_general = [
    [sg.Text("Welcome to menu")],
    [sg.Button("Add Account for login list"), sg.Button("Config account"), sg.Button("Config general")]
]

layout_config_account =  [
    [sg.Text("Account email"), sg.InputText(key="-INPUT-"), sg.Checkbox("Change email", key="-CHANGE EMAIL-")],
    [sg.Text("", key="-ERROR 1-")],
    [sg.Text("Account to change pass"), sg.OptionMenu(key="-OPTIONS-")],
    [sg.Text("New pass"), sg.InputText(key="-INPUT 0-")],
    [sg.Text("New pass (confirmation)"), sg.InputText(key="-INPUT 1-")],
    [sg.Text(key="-ERROR-")]
    [sg.Button("Confirm"), sg.Button("Cancel")]
]

layout_login_web = [
    [sg.Text("Account to login"), sg.OptionMenu(key="-OPTIONS-")],
    [sg.Button("Login")]
]


# Código gerado por Perplexity.ai
# Função para validar o formato do e-mail
def validate_email(email):
    # Regex para validação de e-mail
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

# Code inpired from javatpoint.com (https://www.javatpoint.com/password-validation-in-python)
def validate_password(password):
    pwd.PasswordPolicy.from_names(
        lenght=10,
        digits=2,
    )

    return pwd.test(password)

class UserInput:
    """ 
    Aqui fica a classe que gerencia o input do usuário.
    """
    def __init__(self, first_time=True):
        """
        Método construtor, checa se o usuário já configurou o email 
        """
        
        sg.theme("reddit")
        self.first_time = first_time

        if first_time:                
            self.engine = self.setup()

        window = sg.Window("Menu", layout_general)

        while True:
            # ...
            break

    def setup(self):
        engine = create()

        if self.first_time:
            window = sg.Window("Setup", layout_init)
            engine = stp()

            # Loop infinito para a janela            
            while True:
                event, values = window.read()
                
                if event == sg.WIN_CLOSED or event == "Cancel":
                    break

                elif event == "Submit" and (values["email"] == "" or not validate_email(values["email"])):
                    new_elem = sg.Text("Input de email incorreto")
                    window["error_message"].update(new_elem)

                elif event == "Submit":
                    cipher = set_user_(values['email'])

                    with open("cipher.pkl", "wb") as file:
                        pickle.dump(cipher, file)

                    # Controle de acesso
                    os.chmod("cipher.pkl", 0o600)
            
        return engine

    def config(self):
        # Checagem do user.id
        u_stat = os.stat("cipher.pkl")
        auth_uid = u_stat.st_uid

        user = os.getuid() # Usuário recurrente

        if user == auth_uid:

            load_dotenv()

            # Usando o cipher
            cipher = None
            with open("cipher.pkl", "rb") as infile:
                cipher = pickle.load(infile)

            # Criando janela
            window = sg.Window("Config", layout_config)
            
            while True:
                events, values = window.read()

                if events == sg.WIN_CLOSED or events == "Cancel":
                    break

                


    def config_account(self):
        # Checagem do user.id
        u_stat = os.stat("cipher.pkl")
        auth_uid = u_stat.st_uid

        user = os.getuid() # Usuário atual

        def validate(values, session, layout_config_account):
            if not validate_password(values["-INPUT 1-"]) or not validate_password(values["-INPUT 0-"]):
                layout_config_account["-ERROR-"].update("All the password fields must be at least 10 lenght and have 2 digits!")

            elif values["-INPUT 1-"] != values["-INPUT 0-"]:
                layout_config_account['-ERROR-'].update("The password fields must be equal!")

            else:
                for item in session.query(User).all():
                    if item.platform == values["-OPTIONS-"]:
                        item.password = cipher.encrypt(values["-INPUT 1-"]).encode()
                        
                        # Fechando banco de dados
                        session.commit()
                        session.close()
                        break
                

        if user == auth_uid:
            load_dotenv()

            # Acessando cifra
            cipher = None
            with open("cipher.pkl", 'rb') as file:
                cipher = pickle.load(file)

            # Acessando banco de dados
            engine = create()
            Session = sessionmaker(bind=engine)
            session = Session()
            
            # Criando layout            
            layout_config_account["-OPTIONS-"].update([item.platform for item in session.query(User).all()])
            window = sg.Window("Account config", layout_config_account)

            while True:
                event, values = window.read()

                if event == sg.WIN_CLOSED or event == "Cancel":
                    break

                elif event == "Confirm":
                    if layout_config_account["-CHANGE EMAIL-"]:
                        email_change = True

                    if email_change and values["-INPUT-"] == "" or not validate_email(values["-INPUT-"]):
                        values["-ERROR 1-"].update("Invalid input")

                    validate(values, session, layout_config_account)
                        

                        
                    
