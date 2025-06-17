import data
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from urban_routes_page import UrbanRoutesPage

#Funciones de validación

#Ruta direcciones.
def is_route_set(page, from_address, to_address):
    from_value = page.driver.find_element(*page.from_field).get_property("value")
    to_value = page.driver.find_element(*page.to_field).get_property("value")
    return from_value == from_address and to_value == to_address

#Tarifa seleccionada.
def is_tariff_selected(page):
    el = page.driver.find_element(*page.comfort_tariff)
    clases = el.get_attribute("class")
    return "selected" in clases or "active" in clases

#Numero de confirmación celular.
def get_phone_confirmation_title(page):
    try:
        el = page.driver.find_element_by_class_name("title")
        return el.text.strip()
    except NoSuchElementException:
        return ""

#Tarjeta de credito.
def get_credit_card_title(page):
    try:
        el = page.driver.find_element_by_css_selector(".section.unusual .title")
        return el.text.strip()
    except NoSuchElementException:
        return ""

#Tarjeta de credito agregada.
def is_card_added(page):
    try:
        return page.wait.until(EC.invisibility_of_element_located(page.card_modal))
    except NoSuchElementException:
        return False

#Mensaje al conductor.
def get_driver_message(page):
    try:
        return page.driver.find_element(*page.comment_field).get_attribute("value")
    except NoSuchElementException:
        return ""

#Manta y pañuelos.
def are_blanket_and_tissues_selected(page):
    slider = page.driver.find_element(*page.blanket_checkbox)
    return "checked" in slider.get_attribute("class") or slider.is_selected()

#Helados
def get_ice_cream_quantity(page):
    try:
        counter = page.driver.find_element(By.XPATH, '//div[text()="Helado"]/following-sibling::div//div[@class="counter-value"]')
        return int(counter.text.strip())
    except NoSuchElementException:
        return 0

#Modal de buscar conductor.
def is_searching_modal_visible(page):
    try:
        el = page.driver.find_element(*page.wait_for_modal)
        return el.is_displayed() and "Buscar automóvil" in el.text
    except NoSuchElementException:
        return False

#Modal de confirmación conductor.
def is_driver_info_modal_visible(page):
    try:
        el = page.driver.find_element(*page.wait_for_modal)
        return el.is_displayed() and "El conductor llegará en" in el.text
    except NoSuchElementException:
        return False


#Ayudas para ejecutar tests.
#Volver a llenar los campos de dirección y página.
def prepare_taxi_request(driver):
    page = UrbanRoutesPage(driver)
    page.set_route(data.address_from, data.address_to)
    page.click_request_taxi_button()
    page.select_comfort_tariff()
    return page


# Ultimo pasos
def prepare_full_taxi_request(driver):
    page = prepare_taxi_request(driver)
    page.open_phone_modal()
    page.enter_phone_number_in_modal(data.phone_number)
    page.submit_phone_number()
    page.fill_phone_code()
    page.submit_confirmation_code()
    page.fill_card_number()
    page.add_credit_card(data.card_number, data.card_code)
    page.write_message_for_driver(data.message_for_driver)
    page.request_blanket_and_tissues()
    page.request_ice_cream(2)
    return page