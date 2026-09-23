from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class UrbanRoutesPage:
    # --- Localizadores Paso 1: Ruta ---
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')

    # --- Localizadores Paso 2: Comfort ---
    order_taxi_button = (By.CSS_SELECTOR, "button.button.round")
    comfort_button = (By.XPATH, "//div[text()='Comfort']")

    # --- Localizadores Paso 3: Teléfono ---
    phone_field_button = (By.XPATH, "//div[text()='Número de teléfono']")
    phone_input = (By.ID, "phone")
    phone_submit_button = (By.XPATH, "//button[text()='Siguiente']")
    sms_code_input = (By.ID, "code")
    sms_confirm_button = (By.XPATH, "//button[text()='Confirmar']")
    phone_number_value = (By.XPATH, "//div[@class='np-text']")

    # --- Localizadores Paso 4: Tarjeta ---
    payment_method_button = (By.XPATH, "//div[@class='pp-text']")
    add_card_button = (By.XPATH, "//div[@class='pp-title' and text()='Agregar tarjeta']")
    card_number_input = (By.ID, "number")
    card_code_input = (By.ID, "code")
    link_card_button = (By.XPATH, "//button[text()='Enlace' or text()='Vincular']")
    close_payment_modal_button = (By.XPATH, "//div[@class='payment-picker open']//button[@class='close-button section-close']")
    payment_method_value = (By.CLASS_NAME, "pp-value-text")

    # --- Localizadores Pasos 5, 6, 7 y 8 ---
    comment_input = (By.ID, "comment")
    blanket_switch = (By.XPATH, "//div[text()='Manta y pañuelos']/..//span[contains(@class, 'slider')]")
    blanket_checkbox = (By.XPATH, "//div[text()='Manta y pañuelos']/..//input[@class='switch-input']")
    ice_cream_plus_button = (By.XPATH, "(//div[@class='counter-plus'])[1]")
    ice_cream_value = (By.XPATH, "(//div[@class='counter-value'])[1]")
    order_taxi_smart_button = (By.CLASS_NAME, "smart-button")
    order_modal_header = (By.XPATH, "//div[contains(@class, 'order-header') or contains(@class, 'order-body')]")

    def __init__(self, driver):
        self.driver = driver

    # --- Métodos de Ruta ---
    def set_from(self, from_address):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(self.from_field)
        ).send_keys(from_address)

    def set_to(self, to_address):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(self.to_field)
        ).send_keys(to_address)

    def set_route(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)

    def get_from(self):
        return WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(self.from_field)
        ).get_property('value')

    def get_to(self):
        return WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(self.to_field)
        ).get_property('value')

    # --- Métodos de Tarifa Comfort ---
    def click_order_taxi(self):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(self.order_taxi_button)
        ).click()

    def click_comfort_tariff(self):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(self.comfort_button)
        ).click()

    def is_comfort_selected(self) -> bool:
        comfort_element = WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located(self.comfort_button)
        )
        parent_container = comfort_element.find_element(By.XPATH, "./..")
        return "active" in (parent_container.get_attribute("class") or "")

    # --- Métodos de Teléfono ---
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

    # --- Métodos de Tarjeta ---
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

    # --- Métodos de Requisitos ---
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

    # --- Métodos de Modal Final ---
    def click_smart_order_button(self):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(self.order_taxi_smart_button)
        ).click()

    def is_order_modal_displayed(self) -> bool:
        modal = WebDriverWait(self.driver, 10).until(
            expected_conditions.visibility_of_element_located(self.order_modal_header)
        )
        return modal.is_displayed()