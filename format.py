from bs4 import BeautifulSoup as Soup
import re

def format_html():
	foldername = ''
	print('Открытие файла...')
	try:
		with open('index.html', 'r', encoding='utf-8') as source:
			html = source.read()
		print('ok')
	except Exception as e:
		print(f'***Ошибка открытия index.html: {e}***')
		exit()
	soup = Soup(html, features="html.parser")
	print('Поиск названия папки...')
	find_foldername = soup.find_all('script')
	for scrIndex in find_foldername:
		if len(scrIndex.attrs):
			for key, value in scrIndex.attrs.items():
				if key == 'src':
					if len(re.findall(r'/\w+/', value)):
						regex = re.findall(r'/\w+/', value)
						if len(regex[0]) == 17:
							foldername = regex[0]
							foldername = foldername.replace('/', '')
							break
	if len(foldername) < 15:
		print('Найти название папки не удалось')
	print(foldername)
	print('ok')
	print('Удаление тегов script...')
	try:
		soup = Soup(html, features="html.parser")
		[x.extract() for x in soup.find_all('script')]
		print('ok')
	except Exception as e:
		print(f'***Ошибка форматирования: {e}***')
		exit()
	
	print('Вставка необходимых тегов...')
	try:
		head = soup.find('title')
		# Список для добавления в <head>
		to_head = [
			"content/shared/js/jquery-1.12.4.min.js",
			"content/shared/js/dr-dtime.min.js",
			"content/shared/js/validation.min.js"]
		try:
			print('В <head>')
			for i in to_head:
				script = soup.new_tag('script')
				script['type'] = "text/javascript"
				script['src'] = i
				head.insert_after(script)
				print(f'Вставлен <script type="text/javascript" src={i}')
			lines = []
			print(
				'Что дополнительно добавить в <head>? БЕЗ ПУСТЫХ СТРОК В СЕРЕДИНЕ И ДВУМЯ ПУСТЫМИ В КОНЦЕ (ENTER - для отмены):')
			while True:
				scripts_input = input()
				if scripts_input:
					lines.append(scripts_input)
				else:
					break;
			longstr = ''
			for i in lines:
				longstr += i
			if not len(longstr):
				print('Дополнительные скрипты добавлены не будут')
			else:
				soup_scripts = Soup(longstr, features="html.parser")
				scripts_list = soup_scripts.find_all('script')
				for scrIndex in scripts_list:
					if len(scrIndex.attrs):
						script = soup.new_tag('script')
						script['src'] = scrIndex['src']
						script['async'] = None
						head.insert_after(script)
					elif len(scrIndex.string):
						script = soup.new_tag('script')
						script.string = scrIndex.string
						head.insert_after(script)
		except Exception as e:
			print(f'***Ошибка вставки необходимых тегов: {e}***')
	except:
		print('Тег <title> для вставки в <head> не найден')
	try:
		body = soup.find('div', class_="ac_footer")
		# Список для добавления в <body>
		to_body = [
			f"content/{foldername}/js/jquery.plugin.min.js",
			f"content/{foldername}/js/jquery.countdown.min.js",
			f"content/{foldername}/js/app.js"]
		print('В <body>')
		try:
			for i in to_body:
				script = soup.new_tag('script')
				script['type'] = "text/javascript"
				script['src'] = i
				body.insert_before(script)
				print(f'Вставлен <script type="text/javascript" src={i}>')
		except Exception as e:
			print(f'***Ошибка вставки необходимых тегов: {e}***')
		print('ok')
	except:
		print('Тег <div class="ac_footer"> в <body> не найден')
	
	
	print('Поиск и редактирование тега <form>...')
	try:
		if soup.find('form'):
			print('Тег <form> найден')
			form = soup.find('form')
			form['action'] = 'send.php'
			print('form action = send.php - ok')
			form['method'] = 'get'
			print('form method = get - ok')
			input_tag = soup.new_tag('input')			
			input_tag['name'] = 'subid'
			input_tag['type'] = 'hidden'
			input_tag['value'] = '{subid}'
			form.insert(3, input_tag)
			print('Тег <input name="subid" type="hidden" value="{subid}"> вставлен')
			print('ok')
	except Exception as e:
		print(f'Тег <form> не найден: {e}')
	

	print('Запись в новый файл "index_formatted.html"...')
	try:
		html_f = soup.prettify("utf-8")
		with open('index_formatted.html', 'wb') as formated:
			formated.write(html_f)
		print('ok')
	except Exception as e:
		print(f'***Ошибка записи в новый файл: {e}***')
		exit()
	


def get_visible_text():
	with open('index.html', 'r', encoding='utf-8') as file:
		html = file.read()
	soup = Soup(html, features="html.parser")
	[s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
	visible_text = soup.getText()
	with open('text.txt', 'w', encoding='utf-8') as out:
		out.write(visible_text)

def GScripts():
	lines = []
	print('Что дополнительно добавить в <head>? БЕЗ ПУСТЫХ СТРОК В СЕРЕДИНЕ И ДВУМЯ ПУСТЫМИ В КОНЦЕ (ENTER - для отмены):')
	while True:
		scripts_input = input()
		if scripts_input:
			lines.append(scripts_input)
		else:
			break;
	longstr = ''
	for i in lines:
		longstr += i
	if not len(longstr):
		print('Дополнительные скрипты добавлены не будут')
	else:
		soup_scripts = Soup(longstr, features="html.parser")
		print(type(soup_scripts))
		scripts_list = soup_scripts.find_all('script')
		for scrIndex in scripts_list:
			if len(scrIndex.attrs):
				script = soup.new_tag('script')
				script['src'] = scrIndex['src']
				script['async'] = None
				head.insert_after(script)
			elif len(scrIndex.string):
				script = soup.new_tag('script')
				script.string = scrIndex.string
				head.insert_after(script)


if __name__ == '__main__':
	format_html()
	#get_visible_text()
