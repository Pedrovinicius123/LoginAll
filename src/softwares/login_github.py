# Importando bibliotecas
from selenium import webdriver
from webdriver_manager.firefox.service import Sevice as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

def login(email, password):
    # Realizando conecção com o software
    driver = webdriver.Firefox(service=FirefoxService(GeckDriverManager().install()))
    driver.get("https://github.com/login")

    # Automação do login
    driver.find_element('xpath', '//*[@id="login_field"]').send_key(email)
    driver.find_element('xpath', '//*[@id="password"]').send_key(password)
    driver.find_element('xpath', '/html/body/div[1]/div[3]/main/div/div[4]/form/div/input[13]').click()



