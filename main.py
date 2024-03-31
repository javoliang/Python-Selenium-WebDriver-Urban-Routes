import data
import time
import unittest
import pytest_sugar
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Función para recuperar el código de confirmación del teléfono
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado
    en la aplicación."""
    import json
    from selenium.common import WebDriverException

    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n Utiliza "
                            "'retrieve_phone_code' solo después de haber solicitado el código "
                            "en tu aplicación.")
        return code

class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')

    def __init__(self, driver):
        self.driver = driver

    def set_route(self, address_from, address_to):
        self.driver.find_element(*self.from_field).send_keys(address_from)
        self.driver.find_element(*self.to_field).send_keys(address_to)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')


class TestUrbanRoutes(unittest.TestCase):
    phone_number = data.phone_number
    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado
        # para recuperar el código de confirmación del teléfono
        from selenium.webdriver import DesiredCapabilities

        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--perfLoggingPrefs=enableNetwork')
        cls.driver = webdriver.Chrome(options=chrome_options)

    def test_step_1(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to

        # Esperar hasta que los campos de origen y destino estén visibles y enviar las direcciones
        from_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(routes_page.from_field)
        )
        from_element.send_keys(address_from)
        to_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(routes_page.to_field)
        )
        to_element.send_keys(address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to
    def test_step_2(self):
        # Paso 2: Seleccionar la tarifa Comfort.
        comfort_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@class="button round" and text()="Pedir un taxi"]'))
        )
        comfort_button.click()
        comfort_image = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//img[@alt="Comfort"]'))
        )
        comfort_image.click()
        assert comfort_image.is_displayed()
    def test_step_3(self):
        # Paso 3: Rellenar el número de teléfono
        phone_number_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[text()='Número de teléfono']"))
        )
        phone_number_element.click()
        phone_label = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//label[text()='Número de teléfono']"))
        )
        phone_label.click()
        phone_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "phone"))
        )
        phone_input.send_keys(self.phone_number)
        submit_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@class='button full' and text()='Siguiente']"))
        )
        submit_button.click()
        # Obtener el código de confirmación del teléfono
        self.confirmation_code = retrieve_phone_code(self.driver)
        # Introducir el código de confirmación y confirmar
        code_label = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//label[@for='code' and text()='Introduce el código']"))
        )
        code_label.click()
        time.sleep(1)
        code_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "code"))
        )
        code_input.send_keys(self.confirmation_code)
        time.sleep(1)
        submit_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@class='button full' and text()='Confirmar']"))
        )
        submit_button.click()
        assert submit_button.is_enabled()
    def test_step_4(self):
        # Paso 4: Agregar una Tarjeta de Crédito
        payment_method_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@class='pp-text' and text()='Método de pago']"))
        )
        payment_method_element.click()
        time.sleep(1)
        plus_button = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//img[@class='pp-plus']"))
        )
        plus_button.click()
        card_number = data.card_number
        card_code = data.card_code
        # Introducir el número de tarjeta y el código
        card_number_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "number"))
        )
        card_number_element.send_keys(card_number)
        time.sleep(1)
        # Simular presionar la tecla TAB para cambiar el enfoque y agregar el código de la tarjeta
        ActionChains(self.driver).send_keys(Keys.TAB).perform()
        time.sleep(1)
        ActionChains(self.driver).send_keys(card_code).perform()
        time.sleep(1)
        ActionChains(self.driver).send_keys(Keys.TAB).perform()
        time.sleep(1)
        ActionChains(self.driver).send_keys(card_code).perform()
        time.sleep(1)
        ActionChains(self.driver).send_keys(Keys.TAB).perform()
        time.sleep(1)
        # Localizar el botón "Agregar" y hacer clic en él
        add_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@class='button full' and text()='Agregar']"))
        )
        add_button.click()
        time.sleep(1)
        # Cerrar el cuadro de diálogo para continuar
        close_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[1]/button'))
        )
        close_button.click()
        assert close_button.is_enabled()
    def test_step_5(self):
        # Paso 5: Escribir un mensaje para el controlador
        message_for_driver = data.message_for_driver
        comment_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//label[@for='comment' and @class='label']"))
        )
        comment_element.click()
        comment_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "comment"))
        )
        comment_input.send_keys(message_for_driver)
        assert comment_input.get_property('value') == message_for_driver

    def test_step_6(self):
        # Paso 6: Pedir una manta y pañuelos
        slider_element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        "#root > div > div.workflow > div.workflow-subcontainer > "
                                        "div.tariff-picker.shown > div.form > div.reqs.open > "
                                        "div.reqs-body > div:nth-child(1) > div > div.r-sw > div > "
                                        "span.slider.round"))
        )
        slider_element.click()
        assert slider_element.is_enabled()
    def test_step_7(self):
        # Paso 7: Pedir 2 helados
        counter_plus_element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='r-counter']//div[@class='counter-plus']"))
        )
        counter_plus_element.click()
        time.sleep(1)
        counter_plus_element.click()
        assert counter_plus_element.is_enabled()
    def test_step_8(self):
        # Paso 8 Modal para buscar un taxi
        taxi_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@class='smart-button-main' and text()='Pedir un taxi']"))
        )
        taxi_button.click()
        assert taxi_button.is_enabled()
        time.sleep(3)
    def test_step_9(self):
        # Paso 9 Mostrar Detalles
        detail_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//img[@src='/static/media/burger.7f0605c2.svg' and @alt='burger']"))
        )
        detail_button.click()
        assert detail_button.is_enabled()
        time.sleep(20)
    @classmethod
    def teardown_class(cls):
        # Cerrar la instancia del navegador al finalizar las pruebas
        cls.driver.quit()
