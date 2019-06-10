from bs4 import BeautifulSoup as Soup
from googletrans import Translator
from time import sleep
import os
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
fh = logging.FileHandler("logs.log", 'w', encoding="utf-8")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
log.addHandler(fh)

MainMenu = """
\t\t\t#----------- Main Menu ---------#

\t\t\t#   1. Land                     #
\t\t\t#   2. Preland                  #
\t\t\t#   3. Translate Land           #
\t\t\t#   0. Quit                     #

\t\t\t#-------------------------------#
            
\t\t!!!  Рядом с файлом скрипта папки с index.html  !!!\n\n"""

GroupsMenu = """
\t\t\t#--------- Landing Directories Menu ---------#

\t\t\t#   1. Without "GEO Groups" folders          #
\t\t\t#   2. With "GEO Groups" folders             # 
\t\t\t#   0. Quit                                  #
	                                         
\t\t\t    Geo Grouping example: -MA               
\t\t\t\t\t\t\t\t\t\t--land1       
\t\t\t\t\t\t\t\t\t\t--land2        
\t\t\t\t\t\t\t\t\t  -GT
\t\t\t\t\t\t\t\t\t\t--land1        
\t\t\t\t\t\t\t\t\t\t--land2        
\t\t\t
\t\t\t#--------------------------------------------#\n\n"""


def format_land():
	for key, value in find_dir(q).items():
		longstr = value['longstr']
		for path in value['paths']:
			foldername = ''
			checkscripts_list = []
			print(f'Открытие файла {path}/index.html...')
			try:
				with open(f'{path}/index.html', 'r', encoding='utf-8') as source:
					html = source.read()
				print('ok')
			except Exception as e:
				print(f'***Ошибка открытия index.html: {e}***')
				errors += 1
			soup = Soup(html, features="html.parser")

			# Список нужных скриптов
			js_names = ["jquery", "dr-dtime.min.js", "validation.min.js", "main.js", "app.js", "common.js", "scripts.js"]

			print('Удаление тегов script...')
			try:
				deleted = 0
				for s in soup.find_all('script'):
					if 'src' in s.attrs.keys():
						if any(name in s['src'] for name in js_names):
							print(f'Скрипт {s["src"]} найден')
						else:
							s.extract()
							deleted += 1
					else:
						s.extract()
						deleted += 1
				print(f'Удалено {deleted}')
			except Exception as e:
				print(f'***Ошибка форматирования: {e}***')
				errors += 1

			print('Вставка необходимых тегов...')
			try:
				head = soup.find('title')
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


			print('Замена старого "index.html" и создание бекапа...')
			if not os.path.isfile(f'{path}/index_old.html'):
				os.rename(f'{path}/index.html', f'{path}/index_old.html')
			else:
				print('Найден index_old.html')
			try:
				html_f = soup.prettify("utf-8")
				with open(f'{path}/index.html', 'wb') as formated:
					formated.write(html_f)
				print('ok')
			except Exception as e:
				print(f'***Ошибка записи в новый файл: {e}***')
				exit()
			print('*' * 50)
			print(f'Создание {path}/send.php...')
			with open(f'{path}/send.php', 'w') as send:
				offer_id = input('ID Оффера: ')
				country_code = input('ГЕО Код: ')
				base_url = input('URL лендинга в ПП: ')
				price = input('Цена: ')
				referrer = input('URL лендинга в трекере: ')
				text = "<?php\n\n$name = $_GET['name'];\n$phone = $_GET['phone'];\n" \
					f"$offer_id = '{offer_id}';\n$api_key = 'b';\n" \
					f"$country_code = '{country_code}';\n$base_url = '{base_url}';\n$price = '{price}';\n$referrer = '{referrer}';\n" \
					"""$ip = $_SERVER['REMOTE_ADDR'];
$sub_id = $_GET['subid'];

a

$isCurlEnabled = function(){
    return function_exists('curl_version');
};
if (!$isCurlEnabled) {
    echo "<pre>";
    echo "pls install curl";
    echo "For *unix open terminal and type this:";
    echo 'sudo apt-get install curl && apt-get install php-curl';
    die;
}

$args = array(

	'api_key' => $api_key,
	'name' => $name,
	'phone' => $phone,
	'offer_id' => $offer_id,
	'country_code' => $country_code,
	'base_url' => $base_url,
	'price' => $price,
	'referrer' => $referrer,
	'ip' => $ip,
    'subacc4' => $sub_id
);

$url = API_URL.'?'.http_build_query($args);
$curl = curl_init();
curl_setopt_array($curl, array(
    CURLOPT_URL => $url,
    CURLOPT_RETURNTRANSFER => true
));

$res = curl_exec($curl);
curl_close($curl);

$res = json_decode($res, true);
if ($res['code'] == 'ok') {
    echo $res['msg'] . ": " . $res['order_id'];
} else {
    echo $res['error'];
}

header ('Location: success.html');  """
				send.write(text)
			print('Файл send.php создан')
			print(f'Создание {path}/success.html...')
			with open(f'{path}/success.html', 'w', encoding='utf-8') as file:
				h1 = input('Первый абзац: ')
				h2 = input('Второй абзац: ')
				text = """<html>
<head>
	<meta charset="utf-8">
</head>
<body>
<center>\n""" \
  		f"<h1>{h1}</h1>\n" \
		f"<h1>{h2}</h1>\n" \
"""</center>
</body>
</html>					
"""
				file.write(text)
				print('success.html создан')

def format_preland():
	print('Какие скрипты добавить?\nБЕЗ ПУСТЫХ СТРОК В СЕРЕДИНЕ И ДВУМЯ ПУСТЫМИ В КОНЦЕ (ENTER - для пропуска):')
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
		print('Замена старого "index.html" и создание бекапа...')
		if not os.path.isfile(f'{path}_old.html'):
			os.rename(f'{path}', f'{path}_old.html')
		else:
			print('Найден index_old.html')
		print('Запись в новый файл "index.html"...')
		try:
			html_f = soup.prettify("utf-8")
			with open(f'{path}', 'wb') as formated:
				formated.write(html_f)
			print('ok')
		except Exception as e:
			print(f'***Ошибка записи в новый файл: {e}***')
			exit()
		print('*' * 50)

def translate_land():
	errors = 0
	translator = Translator()
	lang = input('Type 2 letter code for translate language (AR = Arabic, ES = Spanish) Codes - https://www.sitepoint.com/iso-2-letter-language-codes/: ')
	lang.lower()
	translate_hist = """"""
	with open('index.html', 'r', encoding='utf-8') as file:
		html = file.read()
	soup = Soup(html, features="html.parser")
	tags = ['span', 'p', 'b', 'a', 'div', 'li', 'h1', 'h2', 'h3', 'button', 'small', 'strong', 'td', 'img', 'input']

	for tag in tags:
		for htmltag in soup.find_all(tag):
			try:
				log.debug(f'{tag} {htmltag} Text: {htmltag.text}, string: {htmltag.string}')
				if htmltag.string and len(htmltag.string) > 1:
					log.debug(f'First IF (string). len = {len(htmltag.string)}')
					log.debug(f'Tag {tag} {htmltag} String: {htmltag.string}')
					translated = translator.translate(htmltag.string, dest=lang)
					log.info(f'<{tag}> {htmltag.string} > {translated.text}')
					htmltag.string.replace_with(translated.text)
				elif tag == 'img' and 'alt' in htmltag.attrs and len(htmltag["alt"]) > 0:
					log.debug('Second IF (img alt)')
					log.debug(f'Tag {tag} {htmltag} Alt: {htmltag["alt"]}')
					translated = translator.translate(htmltag['alt'], dest=lang)
					log.info(f'<{tag}> {htmltag["alt"]} > {translated.text}')
					htmltag['alt'] = translated.text
				elif tag == 'input' and 'placeholder' in htmltag.attrs and len(htmltag["placeholder"]):
					log.debug('Third IF (placeholder)')
					log.debug(f'Tag {tag} {htmltag} Placeholder: {htmltag["placeholder"]}')
					translated = translator.translate(htmltag['placeholder'], dest=lang)
					log.info(f'<{tag}> {htmltag["placeholder"]} > {translated.text}')
					htmltag['placeholder'] = translated.text
				elif tag != 'div' and htmltag.text and len(htmltag.text) in range(2, 200) and not htmltag.string:
					log.debug('Fourth IF (not if and .text and not .string')
					log.debug(f'Tag {tag} {htmltag} Text({len(htmltag.text)}): {htmltag.text}')
					translated = translator.translate(htmltag.text, dest=lang)
					log.info(f'<{tag}> {htmltag.text} > {translated.text}')
					htmltag.string = translated.text
				else:
					log.debug('Pass')
			except Exception as e:
				pass
				log.error(f'*** ERROR Tag: {tag} , htmltag: {htmltag} , Str: {htmltag.string} / Err: {e} ***')
				errors += 1
			sleep(1)

	html_f = soup.prettify("utf-8")
	with open(f'index_f.html', 'wb') as formated:
		formated.write(html_f)
	log.info(f'Завершено. Ошибок {errors}')

def find_dir(q):
	if q == '1':
		folders = []
		folder_dict = {}
		paths = []
		lines = []

		for i in os.listdir():
			if os.path.isfile(i): continue
			else:
				if i != '.git':
					folders.append(i)
					folder_dict[i] = {}

		print('\nНайденные корневые директории:', folders)
		print(GroupsMenu)
		groupchoose = input('> ')
		for key, value in folder_dict.items():
			print("""
\t\t\t#----------------- Additional Scripts Menu -----------------#
\n""" \
f"\t\t\t\tFolder '{key}'\n\n" \
"""\t\t\t\tВведите дополнительные скрипты для <head>

\t\t\t\t!!!     Без пустых строк     !!! 

\t\t\t\t(ENTER для пропуска)

\t\t\t#-----------------------------------------------------------#\n""")
			while True:
				scripts_input = input()
				if scripts_input:
					lines.append(scripts_input)
				else:
					break
			longstr = ''''''
			for i in lines:
				longstr += i
			value['longstr'] = longstr

			if groupchoose == '1':
				value['paths'] = [key]

			elif groupchoose == '2':
				for subdir in os.listdir(key):
					if os.path.isfile(subdir): continue
					else:
						sdir = key + '/' + subdir
						paths.append(sdir)
				value['paths'] = paths
		return folder_dict
	elif q == '2':
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
	print(MainMenu)
	while True:
		q = input('> ')
		if q == '1':
			format_land()
			break
		elif q == '2':
			format_preland()
			break
		elif q == '3':
			translate_land()
			break
		elif q == '0':
			exit()
		else:
			print('Ошибка ввода')
	print(f'Основной процесс завершен. Ошибок: {errors}')
