import requests
from decouple import config

api_url="https://translation.googleapis.com/language/translate/v2"
key=config('GOOGLE_TRAN_TOKEN')
data = {
    'q':'엄마 판다는 새까가 있네',
    'source':'ko',
    'target':'en'
}

result = requests.post(f'{api_url}?key={key}', data).json()
print(result)