
### 2019.10.24
### Telegram Chatbot 제작 및 배포 (Pythonanywhere)

- 별도 작업 폴더 생성 
```cmd
$ mkdir telegram_bot
```
- web버전 로그인(https://web.telegram.org/ )
- BotFather 선택후 /deletebot 입력하여 기존 봇 있을경우 삭제
- 새 작업 폴더에 flask 세팅 서버 구동
```cmd
#작업폴더 위치에서
source ~/venv/Scripts/activate #가상환경 실행
pip install flask #flask 설치
python -m pip install --upgrade pip
#app.py 파일생성 후
FLASK_APP=app.py flask run #플라스크 실행
```
- telegram >  /newbot 입력후 봇 이름 입력 예) pkh1003_bot
- 챗봇이 생성되면 토큰 정보를 받을 수 있음
- API 사용방법 확인 (https://core.telegram.org/bots/api#available-methods )
```
https://api.telegram.org/bot<token>/getMe
#telegram에서 생성한 챗봇 검색하여 추가 예) @pkh1003_bot 입력
https://api.telegram.org/bot<token>/getUpdates
```

- send_message.py 파일생성
```python
import requests

api_url = 'https://api.telegram.org'
token = '[본인토큰 입력]'
chat_id = '[챗봇id 입력]'
text = input('메시지를 입력해주세요:')

requests.get(f'{api_url}/bot{token}/sendMessage?chat_id={chat_id}&text={text}')
```

##### 토큰정보를 숨기기 위해 python-decouple 설치
- 가상환경에서 python-decouple 설치
```linux
source ~/venv/Scripts/activate #가상환경 실행
pip install python-decouple
touch .env
vi .env
```
- .env에 내용입력
```linux
TELEGRAM_BOT_TOKET=''
CHAT_ID=''
```
- .gitignore 파일 추가하고 내용에 .env 추가
- app.py 수정
```python
from decouple import config
import requests

api_url = 'https://api.telegram.org'
token = config('TELEGRAM_BOT_TOKET') #프로젝트내에 .env에서 정보를 가져옴
chat_id = config('CHAT_ID')
text = input('메시지를 입력해주세요:')

requests.get(f'{api_url}/bot{token}/sendMessage?chat_id={chat_id}&text={text}')
```

##### 과제 - 로또, vonvon 기능 적용
```python
from flask import Flask, render_template, request
from decouple import config
import requests
import random

app = Flask(__name__)

api_url = 'https://api.telegram.org'
token = config('TELEGRAM_BOT_TOKET') #프로젝트내에 .env에서 정보를 가져옴
chat_id = config('CHAT_ID')

# 텔레그램 서버가 우리 서버에게 HTTP POST 요청을 통해, 
# 사용자 메시지 정보를 받으라고 전달해주는 것
# 우리가 status 200을 리턴해줘야 텔레그램 측에서 더이상 전송을 중단한다
# 200을 안돌려주면 계속 POST 요청을 여러번 보낸다
@app.route(f'/{token}', methods=['POST'])
def telegram():
    #1. 메아리(Echo) 기능
    #1.1 request.get_json() 구조 확인하기
    print(request.get_json())
    # #1.2 사용자 아이디, 텍스트 가져오기
    chat_id = request.get_json().get('message').get('from').get('id')
    text = request.get_json().get('message').get('text')
    print(chat_id, text)
    #1.3 텔레그램 API에게 요청을 보내서 답변해주기

    if '/로또' in text:
        #1.로또 기능
        #사용자가 '/로또'라고 말하면 랜덤으로 번호 6개 뽑아서 돌려주기
        #나지 경우엔 전부 메아리
        result = random.sample(range(1,46),6)
        lotto =''
        # for x in result:
        #     lotto += str(x) +","   
        lotto = ', '.join(str(x) for x in result)

        text = f'로또번호: {lotto}'
        requests.get(f'{api_url}/bot{token}/sendMessage?chat_id={chat_id}&text={text}')
    elif '/vonvon' in text:
        #2. vonvon 기능 (심화)
        #사용자가 '/vonvon 이름'이라고 말하면 신이 나를 만들었을 때 요소 돌려주기
        temp = text.split(' ')
        user_name = temp[1]
        first,second,third = vonvon()

        text = f'신이 {user_name}님을 만들때 {first},{second},{third}'
        requests.get(f'{api_url}/bot{token}/sendMessage?chat_id={chat_id}&text={text}')
    else:
        requests.get(f'{api_url}/bot{token}/sendMessage?chat_id={chat_id}&text={text}')
    
    return '', 200

def vonvon():
    # 사용자에게 보여줄 여러가지 재밌는 특정들 리스트를 만든다
    first_list = ['미모들 듬뿍~','착함 세방울 넣고','앗 잘못넣음','엉뚬함 조금 넣고','성실함 두방울 넣고','잘생김 두방울 넣고..엌 쏟았네']
    second_list = ['기럭지도 필요하려나','애교도 조금 넣으면 좋겠군']
    third_list = ['하긴 너무 다 퍼줄 수 없지','기억력을 마지막으로.. 엌 바닥에 쏟았네','성실함을 마지막으로.. 엌 바닥에 쏟았네']
    
    # 리스트에서 랜덤으로 하나씩을 선택한다
    first = random.choice(first_list)
    second = random.choice(second_list)
    third = random.choice(third_list)

    return first,second,third


@app.route('/write')
def write():
    return render_template('write.html')

@app.route('/send')
def send():
    text = request.args.get('message')
    requests.get(f'{api_url}/bot{token}/sendMessage?chat_id={chat_id}&text={text}')
    return '메시지 전송완료'


#debug 모드를 활성화해서 서버 새로고침을 생략
if __name__ == '__main__':
    app.run(debug=True)

```

##### ngrok 이용하여 로컬아이피를 퍼블릭으로 변환
- ngrok : 로컬아이피를 퍼블릭으로 변환해주는 것(https://ngrok.com/)
- 가입 후 프로그램 다운
- cmd 실행 >  해당 파일 위치에서 ngrok 실행
```cmd
$ ngrok http 5000
```
![ngrok1]( https://user-images.githubusercontent.com/33045725/67465759-c140b180-f680-11e9-8318-0cf89827a98a.JPG)

- telegram에 웹 훅 등록
```
#엔그록 url
https://.....ngrok.io

#브라우저에서 아래 url 호출하여 웹훅 설정
https://api.telegram.org/bot<token>/setWebhook?url=<ngrok_url>/<token>
```

##### pythonanywhere 이용해서 사이트 띄우기
- pythonanywhere 가입(https://www.pythonanywhere.com/ )
    - Web 메뉴선택
    - Add a new web app
    - Flask 선택
    - Python 3.7 (Flask 1.0.2)
    - Next
    - http://kyunghee.pythonanywhere.com/ 확인
    - Web > Code 영역 Go to directory버튼 클릭
    - Consoles 선택 > Bash
    ```python
    #decouple 설치
    pip3 install python-decouple --user 
    ```
	- 기존파일 .env 파일 업로드및 생성
	- 기존 app.py 소스 =>flask_app.py에 반영
	- Reload

- 브라우저를 통해 웹훅 삭제
```
https://api.telegram.org/bot<token>/deleteWebhook
```

- 브라우저를 통해 웹훅 등록
```
https://api.telegram.org/bot<token>/setWebhook?url=<pythonanywhere_url>/<chat_id>
```


##### google cloud api를 이용한 번역기

- https://cloud.google.com/apis/docs/overview
- 관련 문서( https://cloud.google.com/translate/docs/quickstart-client-libraries?hl=ko )
- 프로젝트 생성
- 구글 API 키 생성
(콘솔 > API 및 서비스 > 사용자 인증 정보 > 사용자 인증 정보 만들기)
- API 라이브러리 > Cloud Translation API 사용설정
- google.py 생성
```python
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
```





