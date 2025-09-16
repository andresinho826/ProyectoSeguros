Feature: Como usuario quiero interactuar con la pagina OrangeHRM


Scenario Outline: Login en la pagina OrangeHRM
Given me encuentro en la pagina de Login
When ingreso el usuario "<usuario>"
And ingreso la contrasena "<contrasena>"
Then deberia visualizar login exitoso

Examples:
|usuario|contrasena|
|Admin|admin123|