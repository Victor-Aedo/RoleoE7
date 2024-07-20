import pyautogui
import time
import threading
import keyboard
import sys

# Configuraciones iniciales y variables globales
MAX_ITERACIONES_SIN_ENCONTRAR_COVENANT = 5
initial_position = {'x': 1197, 'y': 639}
button_cancel_position = {'x': 823, 'y': 662}
button_actualizar = {'x': 356, 'y': 1001}
button_confirm_rol = {'x': 1091, 'y': 664}
total_covenant_purchased = 0
total_mystics_purchased = 0
ejecutar_ciclo = False
total_roleos = 0

# Función para buscar Covenant-3.png
def buscar_coin():
    global total_covenant_purchased, total_mystics_purchased, ejecutar_ciclo
    covenant = None
    mystics = None

    def buscar_covenant():
        nonlocal covenant
        try:
            covenant = pyautogui.locateOnScreen('app/src/imagenes/Covenant-3.png', grayscale=False, confidence=0.95)
        except Exception as e:
            print('Error buscando covenant:', e)

    def buscar_mystics():
        nonlocal mystics
        try:
            mystics = pyautogui.locateOnScreen('app/src/imagenes/Mystrics-3.png', grayscale=False, confidence=0.95)
        except Exception as e:
            print('Error buscando mystics:', e)

    for iteracion in range(MAX_ITERACIONES_SIN_ENCONTRAR_COVENANT):
        covenant = None
        mystics = None
        
        print(f'Iteración: {iteracion + 1}')

        if not ejecutar_ciclo:
            break

        thread_covenant = threading.Thread(target=buscar_covenant)
        thread_mystics = threading.Thread(target=buscar_mystics)

        thread_covenant.start()
        thread_mystics.start()

        thread_covenant.join()
        thread_mystics.join()

        if not (covenant, mystics):
            pass  

        if covenant:
            print("COVENANT ENCONTRADA!!")
            result = comprar_moneda(covenant)
            if result == True:
                total_covenant_purchased+= 1 
                covenant = None 
                

        if mystics:
            
            result = comprar_moneda(mystics)
            if result == True:
                total_mystics_purchased+= 1
                mystics = None
                   
        if iteracion == 2:
            mouse_down()


      
            



# Función para simular un clic sostenido
def mouse_down():
    pyautogui.mouseDown(button='left', x=initial_position['x'], y=initial_position['y'])
    pyautogui.moveTo(x=initial_position['x'], y=initial_position['y'] - 300, duration=0.2)
    time.sleep(0.2)
    pyautogui.mouseUp(button='left')

# Función para realizar la acción de "roleo"
def roleo():
    global total_roleos
    pyautogui.click(button_actualizar['x'], button_actualizar['y'])
    time.sleep(0.3)
    pyautogui.click(button_confirm_rol['x'], button_confirm_rol['y'])
    total_roleos+= 1

# Función para eliminar compras equivocadas
def eliminar_compras_equivocadas():
    try:
        confirm_prese_button = pyautogui.locateOnScreen('app/src/imagenes/Button-Cancel.png', grayscale=False, confidence=0.95)
        if confirm_prese_button:
            x, y = pyautogui.center(confirm_prese_button)
            pyautogui.click(x, y)
    except Exception as e:
        print('Error eliminando compras equivocadas:', e)

# Función para realizar la compra de la moneda encontrada
def comprar_moneda(coin):
    x, y, width, height = coin
    punto_mas_bajo_x = x + width / 2
    punto_mas_bajo_y = y + height

    pyautogui.click(punto_mas_bajo_x + 850, punto_mas_bajo_y)
    time.sleep(0.1)

    try:
        confirm_prese_button = pyautogui.locateOnScreen('app/src/imagenes/Button-Cancel.png', grayscale=False, confidence=0.95)
    except Exception as e:
        print('Error buscando botón de compra:', e)
        
        return False

    if confirm_prese_button:
        time.sleep(0.1)
        pyautogui.click(1056, 756)
        time.sleep(0.1)
        print('Moneda comprada')
        punto_mas_bajo_x = None
        punto_mas_bajo_y = None
        return True

    # else:
    #     pyautogui.click(button_cancel_position['x'], button_cancel_position['y'])  
    #     time.sleep(0.1)
        

    # eliminar_compras_equivocadas()




# Función para iniciar/detener el ciclo cuando se presiona la tecla "t"
def toggle_ciclo():
    global ejecutar_ciclo
    ejecutar_ciclo = not ejecutar_ciclo
    if ejecutar_ciclo:
        print('Roleo Iniciado')
        while True:
            if ejecutar_ciclo:
                buscar_coin()
                time.sleep(0.1)
                roleo()
    else:
        print('Roleo Detenido')
        print("Covenant compradas: ", total_covenant_purchased)
        print("Mystics compradas: ", total_mystics_purchased)
        print("Total Roleos: ", total_roleos)
        print(f"Skystone gasta: {total_roleos * 3}")


# Función para detener el script cuando se presiona la tecla "escape"
def detener_script():
    global ejecutar_ciclo
    ejecutar_ciclo = False
    print('Total de Covenant compradas:', total_covenant_purchased)
    print('Total de Mystic compradas:', total_mystics_purchased)
    print('Programa Finalizado')
    sys.exit()

# Configurar teclas
keyboard.on_press_key("esc", lambda _: detener_script())
keyboard.on_press_key("t", lambda _: toggle_ciclo())

# Ciclo principal
# ejecutar_ciclo = False
time.sleep(1)
toggle_ciclo()  # Inicia el ciclo al ejecutar el script