from selenium import webdriver
import time

# Inicialización del controlador de Edge
driver = webdriver.Edge()

driver.get('https://web.whatsapp.com/')
time.sleep(15)  # Espera para escanear el código QR manualmente

# Lógica para encontrar elementos, escribir mensajes y enviarlos
# Por ejemplo, encontrar el campo de búsqueda y escribir el mensaje
search_box = driver.find_element_by_xpath('//div[@class="_3FRCZ copyable-text selectable-text"][@contenteditable="true"][@data-tab="3"]')
search_box.send_keys('Pirdin')
search_box.send_keys(u'\ue007')  # Presiona Enter para enviar el mensaje

# Puedes seguir agregando lógica para interactuar con la interfaz de WhatsApp Web aquí

# Cierra el navegador después de algunos segundos (opcional)
time.sleep(5)
driver.quit()
