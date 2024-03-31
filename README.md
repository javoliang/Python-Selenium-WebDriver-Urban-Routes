# Pruebas Automatizadas para Urban Routes

## Descripción del Proyecto

Este proyecto contiene un conjunto de pruebas automatizadas para la aplicación web Urban Routes, que permite a los usuarios solicitar un taxi y configurar su ruta.

## Tecnologías y Técnicas Utilizadas

- Python
- Selenium WebDriver
- Unittest (Módulo de pruebas unitarias de Python)
- PyTest
- Localizadores de elementos web (XPath, ID, clase, etc.)
- Simulación de interacciones del usuario (envío de texto, clics, pulsación de teclas, etc.)
- Manejo de modales y cuadros de diálogo
- Esperas explícitas e implícitas
- Recuperación de información de las herramientas de desarrollador del navegador

## Instrucciones para Ejecutar las Pruebas

1. **Requisitos previos**:
  - Tener Python instalado en tu sistema (versión 3.x)
  - Tener Google Chrome instalado en tu sistema

2. **Configuración del entorno**:
  - Clona este repositorio en tu máquina local.
  - Navega al directorio raíz del proyecto.
  - Instala las dependencias necesarias ejecutando el siguiente comando:
    ```
    pip3 install selenium
    pip3 install pytest-sugar
    ```

3. **Ejecución de las pruebas**:
  - Abre una terminal o línea de comandos.
  - Navega al directorio raíz del proyecto.
  - Ejecuta el siguiente comando para ejecutar las pruebas con PyTest:
    ```
    pytest main.py
    ```
  - Este comando ejecutará todas las pruebas definidas en el archivo `main.py` utilizando PyTest.

4. **Comportamiento de las pruebas**:
  - Las pruebas automatizadas simulan el proceso completo de solicitar un taxi en la aplicación web Urban Routes.
  - Cada prueba cubre una acción específica, como configurar la dirección, seleccionar la tarifa, rellenar el número de teléfono, agregar una tarjeta de crédito, escribir un mensaje para el conductor, pedir accesorios adicionales y, finalmente, solicitar un taxi.
  - Durante la ejecución, se abrirá una instancia del navegador Google Chrome, donde se podrá visualizar el progreso de las pruebas.
  - Las pruebas interactúan con la aplicación web a través de la biblioteca Selenium WebDriver, realizando acciones como enviar texto, hacer clic en elementos, simular pulsaciones de teclas, esperar la aparición de elementos, entre otras.
  - Al finalizar la ejecución de todas las pruebas, se cerrará la instancia del navegador.

Nota: Asegúrate de tener una conexión a Internet estable durante la ejecución de las pruebas, ya que se accede a una URL remota.

## Descripción del Código

### data.py

Este archivo contiene las variables y constantes necesarias para las pruebas automatizadas. Aquí se definen los siguientes elementos:

- `urban_routes_url`: La URL de la aplicación web Urban Routes.
- `address_from`: La dirección de origen para configurar la ruta.
- `address_to`: La dirección de destino para configurar la ruta.
- `phone_number`: El número de teléfono que se utilizará durante las pruebas.
- `card_number`: El número de la tarjeta de crédito que se utilizará durante las pruebas.
- `card_code`: El código de seguridad (CVV) de la tarjeta de crédito.
- `message_for_driver`: El mensaje que se enviará al conductor durante las pruebas.

### main.py

Este archivo contiene el código principal de las pruebas automatizadas. Está estructurado en tres partes principales:

1. **Función `retrieve_phone_code(driver)`**:
   - Esta función ayuda a obtener el código de confirmación del teléfono cuando la aplicación lo solicita durante el proceso de agregar una tarjeta de crédito.
   - Utiliza las herramientas de desarrollador del navegador para acceder a los registros de rendimiento y extraer el código de confirmación.
   - Es necesaria debido a que el código de confirmación no se puede obtener directamente de la interfaz de usuario.

2. **Clase `UrbanRoutesPage`**:
   - Representa la página principal de la aplicación Urban Routes.
   - Contiene localizadores de elementos web (como los campos de dirección de origen y destino) utilizando tuplas con el tipo de localizador y su valor correspondiente.
   - Incluye métodos para establecer la ruta (`set_route()`), obtener la dirección de origen (`get_from()`) y obtener la dirección de destino (`get_to()`).

3. **Clase `TestUrbanRoutes`**:
   - Esta clase heredada de `unittest.TestCase` contiene las pruebas automatizadas.
   - El método `setup_class()` se ejecuta antes de todas las pruebas y configura el controlador Selenium con opciones adicionales para habilitar el registro de rendimiento, necesario para obtener el código de confirmación del teléfono.
   - Cada método de prueba (`test_step_X()`) define una etapa del proceso de solicitud de un taxi en la aplicación web Urban Routes.
   - Las pruebas cubren acciones como configurar la dirección, seleccionar la tarifa, rellenar el número de teléfono, agregar una tarjeta de crédito, escribir un mensaje para el conductor, solicitar accesorios adicionales y, finalmente, solicitar un taxi.
   - Se utilizan técnicas como localización de elementos web, simulación de interacciones del usuario (envío de texto, clics, pulsación de teclas), manejo de modales y cuadros de diálogo, y esperas explícitas e implícitas para garantizar la correcta ejecución de las pruebas.
   - El método `teardown_class()` se ejecuta después de todas las pruebas y cierra la instancia del navegador.

Durante la ejecución de las pruebas, se utiliza la biblioteca Selenium WebDriver para automatizar las interacciones con la aplicación web. Es importante tener Google Chrome instalado y una conexión a Internet estable, ya que se accede a una URL remota durante las pruebas.

Es importante destacar que el código está diseñado para ser ejecutado en un entorno específico, con Google Chrome instalado y una conexión a Internet estable, ya que se accede a una URL remota durante las pruebas.

¡Disfruta de las pruebas automatizadas y mantén un control de calidad continuo en tu aplicación web!
