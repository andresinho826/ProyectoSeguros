import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from pages.cotizacion_page import CotizacionPage

# Vinculamos el feature
scenarios("../features/cotizacion.feature")

@pytest.fixture
def cotizacion_page(driver):
    return CotizacionPage(driver)

@given("estoy en la pagina de cotizacion del SOAT")
def abrir_pagina_cotizacion(cotizacion_page):
    cotizacion_page.abrir_pagina()

@when(parsers.parse('ingreso la placa "{placa}" y solicito la cotizacion'))
def ingresar_placa_y_cotizar(cotizacion_page, placa):
    cotizacion_page.ingresar_placa(placa)
    cotizacion_page.solicitar_cotizacion()

@then("debo ver el valor del SOAT para esa placa")
def verificar_resultado(cotizacion_page):
    resultado = cotizacion_page.obtener_resultado()
    assert resultado is not None
    assert "SOAT" in resultado or resultado.strip() != "", "El resultado del SOAT no se mostró correctamente"
