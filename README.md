# Pruebas Automatizadas para Urban Routes

## Descripción del Proyecto

Este proyecto contiene un conjunto de pruebas automatizadas para la aplicación web Urban Routes, que permite a los usuarios solicitar un taxi y configurar su ruta.

## Tecnologías y Técnicas Utilizadas

- Python
- Selenium WebDriver
- Unittest (Módulo de pruebas unitarias de Python)
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
    pip install selenium
    ```

3. **Ejecución de las pruebas**:
  - Abre una terminal o línea de comandos.
  - Navega al directorio raíz del proyecto.
  - Ejecuta el siguiente comando:
    ```
    python main.py
    ```
  - Este comando ejecutará todas las pruebas definidas en el archivo `main.py`.

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

Este archivo contiene el código principal de las pruebas automatizadas. A continuación, se describen los componentes clave:

1. **Importación de módulos y definición de funciones auxiliares**:
  - Se importan los módulos necesarios, como `data`, `time`, `unittest`, `selenium` y sus subcomponentes.
  - Se define la función `retrieve_phone_code(driver)`, que intercepta y devuelve el código de confirmación del teléfono requerido para agregar una tarjeta de crédito. Esta función utiliza las herramientas de desarrollador del navegador para obtener el código.

2. **Clase UrbanRoutesPage**:
  - Esta clase representa la página principal de la aplicación Urban Routes.
  - Contiene localizadores de elementos web (como los campos de dirección de origen y destino) utilizando tuplas con el tipo de localizador y su valor correspondiente.
  - Incluye métodos para establecer la ruta (`set_route()`), obtener la dirección de origen (`get_from()`) y obtener la dirección de destino (`get_to()`).

3. **Clase TestUrbanRoutes**:
  - Esta clase heredada de `unittest.TestCase` contiene las pruebas automatizadas.
  - El método `setup_class()` se ejecuta antes de todas las pruebas y configura el controlador Selenium con opciones adicionales para habilitar el registro de rendimiento, necesario para obtener el código de confirmación del teléfono.
  - El método `test_set_route()` define la prueba principal que cubre todo el proceso de solicitar un taxi, desde configurar la dirección hasta finalizar la solicitud.
  - Dentro de `test_set_route()`, se realizan las siguientes acciones:
    1. **Navegar a la URL de Urban Routes**:
       - El código `self.driver.get(data.urban_routes_url)` abre la URL de la aplicación web Urban Routes en una nueva instancia del navegador Chrome.

    2. **Configurar la dirección de origen y destino**:
       - Se utilizan esperas explícitas (`WebDriverWait`) para esperar hasta que los elementos web correspondientes a los campos de dirección de origen y destino estén visibles.
       - Una vez que los elementos son visibles, se envían las direcciones de origen (`address_from`) y destino (`address_to`) a los campos correspondientes utilizando el método `send_keys()`.

    3. **Seleccionar la tarifa Comfort**:
       - Se espera hasta que el botón "Pedir un taxi" esté habilitado para hacer clic.
       - Después de hacer clic en el botón, se espera hasta que la imagen de la tarifa "Comfort" sea visible y se hace clic en ella.

    4. **Rellenar el número de teléfono y obtener el código de confirmación**:
       - Se interactúa con varios elementos de la interfaz de usuario para ingresar el número de teléfono (`self.phone_number`).
       - Se envía el número de teléfono al campo correspondiente y se hace clic en el botón "Siguiente".
       - Se llama a la función `retrieve_phone_code(self.driver)` para obtener el código de confirmación del teléfono.
       - Se interactúa con más elementos para ingresar el código de confirmación obtenido y hacer clic en el botón "Confirmar".

    5. **Agregar una tarjeta de crédito**:
       - Se interactúa con varios elementos para abrir el modal de "Agregar una tarjeta".
       - Se envía el número de la tarjeta de crédito (`card_number`) al campo correspondiente.
       - Se simula la pulsación de la tecla TAB y se envía el código de seguridad (`card_code`) al campo correspondiente.
       - Se hace clic en el botón "Agregar" para agregar la tarjeta de crédito.
       - Se cierra el cuadro de diálogo correspondiente.

    6. **Escribir un mensaje para el conductor**:
       - Se interactúa con los elementos necesarios para localizar el campo de comentarios o mensaje para el conductor.
       - Se envía el mensaje (`message_for_driver`) al campo correspondiente.

    7. **Pedir una manta y pañuelos**:
       - Se localiza y hace clic en el control deslizante ("slider") para solicitar una manta y pañuelos.

    8. **Pedir 2 helados**:
       - Se localiza el botón de incremento del contador de helados y se hace clic dos veces para solicitar 2 helados.

    9. **Solicitar un taxi a través del modal correspondiente**:
       - Se espera hasta que el botón "Pedir un taxi" esté habilitado para hacer clic.
       - Se hace clic en el botón para abrir el modal correspondiente y solicitar un taxi.

    10. **Esperar a que aparezca la información del conductor (paso opcional)**:
        - Se espera hasta que el botón de "Detalles" esté habilitado para hacer clic.
        - Se hace clic en el botón de "Detalles" para mostrar la información del conductor.
        - Se espera durante 20 segundos para simular la visualización de los detalles.

  - El método `teardown_class()` se ejecuta después de todas las pruebas y cierra la instancia del navegador.

Durante la ejecución de las pruebas, se utiliza la biblioteca Selenium WebDriver para automatizar las interacciones con la aplicación web. Se emplean técnicas como localización de elementos web, simulación de interacciones del usuario (envío de texto, clics, pulsación de teclas), manejo de modales y cuadros de diálogo, y esperas explícitas e implícitas para garantizar la correcta ejecución de las pruebas.

Es importante destacar que el código está diseñado para ser ejecutado en un entorno específico, con Google Chrome instalado y una conexión a Internet estable, ya que se accede a una URL remota durante las pruebas.

¡Disfruta de las pruebas automatizadas y mantén un control de calidad continuo en tu aplicación web!
