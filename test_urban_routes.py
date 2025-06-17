#test_urban_routes.py
import data
import helpers
from selenium import webdriver
from urban_routes_page import UrbanRoutesPage

class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        #from selenium.webdriver import DesiredCapabilities
        #capabilities = DesiredCapabilities.CHROME
        #capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        #cls.driver = webdriver.Chrome(desired_capabilities=capabilities)
        from selenium.webdriver.chrome.options import Options
        options = Options()
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        cls.driver = webdriver.Chrome(options=options)


    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.address_from, data.address_to)
        assert helpers.is_route_set(routes_page, data.address_from, data.address_to)

    #Seleccionar la tarifa Comfort.
    def test_select_tariff(self):
        self.driver.get(data.urban_routes_url)
        page = UrbanRoutesPage(self.driver)
        page.set_route(data.address_from, data.address_to)
        page.click_request_taxi_button()
        page.select_comfort_tariff()
        assert helpers.is_tariff_selected(page), "No se seleccionó la tarifa Comfort"


    #Rellenar el número de teléfono.
    def test_enter_phone_number(self):
        self.driver.get(data.urban_routes_url)
        page = helpers.prepare_taxi_request(self.driver)
        page.open_phone_modal()
        page.enter_phone_number_in_modal(data.phone_number)
        page.submit_phone_number()
        assert helpers.get_phone_confirmation_title(page) == "Código de confirmación"

    #Agregar una tarjeta de crédito.
    def test_add_credit_card(self):
        self.driver.get(data.urban_routes_url)
        page = helpers.prepare_taxi_request(self.driver)
        page.fill_card_number()
        page.add_credit_card(data.card_number, data.card_code)
        assert helpers.is_card_added(page), "No se agregó la tarjeta correctamente"

    #Escribir un mensaje para el controlador.
    def test_write_driver_message(self):
        self.driver.get(data.urban_routes_url)
        page = helpers.prepare_taxi_request(self.driver)
        page.write_message_for_driver(data.message_for_driver)
        assert helpers.get_driver_message(page) == data.message_for_driver

    #Pedir una manta y pañuelos.
    def test_request_blanket_and_tissues(self):
        self.driver.get(data.urban_routes_url)
        page = helpers.prepare_taxi_request(self.driver)
        page.request_blanket_and_tissues()
        assert helpers.are_blanket_and_tissues_selected(page), "No se seleccionó manta y pañuelos"

    #Pedir 2 helados.
    def test_request_ice_cream(self):
        self.driver.get(data.urban_routes_url)
        page = helpers.prepare_taxi_request(self.driver)
        page.request_ice_cream(2)
        assert helpers.get_ice_cream_quantity(page) == 2, "No se solicitaron 2 helados"


    def test_searching_modal_appears(self):
        self.driver.get(data.urban_routes_url)
        page = helpers.prepare_full_taxi_request(self.driver)
        page.click_phone_and_reserve_button()
        page.wait_for_searching_modal()
        assert helpers.is_searching_modal_visible(page), "No apareció el modal de búsqueda"

    def test_driver_info_modal_appears(self):
        self.driver.get(data.urban_routes_url)
        page = helpers.prepare_full_taxi_request(self.driver)
        page.click_phone_and_reserve_button()
        page.wait_for_driver_info_modal()
        assert helpers.is_driver_info_modal_visible(page), "No apareció el modal con info del conductor"

    def test_confirm_taxi_request(self):
        self.driver.get(data.urban_routes_url)
        page = helpers.prepare_full_taxi_request(self.driver)
        page.click_phone_and_reserve_button()
        page.wait_for_searching_modal()
        assert helpers.is_searching_modal_visible(page), "No apareció el modal de búsqueda"
        page.wait_for_driver_info_modal()
        assert helpers.is_driver_info_modal_visible(page), "No apareció el modal con info del conductor"

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
