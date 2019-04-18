from bs4 import BeautifulSoup as Soup


def format_html():
	print('Открытие файла...')
	try:
		with open('index.html', 'r', encoding='utf-8') as source:
			html = source.read()
		print('ok')
	except Exception as e:
		print(f'***Ошибка открытия index.html: {e}***')
		exit()
	
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
			nolist = ['n', 'N', 'т', 'Т']
			print(f'Что дополнительно добавить в <head>? (n - для отмены):\n')
			scripts_input = str(input())
			if scripts_input in nolist:
				print('Дополнительные скрипты добавлены не будут')
			else:
				soup_scripts = Soup(scripts_longstr)
			# TODO Принимать многострочную str с разным колличеством скриптов. 1, 2  или 3, например
			# Обрабатывать ее soup'ом и закидывать в новые теги
			# Добавить эти теги в head
		except Exception as e:
			print(f'***Ошибка вставки необходимых тегов: {e}***')
	except:
		print('Тег <title> для вставки в <head> не найден')
	try:
		body = soup.find('div', class_="ac_footer")
		foldername = str(input('Введите название папки для скриптов: '))
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


if __name__ == '__main__':
	format_html()
	get_visible_text()
