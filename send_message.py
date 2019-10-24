from decouple import config
import requests

api_url = 'https://api.telegram.org'
token = config('TELEGRAM_BOT_TOKET') #프로젝트내에 .env에서 정보를 가져옴
chat_id = config('CHAT_ID')
text = input('메시지를 입력해주세요:')

requests.get(f'{api_url}/bot{token}/sendMessage?chat_id={chat_id}&text={text}')

