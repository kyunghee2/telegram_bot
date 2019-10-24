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
