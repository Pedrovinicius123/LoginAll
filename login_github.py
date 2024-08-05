# Importando bibliotecas
from selenium import webdriver
from webdriver_manager.firefox.service import Sevice as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

# Realizando conecção com o software
driver = webdriver.Firefox(service=FirefoxService(GeckDriverManager().install()))
driver.get("https://github.com/login")

# Automação do login
driver.find_element('xpath', '//*[@id="login_field"]').send_key()
driver.find_element('xpath', '//*[@id="password"]')

