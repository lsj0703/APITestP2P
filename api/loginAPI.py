import app
import random
import requests


class loginAPI():

    def __init__(self):
        self.img_code_url = app.BASE_URL + "/common/public/verifycode1/{}"
        self.msg_code_url = app.BASE_URL + "/member/public/sendSms"
        self.register_url = app.BASE_URL + "/member/public/reg"
        self.login_url = app.BASE_URL + "/member/public/login"

    def getImgCode(self, session, r):
        url = self.img_code_url.format(r)
        res = session.get(url)
        return res

    def getMsgCode(self, session, phone, imgVerifyCode, type='reg'):
        url = self.msg_code_url
        data = ("phone={}&imgVerifyCode={}&type={}").format(phone, imgVerifyCode, type)
        # print(data)
        res = session.post(url, headers=app.headers, data=data)
        return res

    def register(self, session, phone, password, verifycode='8888', phone_code='666666', dy_server='on', invite_phone=''):
        url = self.register_url
        data = ("phone={}&password={}&verifycode={}&phone_code={}&dy_server={}&dy_server={}").format(phone, password, verifycode, phone_code, dy_server, invite_phone)
        res = session.post(url, headers=app.headers, data=data)
        return res

    def login(self, session, phone, password):
        url = self.login_url
        data = ("keywords={}&password={}").format(phone, password)
        res = session.post(url, headers=app.headers, data=data)
        return res



#s = loginAPI()
# session = requests.Session()
# s.getImgCode(r)
# s.getMsgCode(session, 13032145678, 8888, 'reg')
