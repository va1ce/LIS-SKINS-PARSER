import requests
from bs4 import BeautifulSoup
import time
from random import randrange
import json


HEADERS = {
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
}

URL = "https://lis-skins.ru/market/csgo/?sortby=price_desc&type=45%2C51%2C46%2C48%2C50%2C47%2C49&hold=-1"
def get_urls(url):
	s = requests.Session()
	response = s.get(url=url, headers=HEADERS)

	soup = BeautifulSoup(response.text, 'lxml')
	pagination_count = int(soup.find('div', class_='pagination').find_all('a')[-1].text)
	print(pagination_count)
	url_list = []
	#for page in range(1,pagination_count + 1):
	for page in range(1, pagination_count):
		url = f'{URL}&page={page}'
		response = s.get(url=f'{URL}&page={page}', headers=HEADERS)
		soup = BeautifulSoup(response.text, 'lxml')
		skins_url = soup.find_all('a',class_='name')
		for su in skins_url:
			s_url = su.get('href')
			url_list.append(s_url)
		time.sleep(randrange(2, 5))
		print(f'Обработал {page}/{pagination_count}')
	with open ('url_list.txt', 'w', encoding="UTF-8") as file:
		for url in url_list:
			file.write(f'{url}\n')
	return 'Считал мей'



def get_data(file_path):
	with open(file_path,encoding="UTF-8") as file:
		url_list = [line.strip() for line in file.readlines()]

	s = requests.Session()
	result_data = []
	for url in url_list:
		response = s.get(url=url,headers=HEADERS)
		soup = BeautifulSoup(response.text, 'lxml')
		try:
			item_price = soup.find('div', class_='price').text
			item_float = soup.find('div', class_='float').text
			item_name = soup.find('div', class_='bread').find_all('span')[-1].text

		except AttributeError:
			continue
		#item_sticker = soup.find('div', class_='sticker').text
		print(f'Price =', item_price ,'   Float = ',item_float , '   Name = ', item_name)
		result_data.append(
			{
			'url': url,
			 'market_hash_name':item_name,
			 'price':item_price,
			 'float':item_float,
			}
		)
	with open ('result.json','w', encoding="UTF-8") as file:
		json.dump(result_data,file,indent=4,ensure_ascii=False)
	print(f'Обработал {url}/')
def main():
	print(get_urls(url=URL))
	get_data('url_list.txt')


if __name__ == '__main__':
	main()
