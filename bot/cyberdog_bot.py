import telebot
from telebot.types import InlineKeyboardButton
from telebot.types import InlineKeyboardMarkup

bot = telebot.TeleBot("6232502522:AAHBAp0kzacaDXMjrf9Q0bak6eHK-QiAh0k")


@bot.message_handler(commands=['start'])
def send(message):
    bot.send_message(message.chat.id,
                     "Hola soy Cyberdog tu asistente Canino, presiona /salud para consultar los sintomas")


@bot.message_handler(commands=['salud'])
def cmd_button(message):
    markup = InlineKeyboardMarkup(row_width=2)  # número de botones por fila
    b1 = InlineKeyboardButton("Estado físico", callback_data="estado_fisico")
    b2 = InlineKeyboardButton("Humedad corporal", callback_data="humedad_corporal")
    b3 = InlineKeyboardButton("Calidad de aire", callback_data="calidad_aire")
    b4 = InlineKeyboardButton("Frecuencia cardíaca", callback_data="frecuencia_cardiaca")
    b5 = InlineKeyboardButton("Temperatura corporal", callback_data="temperatura_corporal")
    b6 = InlineKeyboardButton("Reportes", url="https://www.animalesbog.gov.co/content/reporte-diario-gestion ")
    b_cerrar = InlineKeyboardButton("Cerrar", callback_data="cerrar")
    markup.add(b1, b2, b3, b4, b5, b6, b_cerrar)
    bot.send_message(message.chat.id, "Hola ¡soy CyberDog! ¿Cuales sintomas quieres consultar?", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def response_buttons_inline(call):
    cid = call.from_user.id
    mid = call.message.id
    if call.data == "cerrar":
        bot.delete_message(cid, mid)
        # Aquí puedes realizar las acciones necesarias antes de cerrar el programa
        # Por ejemplo, guardar información, finalizar tareas, etc.
        bot.stop_polling()


bot.polling()
