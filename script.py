import sqlite3
import telebot
import requests

BOT_TOKEN = '699552035:AAH1ZX8ctxAAlpt3khZXQzDieeH1iLXoKy0'

HERE_TOKEN_ID   = 'x117QOJHwsz2511ozAGX'
HERE_TOKEN_CODE = 'uJ42APkWYcZWX_vkL0tRcQ'

SPHERES = [
	'IT',
	'Building'
]

bot = telebot.TeleBot(BOT_TOKEN)

main_str = "SELECT * from wp_vac "
not_main_str = "sElEcT * FroM wp_course "

def format_vacs(all_vacs):
	vacancies = []
	for vacancy in all_vacs:
		vacancies.append({'title': vacancy[1], 'salary': vacancy[5], 'employer': vacancy[4], 'sphere': vacancy[7], 'id': vacancy[0]})
	return vacancies

def print_vac(vac):
	return '*' + vac[1] + '*\n' + str(vac[5]) + '\n_' + vac[7] +'_\nПодробнее: наберите "`Вакансия' + str(vac[0]) + '`" без кавычек'

def print_vac2(vac):
	return '*' + vac['title'] + '*\n' + str(vac['salary']) + '\n_' + vac['sphere'] +'_\nПодробнее: наберите "`Вак' + str(vac['id']) + '`" без кавычек'

def getAll():
	conn = sqlite3.connect('db.sqlite3')
	c = conn.cursor()
	c.execute(main_str)
	return c.fetchall()

def getBySphere(sphere):
	conn = sqlite3.connect('db.sqlite3')
	c = conn.cursor()
	c.execute(main_str + 'where sphere=\'' + sphere + '\'')
	return format_vacs(c.fetchall())

def getById(id):
	conn = sqlite3.connect('db.sqlite3')
	c = conn.cursor()
	c.execute(main_str + 'where id=' + id)
	return c.fetchall()

def notGetAll():
	conn = sqlite3.connect('db.sqlite3')
	c = conn.cursor()
	c.execute(not_main_str)
	return c.fetchall()

def notGetById(id):
	conn = sqlite3.connect('db.sqlite3')
	c = conn.cursor()
	c.execute(not_main_str + 'where id=' + id)
	return c.fetchall()

def print_course_short(message, course):
	bot.send_message(
		message.chat.id,
		'*' + course[1] + '*\n' + course[2] + '\n_Подробнее: наберите "_`Курс' + str(course[0]) + '`_" без кавычек_',
		parse_mode = 'Markdown'
	)

def print_course_full(message, course):
	bot.send_message(
		message.chat.id,
		'*' + course[1] + '*\n' + course[3] + '\n_' + course[2] + '_',
		parse_mode = 'Markdown'
	)

def printBySphere(message):
	for elem in getBySphere(message.text):
		bot.send_message(message.chat.id, print_vac2(elem), parse_mode = 'Markdown')

@bot.message_handler(commands = ['start'])
def test_bot(message):
	markup = telebot.types.ReplyKeyboardMarkup()
	buttonAll = telebot.types.KeyboardButton('Все')
	buttonCrs = telebot.types.KeyboardButton('Курсы')
	buttonTwo = telebot.types.KeyboardButton('IT')
	buttonTri = telebot.types.KeyboardButton('Building')
	markup.row(buttonAll, buttonCrs)
	markup.row(buttonTwo, buttonTri)
	bot.send_message(message.chat.id, "Здравствуйте!\nЯ могу вам:\nувидеть все имеющиеся у нас вакансии,\nувидеть вакансии в определенной категории\nи узнать, где находятся ближайшие центры занятости населения.\nДля того, чтобы узнать, где же находятся ближайшие ЦЗН, просто отправьте мне свое местоположение.", reply_markup = markup)

@bot.message_handler(commands = ['all'])
def allVacs(message):
	for elem in getAll():
		bot.send_message(message.chat.id, print_vac(elem), parse_mode = 'Markdown')

@bot.message_handler(commands = ['courses'])
def courses(message):
	conn = sqlite3.connect('db.sqlite3')
	c = conn.cursor()
	c.execute(not_main_str)
	for elem in c.fetchall():
		print_course_short(message, elem)

# @bot.message_handler(commands = ['kill'])
# def kill(message):
# 	bot.send_message(message.chat.id, "You have killed me. x_x")
# 	print("5" / 0)

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

@bot.message_handler(content_types = ['text'])
def handle_text(message):
	if message.text == 'Все':
		for elem in getAll():
			bot.send_message(message.chat.id, print_vac(elem), parse_mode = 'Markdown')

	elif message.text[:3] == 'Вак':
		try:
			id = message.text[3:]
			responce = getById(str(int(id)))
			result = '*' + responce[0][1] + '*, ' + str(responce[0][5]) + ' тенге\n' + responce[0][3] + '\n_Опубликовано в сфере ' + responce[0][7] + ' компанией ' + responce[0][4] + '_\n*Требования:* ' + responce[0][6]
			bot.send_message(message.chat.id, result, parse_mode = 'Markdown')
		except Exception as ex:
			print(ex)
			bot.send_message(message.chat.id, "Такой вакансии нет!")
		
	elif message.text in SPHERES:
		printBySphere(message)
	
	elif message.text == 'Курсы':
		courses(message)
	
	elif message.text[:4] == 'Курс':
		try:
			id = message.text[4:]
			responce = notGetById(id)
			print_course_full(message, responce[0])
		except Exception as ex:
			print(ex)
			bot.send_message(message.chat.id, "Такого курса нет!")

	else:
		test_bot(message)

bot.polling()