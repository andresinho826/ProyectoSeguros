from selenium.webdriver.common.by import By

class CotizacionPage:
    def __init__(self, driver):
        self.driver = driver
        self.placa_input = (By.ID, "placa")                # Ejemplo: id del campo placa
        self.cotizar_button = (By.ID, "btnCotizar")       # Botón cotizar
        self.valor_label = (By.ID, "valorSOAT")           # Elemento donde se muestra el valor

    def abrir(self, url):
        self.driver.get(url)


    def ingresar_placa(self, placa):
        self.driver.find_element(*self.placa_input).send_keys(placa)

    def solicitar_cotizacion(self):
        self.driver.find_element(*self.cotizar_button).click()

    def obtener_valor(self):
        return self.driver.find_element(*self.valor_label).text