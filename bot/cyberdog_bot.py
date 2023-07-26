import requests
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

bot = telebot.TeleBot("6232502522:AAHBAp0kzacaDXMjrf9Q0bak6eHK-QiAh0k")


# Manejador para el comando /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id,
                     "Hola soy Cyberdog, tu asistente Canino. Presiona /salud para consultar los síntomas")


# Manejador para el comando /salud
@bot.message_handler(commands=['salud'])
def show_symptoms_menu(message):
    markup = create_inline_keyboard_markup()  # Crea el markup con los botones
    bot.send_message(message.chat.id, "¡Hola! Soy CyberDog. ¿Qué síntomas quieres consultar?", reply_markup=markup)


# Función para crear el markup con los botones
def create_inline_keyboard_markup():
    markup = InlineKeyboardMarkup(row_width=2)  # número de botones por fila

    # Definir los botones y sus respectivos callback_data
    buttons = [
        ("Estado físico", "estado_fisico"),
        ("Humedad y temperatura", "humedad_temperatura_corporal"),
        ("Calidad de aire", "calidad_aire"),
        ("Frecuencia cardíaca", "frecuencia_cardiaca"),
        ("Reportes", "https://www.animalesbog.gov.co/content/reporte-diario-gestion"),
        ("Cerrar", "cerrar")
    ]

    # Agregar los botones al markup
    for label, callback_data in buttons:
        if label == "Reportes":
            markup.add(InlineKeyboardButton(label, url=callback_data))
        else:
            markup.add(InlineKeyboardButton(label, callback_data=callback_data))

    return markup


# Manejador para los botones del menú
# Función para obtener y mostrar los datos del servicio REST
def get_and_show_data(call, url):
    try:
        response = requests.get(url)

        if response.status_code == 200:
            bot.send_message(call.message.chat.id, f"Respuesta del servicio: {response.json()}")
        else:
            bot.send_message(call.message.chat.id, "Ocurrió un error al obtener los datos.")
    except Exception as e:
        bot.send_message(call.message.chat.id, f"Error al obtener los datos: {e}")


# Manejador para los botones del menú
@bot.callback_query_handler(func=lambda call: True)
def handle_button_click(call):
    cid = call.from_user.id
    mid = call.message.id

    if call.data == "cerrar":
        try:
            bot.delete_message(cid, mid)
            # Aquí puedes realizar las acciones necesarias antes de cerrar el programa
            # Por ejemplo, guardar información, finalizar tareas, etc.
            bot.stop_polling()
        except telebot.apihelper.ApiException as e:
            # Manejar la excepción cuando no se puede eliminar el mensaje
            print(f"Error al intentar eliminar el mensaje: {e}")
            bot.send_message(cid, "No se pudo eliminar el mensaje. Inténtalo nuevamente más tarde.")

    elif call.data == "estado_fisico":
        get_and_show_data(call, "http://monitoring-api:5001/mpu6050")

    elif call.data == "humedad_temperatura_corporal":
        get_and_show_data(call, "http://monitoring-api:5001/dht11")

    elif call.data == "calidad_aire":
        get_and_show_data(call, "http://monitoring-api:5001/mq135")

    elif call.data == "frecuencia_cardiaca":
        get_and_show_data(call, "http://monitoring-api:5001/xd58c")


# Iniciar el bot
if __name__ == "__main__":
    bot.polling()
