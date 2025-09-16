from selenium.webdriver.common.by import By

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        """
        self.usuario = (By.XPATH, "//input[@placeholder='Username']")                # input login
        self.contrasena = (By.XPATH, "//input[@placeholder='Password']")       # input contraseña
        self.login_button = (By.XPATH, "//button[@type='submit']")           # boton submit
        self.login_exitoso_ = (By.XPATH, "//a[@class='oxd-main-menu-item active']")
        """

        self.usuario_input = (By.NAME, "username")                # input login
        self.contrasena_input = (By.NAME, "password")        # input contraseña
        self.login_button = (By.CSS_SELECTOR, "button.orangehrm-login-button")           # boton submit
        self.login_exitoso_ = (By.XPATH, "//a[@class='oxd-main-menu-item active']")

         # validar si este boton esta presente por pantalla

    def abrir(self, url):
        self.driver.get(url)


    def ingresar_usuario(self, usuario):
        self.driver.find_element(*self.usuario_input).clear()
        self.driver.find_element(*self.usuario_input).send_keys(usuario)

    def ingresar_contrasena(self, contrasena):
        self.driver.find_element(*self.contrasena_input).clear()
        self.driver.find_element(*self.contrasena_input).send_keys(contrasena)

    def boton_login(self):
        self.driver.find_element(*self.login_button).click()

    def login_exitoso(self):
        try:
            return self.driver.find_element(*self.login_exitoso_).is_displayed()
        except:
            return False