from bs4 import BeautifulSoup as Soup
import re
import os

def format_land():
	for key, value in find_dir(q).items():
		longstr = value['longstr']
		for path in value['paths']:
			foldername = ''
			checkscripts_list = []
			print(f'Открытие файла {path}index.html...')
			try:
				with open(f'{path}index.html', 'r', encoding='utf-8') as source:
					html = source.read()
				print('ok')
			except Exception as e:
				print(f'***Ошибка открытия index.html: {e}***')
				exit()
			soup = Soup(html, features="html.parser")
			print('Поиск названия директории и нужных скриптов...')
			find_foldername = soup.find_all('script')
			for scrIndex in find_foldername:
				if len(scrIndex.attrs):
					for key, value in scrIndex.attrs.items():
						if key == 'src':
							checkscripts_list.append(value)
							if len(re.findall(r'/\w+/', value)):
								regex = re.findall(r'/\w+/', value)
								if len(regex[0]) == 17:
									foldername = regex[0]
									foldername = foldername.replace('/', '')
									break
			if len(foldername) < 15:
				print('Найти название папки не удалось')
			print('Директория: ', foldername)
			# Список для добавления в <head>
			to_head = [
				"content/shared/js/jquery-1.12.4.min.js",
				"content/shared/js/dr-dtime.min.js",
				"content/shared/js/validation.min.js"]
			# Список для добавления в <body>
			to_body = [
				f"content/{foldername}/js/jquery.plugin.min.js",
				f"content/{foldername}/js/jquery.countdown.min.js",
				f"content/{foldername}/js/app.js"]
			for i in to_head:
				if i not in checkscripts_list:
					print(f'Скрипт с атрибутом src={i} не найден и в HEAD добавлен не будет')
					to_head.remove(i)
			for i in to_body:
				if i not in checkscripts_list:
					print(f'Скрипт с атрибутом src={i} не найден и в BODY добавлен не будет')
					to_body.remove(i)
			print('ok')
			print('Удаление тегов script...')
			try:
				#soup = Soup(html, features="html.parser")
				[x.extract() for x in soup.find_all('script')]
				print('ok')
			except Exception as e:
				print(f'***Ошибка форматирования: {e}***')
				exit()

			print('Вставка необходимых тегов...')
			try:
				head = soup.find('title')
				print('В <head>')
				for i in to_head:
					script = soup.new_tag('script')
					script['type'] = "text/javascript"
					script['src'] = i
					head.insert_after(script)
					print(f'Вставлен <script type="text/javascript" src={i}')
				print(longstr)
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
				errors += 1

			try:
				body = soup.find('div', class_="ac_footer")
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
					errors += 1
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
					if not soup.find_all(attrs={"name": "subid"}):
						input_tag = soup.new_tag('input')
						input_tag['name'] = 'subid'
						input_tag['type'] = 'hidden'
						input_tag['value'] = '{subid}'
						form.insert(3, input_tag)
						print('Тег <input name="subid" type="hidden" value="{subid}"> вставлен')
					elif soup.find_all(attrs={"name": "subid"}):
						print('Тег <input name="subid" уже присутствует')
					print('ok')
			except Exception as e:
				print(f'Тег <form> не найден: {e}')


			print('Запись в новый файл "index_formatted.html"...')
			try:
				html_f = soup.prettify("utf-8")
				with open(f'{path}index_formatted.html', 'wb') as formated:
					formated.write(html_f)
				print('ok')
			except Exception as e:
				print(f'***Ошибка записи в новый файл: {e}***')
				exit()
			print('*' * 50)

def format_preland():
	print('Какие скрипты добавить?\nБЕЗ ПУСТЫХ СТРОК В СЕРЕДИНЕ И ДВУМЯ ПУСТЫМИ В КОНЦЕ (ENTER - для отмены):')
	lines = []
	while True:
		scripts_input = input()
		if scripts_input:
			lines.append(scripts_input)
		else:
			break;
	longstr = ''''''
	for i in lines:
		longstr += i
	del lines
	for path in find_dir(q):
		print(f'Открытие файла {path}...')
		try:
			with open(f'{path}', 'r', encoding='utf-8') as source:
				html = source.read()
			print('ok')
		except Exception as e:
			print(f'***Ошибка открытия index.html: {e}***')
			exit()
		soup = Soup(html, features="html.parser")
		dtimecount = 0
		deletedcount = 0
		print('Удаляем скрипты...')
		for s in soup.find_all("script"):
			if 'src' in s.attrs.keys():
				if s['src'] == 'content/shared/js/dr-dtime.min.js'\
					or s['src'] == 'content/shared/js/jquery-1.12.4.min.js':
					print(f"Найден {s['src']}")
				else:
					s.extract()
					deletedcount += 1
			elif 'dtime' in s.text:
				dtimecount += 1
			else:
				s.extract()
				deletedcount += 1
		print(f'Найдено dtime_nums: {dtimecount} /// Удалено: {deletedcount}')
		print('ok')
		if soup.find('base'):
			print('<base> уже существует')
		else:
			print('Вставляем <base> в head...')
			base_tag = soup.new_tag('base')
			base_tag['target'] = '_blank'
			head = soup.find('head')
			head.insert(1, base_tag)
		print('ok')
		print('Заменяем все href на {offer}')
		for a in soup.find_all('a'):
			if 'href' in a.attrs.keys():
				if not a['href'] == 'http://ac-feedback.com/report_form/':
					a['href'] = '{offer}'
		print('ok')
		print('Вставляем дополнительные теги...')
		if not len(longstr):
			print('Дополнительные скрипты не найдены')
		else:
			soup_scripts = Soup(longstr, features="html.parser")
			scripts_list = soup_scripts.find_all('script')
			head = soup.find('title')
			for scrIndex in scripts_list:
				try:
					if len(scrIndex.attrs):
						if 'src' and 'async' in scrIndex.attrs.keys():
							script = soup.new_tag('script')
							script['src'] = scrIndex['src']
							script['async'] = None
							head.insert_after(script)
							print(f"Вставлен <script async src={scrIndex['src']}")
						if len(scrIndex.string):
							if 'window.location.href' in scrIndex.string:
								script = soup.new_tag('script')
								script['type'] = 'text/javascript'
								script.string = scrIndex.string
								body = soup.find('div', class_="ac_footer")
								body.insert_after(script)
					elif len(scrIndex.string):
						script = soup.new_tag('script')
						script.string = scrIndex.string
						head.insert_after(script)
				except:
					pass
		print('ok')
		print('Запись в новый файл "index_formatted.html"...')
		try:
			html_f = soup.prettify("utf-8")
			with open(f'{path}_formatted.html', 'wb') as formated:
				formated.write(html_f)
			print('ok')
		except Exception as e:
			print(f'***Ошибка записи в новый файл: {e}***')
			exit()
		print('*' * 50)


def get_visible_text():
	with open('index.html', 'r', encoding='utf-8') as file:
		html = file.read()
	soup = Soup(html, features="html.parser")
	[s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
	visible_text = soup.getText()
	with open('text.txt', 'w', encoding='utf-8') as out:
		out.write(visible_text)

def find_dir(q):
	if q == 'land':
		folders = []
		folder_dict = {}
		for i in os.listdir():
			if os.path.isfile(i): continue
			else:
				if i != '.git':
					folders.append(i)
					folder_dict[i] = {}

		print('Найденные корневые директории:', folders)
		for key, value in folder_dict.items():
			paths = []
			lines = []
			print(f'{key} --- Что дополнительно добавить в <head>?\
				\nБЕЗ ПУСТЫХ СТРОК В СЕРЕДИНЕ И ДВУМЯ ПУСТЫМИ В КОНЦЕ (ENTER - для отмены):')
			while True:
				scripts_input = input()
				if scripts_input:
					lines.append(scripts_input)
				else:
					break;
			longstr = ''''''
			for i in lines:
				longstr += i
			value['longstr'] = longstr
			for subdir in os.listdir(key):
				if os.path.isfile(subdir): continue
				else:
					sdir = key + '/' + subdir + '/'
					paths.append(sdir)
			value['paths'] = paths
		return folder_dict
	elif q == 'preland':
		paths = []
		for i in os.listdir():
			if os.path.isfile(i): continue
			else:
				if i != '.git':
					if os.path.isfile(f'{i}/index.html'):
						paths.append(i + '/index.html')
					else:
						for j in os.listdir(i):
							if os.path.isfile(f'{i}/{j}'): continue
							else:
								if os.path.isfile(f'{i}/{j}/index.html'):
									paths.append(f'{i}/{j}/index.html')
		return paths

if __name__ == '__main__':
	errors = 0
	print('land - рядом со скриптом минимум 1 папка с гео, внутри которой минимум одна папка с сайтом (index.html)')
	print('preland - рядом со скриптом папки с сайтами (index.html)')
	q = input('land / preland ? - ')
	q = q.lower()
	if q == 'land':
		format_land()
	elif q == 'preland':
		format_preland()
	else:
		print('Ошибка ввода')
	print(f'Завершено. Ошибок: {errors}')
	#get_visible_text()
