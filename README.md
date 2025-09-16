
# Proyecto de pruebas pytest-bdd + Selenium (OrangeHRM demo)

Este repositorio contiene una estructura de ejemplo para ejecutar pruebas E2E del login de **OrangeHRM ([https://opensource-demo.orangehrmlive.com](https://opensource-demo.orangehrmlive.com))** usando **pytest**, **pytest-bdd** (Gherkin), **Selenium** y el patrón **Page Object Model (POM)**.

El objetivo de este README es darte una guía paso a paso para instalar, ejecutar y mantener las pruebas, además de explicar la estructura de archivos y resolver problemas comunes.

---

## Tabla de contenido

1. Requisitos previos
2. Instalación
3. Estructura del proyecto
4. Variables de entorno (.env)
5. Contenido clave (ejemplos de archivos)

   * `features/login.feature`
   * `pages/login_page.py`
   * `steps/login_steps.py` (o `steps/login_steps.py`)
   * `conftest.py` (opcional)
6. Cómo ejecutar las pruebas
7. Buenas prácticas y recomendaciones
8. Troubleshooting (errores comunes)
9. Extensiones/CI (no aplicadas en este proyecto aun)

---

## 1. Requisitos previos

* Python 3.8+ instalado
* Google Chrome instalado (u otro navegador si cambias el driver)
* Conexión a internet (para `webdriver-manager` descargar chromedriver la primera vez)
* (Opcional) VS Code u otro editor

---

## 2. Instalación

1. Crea y activa un entorno virtual (recomendado):

```bash
python -m venv myenv
# Windows
myenv\Scripts\activate
# macOS / Linux
source myenv/bin/activate
```

2. Crea un archivo `requirements.txt` con estas dependencias ejemplo:

```
pytest
pytest-bdd
selenium
webdriver-manager
python-dotenv
```

3. Instala las dependencias:

```bash
pip install -r requirements.txt
```

---

## 3. Estructura del proyecto (sugerida)

```
project-root/
├── features/
│   └── login.feature
├── pages/
│   └── login_page.py
├── steps/        # o tests/
│   └── login_steps.py/
│       
├── envs/
│   └── qa.env
├── requirements.txt
├── pytest.ini    # (opcional) config de pytest
└── README.md
```

---

## 4. Variables de entorno (.env)

Crea un archivo `envs/qa.env` con el contenido:

```
ORANGE_URL=https://opensource-demo.orangehrmlive.com/web/index.php/auth/login
```

Asegúrate de que el nombre de la variable (`ORANGE_URL`) coincida exactamente con lo que lees en tu script (`os.getenv("ORANGE_URL")`).

---

## 5. Contenido clave (ejemplos)

A continuación tienes ejemplos listos para copiar y pegar. **Ajusta rutas y nombres si tu proyecto las difiere.**

### `features/login.feature`

```gherkin
Feature: Login OrangeHRM
  Para acceder a la aplicación como usuario válido

  Scenario Outline: Login exitoso
    Given me encuentro en la pagina de Login
    When ingreso el usuario "<usuario>"
    And ingreso la contrasena "<contrasena>"
    Then deberia visualizar login exitoso

  Examples:
    | usuario | contrasena |
    | Admin   | admin123   |
```

> Importante: los textos de los steps deben coincidir exactamente con los decoradores usados en `login_steps.py` (placeholders y comillas incluidas si usas `parsers.parse('... "{usuario}"')`).

---

### `pages/login_page.py` (Page Object Model)

```python
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        # Locators robustos
        self.username_input = (By.NAME, "username")
        self.password_input = (By.NAME, "password")
        self.login_btn = (By.CSS_SELECTOR, "button.orangehrm-login-button")
        self.active_menu_item = (By.CSS_SELECTOR, "a.oxd-main-menu-item.active")

    def abrir(self, url):
        self.driver.get(url)

    def ingresar_usuario(self, usuario):
        el = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.username_input)
        )
        el.clear()
        el.send_keys(usuario)

    def ingresar_contrasena(self, contrasena):
        el = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.password_input)
        )
        el.clear()
        el.send_keys(contrasena)

    def click_login(self):
        btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.login_btn)
        )
        btn.click()

    def login_exitoso(self):
        try:
            return WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.active_menu_item)
            ) is not None
        except:
            return False
```

---

### `tests/steps/login_steps.py` (o `steps/login_steps.py`)

```python
import os
from dotenv import load_dotenv
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from pytest_bdd import scenarios, given, when, then, parsers
from pages.login_page import LoginPage

# Cargar variables de entorno
load_dotenv("envs/qa.env")
ORANGE_URL = os.getenv("ORANGE_URL")

# Registrar feature (ruta relativa desde donde ejecutas pytest)
scenarios("features/login.feature")

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=options
    )
    driver.implicitly_wait(5)  # espera implícita moderada
    yield driver
    driver.quit()

@given('me encuentro en la pagina de Login')
def abrir_pagina(driver):
    login_page = LoginPage(driver)
    login_page.abrir(ORANGE_URL)
    driver.page = login_page

@when(parsers.parse('ingreso el usuario "{usuario}"'))
def ingresar_credencial_usuario(driver, usuario):
    page = driver.page
    page.ingresar_usuario(usuario)

@when(parsers.parse('ingreso la contrasena "{contrasena}"'))
def ingresar_credencial_contrasena(driver, contrasena):
    page = driver.page
    page.ingresar_contrasena(contrasena)
    page.click_login()

@then('deberia visualizar login exitoso')
def validar_login_exitoso(driver):
    page = driver.page
    assert page.login_exitoso() is True
```

> Nota: puedes mover la fixture `driver` a `conftest.py` si quieres que esté disponible globalmente para otros tests.

---

### `conftest.py` (opcional - para fixtures globales)

```python
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="session")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=options
    )
    driver.implicitly_wait(5)
    yield driver
    driver.quit()
```

---

## 6. Cómo ejecutar las pruebas

* Ejecutar **todos** los tests:

```bash
pytest -v
```

* Ejecutar un **archivo de steps** o un test específico (recomendado para debug):

```bash
pytest -v steps/login_steps.py
# O ejecutar la función de test generada (si conoces el nombre):
pytest -v steps/login_steps.py::test_login_en_la_pagina_orangehrm
```

> ⚠️ `pytest` no ejecuta archivos `.feature` directamente como si fuesen tests. Con `pytest-bdd`, los tests se generan a partir de las funciones Python que cargan los feature (por ejemplo, usando `scenarios("features/login.feature")`). Por eso normalmente ejecutas `pytest` sobre módulos Python (tests/steps) o usas `-k` para filtrar por nombre.

* Ejecutar un test por nombre (filtro -k):

```bash
pytest -k login -v
```

---

## 7. Buenas prácticas y recomendaciones

* **Locators**: usar `By.ID` o `By.NAME` cuando existan. Evitar `placeholder` como locator por traducciones o cambios. Preferir `CSS_SELECTOR` limpio sobre XPATH cuando sea posible.
* **WAI**: combinar `implicitly_wait(5)` + `WebDriverWait` explícitos en los métodos que lo requieran.
* **POM**: cada página con sus métodos (abrir, completar campos, clics, validaciones).
* **Clear**: limpiar campos antes de escribir (`.clear()`).
* **Conftest**: centraliza fixtures reutilizables en `conftest.py`.
* **Datos**: para credenciales sensibles, usa variables de entorno y secretos seguros.

---

## 8. Troubleshooting (errores comunes)

### `InvalidSelectorException`

Causa: estás usando un XPATH con `By.CSS_SELECTOR` (ej: `"//input[@name='username']"`) o el selector CSS está mal formado.

Solución:

* Asegúrate de usar `By.XPATH` con strings `//` o `By.CSS_SELECTOR` con selectores válidos.
* Evita espacios/nombres de clases sin el punto (`a.class1.class2` vs `a.class1 class2`).

### `NoSuchElementException`

Causa: el elemento no está en el DOM en el momento de la búsqueda.

Solución:

* Aumenta espera explícita usando `WebDriverWait` y `expected_conditions`.
* Verifica si el elemento está dentro de un `iframe` (en tal caso `driver.switch_to.frame(...)`).

### `None` al abrir URL

Causa: variable de entorno `ORANGE_URL` no definida o mal escrita.
Solución: revisar `envs/qa.env` y `load_dotenv("envs/qa.env")` y que `os.getenv("ORANGE_URL")` coincide con el nombre.

---

## 9. Extensiones / CI

* Para integrarlo a CI (GitHub Actions / GitLab CI), instala las dependencias, ejecuta `pytest -q` y asegúrate de ejecutar en runner con navegador (o usar un contenedor con Chrome + chromedriver). También puedes usar `selenium/standalone-chrome` y ejecutar pruebas apuntando al Grid.

---

## Conclusión

Correo de contacto:

#### andresinho826@gmail.com
