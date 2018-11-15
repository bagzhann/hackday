# -*- coding: UTF-8 -*-

import sqlite3
import telebot
import requests

BOT_TOKEN = '699552035:AAH1ZX8ctxAAlpt3khZXQzDieeH1iLXoKy0'

HERE_TOKEN_ID   = 'x117QOJHwsz2511ozAGX'
HERE_TOKEN_CODE = 'uJ42APkWYcZWX_vkL0tRcQ'

SPHERES = [
	'IT',
	'Building',
    'Sphere'
]

GET_VACS_COMMAND = 'SELECT * from wp_vac '
GET_COUR_COMMAND = 'SELECT * from wp_course '

bot = telebot.TeleBot(BOT_TOKEN)

def format_item(item, full = False):
    if full == False:
        if len(item) == 5:
            return (
                '*' +
                item[4] +
                '*, ' +
                item[3] +
                '\n*Курс от* ' +
                item[1] +
                '\n*Подробнее:* введите "Курс ' +
                str(item[0]) +
                '" без кавычек.'
            )
        else:   
            return (
                '*' +
                item[1] +
                '*, ' +
                str(item[5]) +
                '\n*Требования:* ' +
                item[6] +
                '\n*Работодатель:* ' +
                item[4] +
                '\n*Подробнее:* введите "Вакансия ' +
                str(item[0]) +
                '" без кавычек.'
            )
    else:
        if len(item) == 5:
            return (
                '*' +
                item[4] +
                '*, ' +
                item[3] +
                '\n*Описание:* ' +
                item[2] +
                '\n*Контакты:* ' +
                item[1]
            )
        else:
            return (
                '*' +
                item[1] +
                '*, ' +
                str(item[5]) +
                '\n*Описание:* ' +
                item[3] +
                '\n*Требования:* ' +
                item[6] +
                '\n*Работодатель:* ' +
                item[4]
            )

def get_all(get_type):
    return sqlite3.connect('db.sqlite3').cursor().execute(get_type).fetchall()

def get_by_sphere(get_type, sphere):
    return sqlite3.connect('db.sqlite3').cursor().execute(get_type + 'where sphere=\'' + sphere + '\'').fetchall()

def get_by_id(get_type, id):
    return sqlite3.connect('db.sqlite3').cursor().execute(get_type + 'where id=' + id).fetchone()

@bot.message_handler(commands = ['start'])
def start(message):
	markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard = True)
	buttonVacs = telebot.types.KeyboardButton('Вакансии')
	buttonCrs = telebot.types.KeyboardButton('Курсы')
	markup.row(buttonVacs, buttonCrs)
	bot.send_message(message.chat.id, "Здравствуйте!\nЯ могу помочь вам:\nувидеть все имеющиеся у нас вакансии и курсы,\nфильтровать их по категориям\nи узнать, где находятся ближайшие центры занятости населения.\nДля того, чтобы узнать, где же находятся ближайшие ЦЗН, просто отправьте мне свое местоположение.", reply_markup = markup)

@bot.message_handler(commands = ['vacancies'])
def all_vacs(message):
	for elem in get_all(GET_VACS_COMMAND):
		bot.send_message(message.chat.id, format_item(elem), parse_mode = 'Markdown')

@bot.message_handler(commands = ['courses'])
def all_courses(message):
	for elem in get_all(GET_COUR_COMMAND):
		bot.send_message(message.chat.id, format_item(elem), parse_mode = 'Markdown')

@bot.message_handler(content_types = ['text'])
def handle_text(message):
    if message.text == 'Вакансии':
        markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard = True)
        buttonAll = telebot.types.KeyboardButton('Все вакансии')
        buttonIT = telebot.types.KeyboardButton('Вакансии IT')
        buttonBld = telebot.types.KeyboardButton('Вакансии Building')
        buttonSph = telebot.types.KeyboardButton('Вакансии Sphere')
        markup.add(buttonAll, buttonIT, buttonBld, buttonSph)
        bot.send_message(message.chat.id, 'Выберите категорию:', reply_markup = markup)
    elif message.text == 'Все вакансии':
        all_vacs(message)
    elif message.text == 'Курсы':
        markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard = True)
        buttonAll = telebot.types.KeyboardButton('Все курсы')
        buttonIT = telebot.types.KeyboardButton('Курсы IT')
        buttonBld = telebot.types.KeyboardButton('Курсы Building')
        buttonSph = telebot.types.KeyboardButton('Курсы Sphere')
        markup.add(buttonAll, buttonIT, buttonBld, buttonSph)
        bot.send_message(message.chat.id, 'Выберите категорию:', reply_markup = markup)
    elif message.text == 'Все курсы':
        all_courses(message)
    elif message.text[:9] == 'Вакансии ':
        try:
            vacs = get_by_sphere(GET_VACS_COMMAND, message.text[9:])
            for vac in vacs:
                bot.send_message(message.chat.id, format_item(vac), parse_mode = 'Markdown')
        except Exception as ex:
            print(ex)
            bot.send_message(message.chat.id, 'Такой категории нет.')
    elif message.text[:9] == 'Вакансия ':
        try:
            vac = get_by_id(GET_VACS_COMMAND, message.text[9:])
            bot.send_message(message.chat.id, format_item(vac, full = True), parse_mode = 'Markdown')
        except Exception as ex:
            print(ex)
            bot.send_message(message.chat.id, 'Такой вакансии нет.')
    elif message.text[:6] == 'Курсы ':
        try:
            cours = get_by_sphere(GET_COUR_COMMAND, message.text[6:])
            for cour in cours:
                bot.send_message(message.chat.id, format_item(cour), parse_mode = 'Markdown')
        except Exception as ex:
            print(ex)
            bot.send_message(message.chat.id, 'Такой категории нет.')
    elif message.text[:5] == 'Курс ':
        try:
            cour = get_by_id(GET_COUR_COMMAND, message.text[5:])
            bot.send_message(message.chat.id, format_item(cour, full = True), parse_mode = 'Markdown')
        except Exception as ex:
            print(ex)
            bot.send_message(message.chat.id, 'Такого курса нет.')
    elif message.text == 'kill':
        print(5 / 0)
    else:
        start(message)

@bot.message_handler(content_types = ['location'])
def handle_location(message):
	user_location = message.location

	request_parameters = {
		'at': str(user_location.latitude) + ',' + str(user_location.longitude),
		'q': 'Центр Занятости',
		'app_id': HERE_TOKEN_ID,
		'app_code': HERE_TOKEN_CODE
	}

	map_points = requests.get(
		'https://places.cit.api.here.com/places/v1/autosuggest',
		params = request_parameters
	).json()

	i = 0

	while i < 2:
		result_title = map_points['results'][i]['title']
		result_address_raw = map_points['results'][i]['vicinity'].split('<br/>')
		result_address = ''

		for elem in result_address_raw:
			result_address += elem + ' '

		result_coordinates = map_points['results'][i]['position']

		bot.send_venue(
			message.chat.id,
			result_coordinates[0],
			result_coordinates[1],
			result_title,
			result_address
		)

		i += 1

bot.polling()