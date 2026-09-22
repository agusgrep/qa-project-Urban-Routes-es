import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
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
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    #opcion comfort
    order_taxi_button = (By.CSS_SELECTOR, "button.button.round")
    comfort_button = (By.XPATH, "//div[text()='Comfort']")
    #opcion telefono
    phone_field_button = (By.XPATH, "//div[text()='Número de teléfono']")
    phone_input = (By.ID, "phone")
    phone_submit_button = (By.XPATH, "//button[text()='Siguiente']")
    sms_code_input = (By.ID, "code")
    sms_confirm_button = (By.XPATH, "//button[text()='Confirmar']")
    phone_number_value = (By.XPATH, "//div[@class='np-text']")
    #opcion tarjeta
    payment_method_button = (By.XPATH, "//div[@class='pp-text']")
    add_card_button = (By.XPATH, "//div[@class='pp-title' and text()='Agregar tarjeta']")
    card_number_input = (By.ID, "number")
    card_code_input = (By.ID, "code")
    link_card_button = (By.XPATH, "//button[text()='Enlace' or text()='Vincular']")
    close_payment_modal_button = (By.XPATH,
                                  "//div[@class='payment-picker open']//button[@class='close-button section-close']")
    payment_method_value = (By.CLASS_NAME, "pp-value-text")
    #localizadores para ultimos pasos
    comment_input = (By.ID, "comment")
    blanket_switch = (By.XPATH, "//div[text()='Manta y pañuelos']/..//span[contains(@class, 'slider')]")
    blanket_checkbox = (By.XPATH, "//div[text()='Manta y pañuelos']/..//input[@class='switch-input']")
    ice_cream_plus_button = (By.XPATH, "(//div[@class='counter-plus'])[1]")
    ice_cream_value = (By.XPATH, "(//div[@class='counter-value'])[1]")
    order_taxi_smart_button = (By.CLASS_NAME, "smart-button")
    order_modal_header = (By.XPATH, "//div[contains(@class, 'order-header') or contains(@class, 'order-body')]")

    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')
    #unificar metodos para la ruta pasos
    def set_route(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)
    #Metodos para esperar y clickear la tarifa comfort
    def click_order_taxi(self):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(self.order_taxi_button)
        ).click()

    def click_comfort_tariff(self):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(self.comfort_button)
        ).click()

    def is_comfort_selected(self) -> bool:
        # Busca el botón Comfort, sube al contenedor padre directo (..) y verifica si tiene la clase 'active'
        comfort_element = WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located(self.comfort_button)
        )
        parent_container = comfort_element.find_element(By.XPATH, "./..")
        return "active" in (parent_container.get_attribute("class") or "")
    #metodo para el telefono
    def open_phone_modal(self):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(self.phone_field_button)
        ).click()

    def enter_phone_number(self, phone_number):
        input_elem = WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(self.phone_input)
        )
        input_elem.send_keys(phone_number)
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(self.phone_submit_button)
        ).click()

    def enter_sms_code(self, sms_code):
        code_elem = WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(self.sms_code_input)
        )
        code_elem.send_keys(sms_code)
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(self.sms_confirm_button)
        ).click()

    def get_phone_number_text(self):
        return WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(self.phone_number_value)
        ).text
    #tarjeta de credito
    def open_payment_modal(self):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(self.payment_method_button)
        ).click()

    def click_add_card(self):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(self.add_card_button)
        ).click()

    def fill_card_details(self, card_number, card_code):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(self.card_number_input)
        ).send_keys(card_number)

        code_field = WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(self.card_code_input)
        )
        code_field.send_keys(card_code)
        # Quita el foco con TAB para habilitar el botón Enlace/Vincular
        code_field.send_keys(Keys.TAB)

    def click_link_card(self):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(self.link_card_button)
        ).click()

    def close_payment_modal(self):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(self.close_payment_modal_button)
        ).click()

    def get_selected_payment_text(self):
        return WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(self.payment_method_value)
        ).text

    def set_driver_message(self, message):
        input_elem = WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(self.comment_input)
        )
        input_elem.send_keys(message)

    def get_driver_message(self):
        return self.driver.find_element(*self.comment_input).get_property('value')

    def click_blanket_switch(self):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(self.blanket_switch)
        ).click()

    def is_blanket_switch_selected(self) -> bool:
        checkbox = self.driver.find_element(*self.blanket_checkbox)
        return checkbox.is_selected()

    def add_ice_creams(self, count=2):
        plus_btn = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(self.ice_cream_plus_button)
        )
        for _ in range(count):
            plus_btn.click()

    def get_ice_cream_count(self) -> str:
        return WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(self.ice_cream_value)
        ).text

    # --- Métodos de Pedido Final y Modal ---
    def click_smart_order_button(self):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(self.order_taxi_smart_button)
        ).click()

    def is_order_modal_displayed(self) -> bool:
        modal = WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(self.order_modal_header)
        )
        return modal.is_displayed()

class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome(desired_capabilities=capabilities)

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    def test_choose_comfort(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)

        routes_page.click_order_taxi()
        routes_page.click_comfort_tariff()

        assert routes_page.is_comfort_selected() is True
    #rellenar numero de telefono
    def test_fill_phone_number(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_order_taxi()
        routes_page.click_comfort_tariff()

        routes_page.open_phone_modal()
        routes_page.enter_phone_number(data.phone_number)

        # Intercepta el SMS tras solicitarlo y lo ingresa
        sms_code = retrieve_phone_code(self.driver)
        routes_page.enter_sms_code(sms_code)

        assert routes_page.get_phone_number_text() == data.phone_number

    #agregar tarjeta de credito
    def test_add_credit_card(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_order_taxi()
        routes_page.click_comfort_tariff()

        routes_page.open_payment_modal()
        routes_page.click_add_card()
        routes_page.fill_card_details(data.card_number, data.card_code)
        routes_page.click_link_card()
        routes_page.close_payment_modal()

        assert "Tarjeta" in routes_page.get_selected_payment_text()
    #mensaje para conductor
    def test_write_driver_message(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_order_taxi()
        routes_page.click_comfort_tariff()

        routes_page.set_driver_message(data.message_for_driver)
        assert routes_page.get_driver_message() == data.message_for_driver
    #pedir manta y pañuelos
    def test_order_blanket_and_tissues(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_order_taxi()
        routes_page.click_comfort_tariff()

        routes_page.click_blanket_switch()
        assert routes_page.is_blanket_switch_selected() is True
    #pedir 2 helados
    def test_order_two_ice_creams(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_order_taxi()
        routes_page.click_comfort_tariff()

        routes_page.add_ice_creams(2)
        assert routes_page.get_ice_cream_count() == "2"
    #llamada a todos los metodos
    def test_search_taxi_modal_appears(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)

        # Ruta y Tarifa
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_order_taxi()
        routes_page.click_comfort_tariff()

        # Teléfono
        routes_page.open_phone_modal()
        routes_page.enter_phone_number(data.phone_number)
        sms_code = retrieve_phone_code(self.driver)
        routes_page.enter_sms_code(sms_code)

        # Tarjeta
        routes_page.open_payment_modal()
        routes_page.click_add_card()
        routes_page.fill_card_details(data.card_number, data.card_code)
        routes_page.click_link_card()
        routes_page.close_payment_modal()

        # Requisitos
        routes_page.set_driver_message(data.message_for_driver)
        routes_page.click_blanket_switch()
        routes_page.add_ice_creams(2)

        # Pedir taxi
        routes_page.click_smart_order_button()

        # Validación
        assert routes_page.is_order_modal_displayed() is True

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
