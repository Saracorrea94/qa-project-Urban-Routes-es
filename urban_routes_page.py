#urban_routes_page.py
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

class UrbanRoutesPage:
    # Localizadores
    from_field = (By.ID, "from")
    to_field = (By.ID, "to")

    # Botón "Pedir un taxi"
    request_btn = (By.CLASS_NAME, "round")

    # Tarifa Comfort (no tiene ID, así que usamos clase)
    comfort_tariff = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[1]/div[5]')

    # Campo visual "Número de teléfono" (antes de que aparezca el input real)
    phone_field_button = (By.CLASS_NAME, "np-button")

    # Campo input real para ingresar el teléfono
    phone_field = (By.ID, "phone")

    # Código para teléfono
    phone_code_field = (By.ID, "code")

    # Botón "Siguiente" en el formulario del teléfono
    next_btn = (By.CLASS_NAME, "full")

    #Boton confirmar cuando se envia codigo
    confirm_code_button = (By.CSS_SELECTOR, "button[type='submit'].button.full")

    # Botón método de pago
    payment_method_btn = (By.CLASS_NAME, "pp-button")

    # Botón "+" para agregar tarjeta
    add_card = (By.CLASS_NAME, "pp-plus")

    # Input número de tarjeta
    card_num = (By.ID, "number")

    # Input código de tarjeta (CVV)
    card_cvv = (By.ID, "code")

    #Agregar tarjeta con campos completos
    add_card_btn = (By.XPATH, "//button[text()='Agregar']")

    #Clic por fuera
    card_wrapper = (By.CSS_SELECTOR, "div.card-wrapper")

    #Cerrar después de agregar tarjeta
    card_modal = (By.CSS_SELECTOR, ".section.unusual")
    close_button = (By.CSS_SELECTOR, ".section.unusual .close-button")

    # Preferencias
    comment_field = (By.ID, "comment")
    blanket_checkbox = (By.CSS_SELECTOR, "div.r-sw div.switch span.slider.round")
    add_ice_cream_button = (By.XPATH, '//div[text()="Helado"]/following-sibling::div//div[@class="counter-plus"]')

    #Clic en boton pedir un taxi.
    confirm_btn_taxi = (By.CLASS_NAME, "smart-button")

    #Cuadro espera assignation conductor.
    wait_for_modal = (By.CLASS_NAME, "order-header-title")

    #Información de conductor.
    driver_info = (By.CLASS_NAME, "order-header-title")

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait   = WebDriverWait(driver, timeout)

    def wait_for_element(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def open(self, url):
        self.driver.get(url)

    def set_from(self, from_address):
        from_input = self.wait_for_element(self.from_field)
        from_input.clear()
        from_input.send_keys(from_address)

    def set_to(self, to_address):
        to_input = self.wait_for_element(self.to_field)
        to_input.clear()
        to_input.send_keys(to_address)

    def get_from(self):
            return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
            return self.driver.find_element(*self.to_field).get_property('value')

    #Completa los campos 'Desde' y 'Hasta' con las direcciones proporcionadas.
    def set_route(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)

    # Botón pedir taxi
    def click_request_taxi_button(self):
        request_btn = self.wait.until(EC.element_to_be_clickable(self.request_btn))
        request_btn.click()

    # Seleccionar tarifa comfort
    def select_comfort_tariff(self):
        self.driver.find_element(*self.comfort_tariff).click()

    # Seleccionar campo numero de teléfono
    def open_phone_modal(self):
        self.driver.find_element(*self.phone_field_button).click()

    # Cuadro rellenar numero de teléfono
    def enter_phone_number_in_modal(self, phone_number):
        input_field = self.driver.find_element(*self.phone_field)
        input_field.send_keys(phone_number)

    # Confirmar código numero de teléfono
    def submit_confirmation_code(self):
        # Espera que el botón esté presente y clickeable
        confirm_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Confirmar']")))
        # Desplaza el botón a la vista (por si hay scroll)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", confirm_button)
        time.sleep(0.5)  # breve pausa opcional por si hay transición
        confirm_button.click()

    #Obtiene automáticamente el código desde los logs y lo ingresa en el campo correspondiente.
    def fill_phone_code(self):
        from main import retrieve_phone_code
        code = retrieve_phone_code(self.driver)
        input_field = self.wait_for_element(self.phone_code_field)
        input_field.send_keys(code)
        input_field.send_keys(Keys.TAB)

    #Envía el número de teléfono ingresado.
    def submit_phone_number(self):
        self.driver.find_element(*self.next_btn).click()

    #Abre el formulario para ingresar una nueva tarjeta.
    def fill_card_number(self):
        self.driver.find_element(*self.payment_method_btn).click()

    #Agregar datos de tarjeta.
    def add_credit_card(self, number, code):
        self.wait_for_element(self.add_card).click()
        self.wait_for_element(self.card_num).send_keys(number)
        elems = self.driver.find_elements(*self.card_cvv)
        for elem in elems:
            if elem.is_displayed():
                elem.send_keys(code)
                break
        # Ahora sí, quitar el foco haciendo clic en el div general
        self.driver.find_element(*self.card_wrapper).click()
        self.wait_for_element(self.add_card_btn).click()
        # Esperar y cerrar la ventana/modal
        close_btn = self.wait.until(EC.presence_of_element_located(self.close_button))
        self.driver.execute_script("arguments[0].click();", close_btn)
        # Esperar a que el modal desaparezca completamente
        self.wait.until(EC.invisibility_of_element_located(self.card_modal))


    #Escribe un mensaje personalizado para el conductor.
    def write_message_for_driver(self, message):
        wait = WebDriverWait(self.driver, 10)
        elem = wait.until(EC.element_to_be_clickable(self.comment_field))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elem)
        elem.send_keys(message)

    #Selecciona manta y pañuelos en la sección de preferencias.
    def request_blanket_and_tissues(self):
        wait = WebDriverWait(self.driver, 10)
        # Esperar que el slider sea clickable
        slider = wait.until(EC.element_to_be_clickable(self.blanket_checkbox))
        # Hacer scroll hasta el toggle para asegurarse que esté visible
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", slider)
        # Click en el slider para activar el toggle
        slider.click()

    #Solicita helados (por defecto 2) desde la sección de preferencias.
    def request_ice_cream(self, quantity=2):
        for _ in range(quantity):
            wait = WebDriverWait(self.driver, 10)
            elem = wait.until(EC.element_to_be_clickable(self.add_ice_cream_button))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elem)
            elem.click()

    #Confirmar pedir taxi.
    def click_phone_and_reserve_button(self):
        self.driver.find_element(*self.confirm_btn_taxi).click()

    #Espera a que aparezca el modal de búsqueda de automóvil.
    def wait_for_searching_modal(self):
        self.wait.until(EC.text_to_be_present_in_element(self.wait_for_modal, "Buscar automóvil"))

    #Espera a que aparezca el modal con la información del conductor.
    def wait_for_driver_info_modal(self):
        WebDriverWait(self.driver, 60).until(EC.text_to_be_present_in_element((By.CLASS_NAME, "order-header-title"), "El conductor llegará en"))

    #Funciones de validación
    def is_tariff_selected(self):
        el = self.driver.find_element(*self.comfort_tariff)
        clases = el.get_attribute("class")
        return "selected" in clases or "active" in clases

    def is_route_set(self, from_address, to_address):
        from_value = self.driver.find_element(*self.from_field).get_property("value")
        to_value = self.driver.find_element(*self.to_field).get_property("value")
        return from_value == from_address and to_value == to_address

    def is_searching_modal_visible(self):
        try:
            el = self.driver.find_element(*self.wait_for_modal)
            return el.is_displayed() and "Buscar automóvil" in el.text
        except NoSuchElementException:
            return False

    def is_driver_info_modal_visible(self):
        try:
            el = self.driver.find_element(*self.wait_for_modal)
            return el.is_displayed() and "El conductor llegará en" in el.text
        except NoSuchElementException:
            return False