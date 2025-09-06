Feature: Cotización del SOAT

  Como prospecto cliente
  Quiero cotizar el SOAT ingresando la placa de mi vehículo
  Para conocer el valor de la poliza antes de comprarla


Scenario Outline: Cotizar SOAT con varias placas
    Given estoy en la pagina de cotizacion del SOAT
    When ingreso la placa "<placa>" y solicito la cotizacion
    Then debo ver el valor del SOAT para esa placa

    Examples:
      | placa    |
      | ABC123   |
      | XYZ789   |
