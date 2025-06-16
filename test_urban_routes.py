#test_urban_routes.py
import data
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
        assert routes_page.get_from() == data.address_from
        assert routes_page.get_to() == data.address_to

    def test_full_taxi_request(self):
        self.driver.get(data.urban_routes_url)
        page = UrbanRoutesPage(self.driver)

        # Dirección
        page.set_route(data.address_from, data.address_to)
        assert page.is_route_set(data.address_from, data.address_to), "La ruta no está preparada"

        # Pedir taxi y seleccionar tarifa
        page.click_request_taxi_button()
        page.select_comfort_tariff()
        assert page.is_tariff_selected(), "No se seleccionó la tarifa comfort"

        # Teléfono
        page.open_phone_modal()
        page.enter_phone_number_in_modal(data.phone_number)
        page.submit_phone_number()

        # Código de confirmación
        page.fill_phone_code()
        page.submit_confirmation_code()

        # Agregar tarjeta
        page.fill_card_number()
        page.add_credit_card(data.card_number, data.card_code)

        # Mensaje para conductor
        page.write_message_for_driver(data.message_for_driver)

        # Pedir manta/pañuelos
        page.request_blanket_and_tissues()

        # Pedir 2 helados
        page.request_ice_cream(2)

        #Confirmar el pedido haciendo clic en el botón "Introducir un número de teléfono y reservar"
        page.click_phone_and_reserve_button()

        # Espera a que aparezca el modal "Buscar automóvil"
        page.wait_for_searching_modal()
        assert page.is_searching_modal_visible(), "No apareció el modal de búsqueda"

        # Espera a que se actualice con la información del conductor
        page.wait_for_driver_info_modal()
        assert page.is_driver_info_modal_visible(), "No apareció el modal con info del conductor"

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
