import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


def pytest_addoption(parser):
    """
    Permite pasar parámetros desde la línea de comandos.
    Ejemplo:
      pytest --browser chrome
      pytest --browser firefox
    """
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Navegador para ejecutar las pruebas: chrome o firefox"
    )


@pytest.fixture
def driver(request):
    """
    Fixture principal que levanta el navegador y lo cierra al finalizar la prueba.
    """
    browser = request.config.getoption("--browser")

    if browser.lower() == "chrome":
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    elif browser.lower() == "firefox":
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    else:
        raise ValueError(f"Navegador no soportado: {browser}")

    driver.maximize_window()
    driver.implicitly_wait(10)

    yield driver

    driver.quit()
