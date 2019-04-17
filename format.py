from bs4 import BeautifulSoup as Soup
from sys import argv


def format_html():
	foldername = str(argv[1])
	print('Открытие файла...')
	try:
		with open('index.html', 'r', encoding='utf-8') as source:
			html = source.read()
	except Exception as e:
		print(f'***Ошибка открытия index.html: {e}***')
		exit()
	print('Файл открыт')
	print('Удаление тегов script...')
	try:
		soup = Soup(html, features="html.parser")
		[x.extract() for x in soup.find_all('script')]
	except Exception as e:
		print(f'***Ошибка форматирования: {e}***')
		exit()
	print('Удалено')

	head = soup.find('title')
	body = soup.find('div', class_="page__wrapper js-wrapper")
	to_head = [
		"content/shared/js/jquery-1.12.4.min.js",
		"content/shared/js/dr-dtime.min.js",
		"content/shared/js/validation.min.js"]
	to_body = [
		f"content/{foldername}/js/jquery.plugin.min.js",
		f"content/{foldername}/js/jquery.countdown.min.js",
		f"content/{foldername}/js/app.js"]
	print('Вставка необходимых тегов...')
	try:

		print('В <head>')
		for i in to_head:
			script = soup.new_tag('script')
			script['type'] = "text/javascript"
			script['src'] = i
			head.insert_after(script)
			print(f'Вставлен <script type="text/javascript" src={i}')
		print('В <body>')
		for i in to_body:
			script = soup.new_tag('script')
			script['type'] = "text/javascript"
			script['src'] = i
			body.insert_after(script)
			print(f'Вставлен <script type="text/javascript" src={i}>')
	except Exception as e:
		print(f'***Ошибка вставки необходимых тегов: {e}***')
		exit()
	print(f'Необходимые теги вставлены')

	print('Запись в новый файл "index_formatted.html"...')
	try:
		html_f = soup.prettify("utf-8")
		with open('index_formatted.html', 'wb') as formated:
			formated.write(html_f)
	except Exception as e:
		print(f'***Ошибка записи в новый файл: {e}***')
		exit()
	print('Записано успешно')


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
