"""
Файл содержащий базовые конфигурации бота и API
(Токен, API-ключ, website, параметры и url-адреса)
"""

TOKEN = ''
KEY = ''
WEBSITE = 'hotels4.p.rapidapi.com'
url = 'https://hotels4.p.rapidapi.com/locations/search'
url_list = 'https://hotels4.p.rapidapi.com/properties/list'
url_photos = 'https://hotels4.p.rapidapi.com/properties/get-hotel-photos'
db = 'python_basic_diploma/database/Users.db'
client = {
    'X-RapidAPI-Key': KEY,
    'X-RapidAPI-Host': WEBSITE
}


