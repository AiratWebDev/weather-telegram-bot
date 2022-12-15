import telebot
from telebot import types
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys #нужно для написания текста
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from key import bot_key

option = webdriver.ChromeOptions()
option.add_argument('headless')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)

weather_bot = telebot.TeleBot(bot_key)


@weather_bot.message_handler(commands=['start'])
def show_weather(message):
    msg = weather_bot.send_message(message.chat.id, text='Привет, в каком городе ты хочешь узнать погоду?')
    weather_bot.register_next_step_handler(msg, city_choosing)


def city_choosing(city):
    weather_bot.send_message(city.chat.id, text='Ищу погоду')
    driver.get('https://www.gismeteo.ru/')
    search = driver.find_element(By.XPATH, value="/html/body/header/div[2]/div[2]/div/div/div[1]/div/input")
    search.send_keys(city.text)
    sleep(0.5)
    search.send_keys(Keys.ARROW_DOWN)  # нажатие на стрелочку для выбора города
    search.send_keys(Keys.ENTER)

    weather = driver.find_element(By.CLASS_NAME, "weather-value")
    weather_bot.send_message(city.chat.id, text=f'Погода в городе {city.text}: {weather.text}°C')


weather_bot.polling(none_stop=True)
