from PySimpleGUI import PySimpleGUI as sg
from sqlalchemy import sessionmaker
from ..src.input_login_user import set_user_
from ..src.softwares.firefox import login as login_firefox
from ..src.input_login_user import setup as stp
from ..src.input_login_user import create
from ..src.user import User


import pickle
import os

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


# Código gerado por Perplexity.ai
# Função para validar o formato do e-mail
def validate_email(email):
    # Regex para validação de e-mail
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

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

    def setup(self):
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

                    with open("cipher.pkl", "w") as file:
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
            engine = create()
            window = sg.Window("Config", layout_config)        

    def config_account(self):
        # Checagem do user.id
        u_stat = os.stat("cipher.pkl")
        auth_uid = u_stat.st_uid

        user = os.getuid() # Usuário atual

        if user == auth_uid:
            # Acessando banco de dados

            engine = create()
            Session = sessionmaker(bind=engine)
            session = Session()
            
            # Criando layout
            layout_config_account =  [
                [sg.Text("Account to change pass"), sg.OptionMenu([item.plataform for item in session.query(User).all()])],
                [sg.Text]
            ] 


