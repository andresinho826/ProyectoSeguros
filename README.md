
# Proyecto de Automatización - Seguros Mundial

Este repositorio contiene una estructura básica de automatización de pruebas utilizando **Page Object Model (POM)** como patrón de diseño y **pytest-bdd** como framework para Desarrollo Basado en el Comportamiento (BDD).

---

## 📂 Estructura del Proyecto

```

segurosMundial/
│
├── features/               # Archivos .feature (escenarios en Gherkin)
│   └── login.feature
│
├── pages/                  # Page Objects (interacción con la UI)
│   └── login\_page.py
│
├── steps/                  # Definición de pasos (Given, When, Then)
│   └── test\_login\_steps.py
│
└── conftest.py             # Configuración y fixtures compartidos

````

---

## 🛠️ Requisitos Previos

- **Python 3.8+**
- **pip** actualizado
- **Git** instalado

### 🔧 Paquetes recomendados en VSCode
- [Material Icon Theme](https://marketplace.visualstudio.com/items?itemName=PKief.material-icon-theme)
- [GitHub Copilot](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot) (opcional, uso personal)
- [Cucumber (Gherkin) Full Support](https://marketplace.visualstudio.com/items?itemName=alexkrechik.cucumberautocomplete)

---

## ⚙️ Configuración del Entorno

1. **Crear máquina virtual**
   ```bash
   python -m venv myenv
````

2. **Activar el entorno virtual**

   * En **Windows CMD**:

     ```bash
     myenv\Scripts\activate
     ```
   * En **PowerShell** (puede requerir permisos):

     ```bash
     .\myenv\Scripts\Activate.ps1
     ```

3. **Instalar dependencias**

   ```bash
   pip install selenium
   pip install pytest pytest-bdd
   ```


     ```bash
   pip install -r requirements.txt
   pip list

   ```

---

## 📝 ¿Qué es un Feature?

Un archivo **Feature** describe **qué debe hacer el sistema** desde el punto de vista del usuario o negocio.
No se enfoca en cómo se implementa, sino en **funcionalidades, comportamientos y reglas de negocio**.

### 📄 Estructura básica de un Feature

```gherkin
Feature: [Nombre de la funcionalidad]
  [Descripción breve opcional]

  Scenario: [Caso específico a probar]
    Given [precondición]
    When [acción del usuario o del sistema]
    Then [resultado esperado]
```

---

## 🔄 Relación con el Patrón AAA

El desarrollo de escenarios BDD se relaciona directamente con el **Patrón AAA (Arrange-Act-Assert):**

* **Arrange → Given** → Preparación o precondiciones.
* **Act → When** → Acción del usuario o evento del sistema.
* **Assert → Then** → Verificación del resultado esperado.

---

## 🚀 Ejecución de pruebas

Para correr las pruebas:

```bash
pytest -v
```

Si se quieren ejecutar pruebas de un **feature específico**:

```bash
pytest features/login.feature -v
```

---

## 📌 Notas

* Puede ser necesario cambiar de consola (por ejemplo, de **PowerShell** a **CMD**) para activar correctamente el entorno virtual.
* Mantén actualizadas las librerías con:

  ```bash
  pip install --upgrade pip
  ```

