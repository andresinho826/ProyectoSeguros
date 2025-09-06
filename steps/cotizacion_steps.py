import os # libreria que reconoce el SO
from dotenv import load_dotenv # utilizar y trabajar con las variables de entorno creadas
import pytest # importamos para pytest BDD
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService # trabajamos con chrome inicialmente
from webdriver_manager.chrome import ChromeDriverManager
from pytest_bdd import scenarios, given, when, then, parsers
from pages.cotizacion_page import CotizacionPage

# --- cargar .env ---
load_dotenv("envs/prod.env")  # busca automáticamente .env en la raíz

SOAT_URL = os.getenv("SOAT_URL")  # lee la variable


# *** ruta absoluta al feature ***
"""THIS_FILE = os.path.abspath(__file__)
PROJECT_ROOT = os.path.dirname(os.path.dirname(THIS_FILE))
FEATURE_PATH = os.path.join(PROJECT_ROOT, "features", "cotizacion_soat.feature")

print("DEBUG feature path:", FEATURE_PATH)  # para ver en consola

# aquí le pasamos la ruta absoluta
scenarios(FEATURE_PATH)"""
scenarios("../features/cotizacion_soat.feature")

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    yield driver # libera recursos internamente - propio de python
    driver.quit()

@given('estoy en la pagina de cotizacion del SOAT')
def abrir_pagina(driver):
    cotizacion_page = CotizacionPage(driver)
    cotizacion_page.abrir(SOAT_URL)  # usar variable de entorno
    driver.page = cotizacion_page

@when(parsers.parse('ingreso la placa "{placa}" y solicito la cotizacion'))
def ingresar_placa_y_cotizar(driver, placa):
    page = driver.page
    page.ingresar_placa(placa)
    page.solicitar_cotizacion()

@then('debo ver el valor del SOAT para esa placa')
def validar_valor(driver):
    page = driver.page
    valor = page.obtener_valor()
    assert valor != ""
    print(f"Valor del SOAT: {valor}")