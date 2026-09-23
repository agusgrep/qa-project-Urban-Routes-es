import data
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages import UrbanRoutesPage
from helpers import retrieve_phone_code


class TestUrbanRoutes:

    driver = None

    def setup_method(self):
        # Configuración moderna compatible con Selenium 4.10+
        options = Options()
        options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})
        self.driver = webdriver.Chrome(options=options)

    # 1. Configurar la dirección
    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        assert routes_page.get_from() == data.address_from
        assert routes_page.get_to() == data.address_to

    # 2. Seleccionar la tarifa Comfort
    def test_choose_comfort(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_order_taxi()
        routes_page.click_comfort_tariff()
        assert routes_page.is_comfort_selected() is True

    # 3. Rellenar el número de teléfono
    def test_fill_phone_number(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_order_taxi()
        routes_page.click_comfort_tariff()

        routes_page.open_phone_modal()
        routes_page.enter_phone_number(data.phone_number)
        sms_code = retrieve_phone_code(self.driver)
        routes_page.enter_sms_code(sms_code)

        assert routes_page.get_phone_number_text() == data.phone_number

    # 4. Agregar una tarjeta de crédito
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

    # 5. Escribir un mensaje para el controlador / conductor
    def test_write_driver_message(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_order_taxi()
        routes_page.click_comfort_tariff()

        routes_page.set_driver_message(data.message_for_driver)
        assert routes_page.get_driver_message() == data.message_for_driver

    # 6. Pedir una manta y pañuelos
    def test_order_blanket_and_tissues(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_order_taxi()
        routes_page.click_comfort_tariff()

        routes_page.click_blanket_switch()
        assert routes_page.is_blanket_switch_selected() is True

    # 7. Pedir 2 helados
    def test_order_two_ice_creams(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_order_taxi()
        routes_page.click_comfort_tariff()

        routes_page.add_ice_creams(2)
        assert routes_page.get_ice_cream_count() == "2"

    # 8. Aparece el modal para buscar un taxi
    def test_search_taxi_modal_appears(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)

        # Flujo previo necesario
        routes_page.set_route(data.address_from, data.address_to)
        routes_page.click_order_taxi()
        routes_page.click_comfort_tariff()

        routes_page.open_phone_modal()
        routes_page.enter_phone_number(data.phone_number)
        sms_code = retrieve_phone_code(self.driver)
        routes_page.enter_sms_code(sms_code)

        routes_page.open_payment_modal()
        routes_page.click_add_card()
        routes_page.fill_card_details(data.card_number, data.card_code)
        routes_page.click_link_card()
        routes_page.close_payment_modal()

        routes_page.set_driver_message(data.message_for_driver)
        routes_page.click_blanket_switch()
        routes_page.add_ice_creams(2)

        # Clic para solicitar taxi
        routes_page.click_smart_order_button()

        # Validación
        assert routes_page.is_order_modal_displayed() is True

    def teardown_method(self):
        self.driver.quit()