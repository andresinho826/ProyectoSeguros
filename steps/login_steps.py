import os # libreria que reconoce el SO
from dotenv import load_dotenv # utilizar y trabajar con las variables de entorno creadas
import pytest # importamos para pytest BDD
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService # trabajamos con chrome inicialmente
from webdriver_manager.chrome import ChromeDriverManager
from pytest_bdd import scenarios, given, when, then, parsers
from pages.login_page import LoginPage

# --- cargar .env ---
load_dotenv("envs/qa.env")  # busca automáticamente .env en la raíz

ORANGE_URL = os.getenv("ORANGE_URL")  # lee la variable


# *** ruta absoluta al feature ***
scenarios("../features/login.feature")

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.implicitly_wait(15) # espera implita de 15 segundos
    yield driver # libera recursos internamente - propio de python
    driver.quit()

@given('me encuentro en la pagina de Login')
def abrir_pagina(driver):
    login_page = LoginPage(driver)
    login_page.abrir(ORANGE_URL)  # usar variable de entorno
    driver.page = login_page

@when(parsers.parse('ingreso el usuario "{usuario}"'))
def ingresar_credencial_usuario(driver, usuario):
    page = driver.page
    page.ingresar_usuario(usuario)

@when(parsers.parse('ingreso la contrasena "{contrasena}"'))
def ingresar_credencial_contrasena(driver, contrasena):
    page = driver.page
    page.ingresar_contrasena(contrasena)
    page.boton_login()

@then('deberia visualizar login exitoso')
def validar_login_exitoso(driver):
    page = driver.page
    assert page.login_exitoso() == True
    