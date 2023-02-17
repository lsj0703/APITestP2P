import unittest
import requests
import random, string
from api.loginAPI import loginAPI
from utils import init_log_config, assert_utils, get_data
import json, logging
from parameterized import parameterized


class TestLogin(unittest.TestCase):
    phone1 = '13012341111'
    phone2 = '13012341112'
    imgCode = '8888'
    imgCodeError = '6666'
    password = 'qwer1234'
    phone_code = '666666'
    dy_server = 'on'

    @classmethod
    def setUpClass(cls) -> None:
        cls.login_api = loginAPI()
        cls.log_reg = init_log_config('register')
        cls.log_login = init_log_config('login')
        cls.session = requests.Session()

    @classmethod
    def tearDown(cls):
        if cls.session:
            cls.session.close()

    @parameterized.expand(get_data('imgVerifyCode.json', 'test_img_verifycode', params=('type', 'status_code', 'desc')))
    def test001_get_img_code(self, type, status_code, desc):
        r = ''
        if type == 'float':
            r = random.random()
        elif type == 'int':
            r = random.randint(1000000, 9999999)
        elif type == 'char':
            r = random.choice(string.ascii_letters)

        res = self.login_api.getImgCode(self.session, r)
        self.assertEqual(status_code, res.status_code)
        self.log_reg.info("register msg = {}{}".format(desc, res))

    @parameterized.expand(get_data('register.json', 'test_register', params=(
    'phone', 'pwd', 'verifycode', 'phone_code', 'invite_phone', 'status_code', 'status',
    'description', 'desc')))
    def test002_register(self, phone, pwd, verifycode, phone_code, invite_phone, status_code, status,
                         description, desc):
        r = random.random()
        res = self.login_api.getImgCode(self.session, r)
        self.assertEqual(200, res.status_code)

        res = self.login_api.getMsgCode(self.session, phone, self.imgCode)
        assert_utils(self, res, 200, 200, "短信发送成功")

        res = self.login_api.register(self.session, phone, pwd, verifycode, phone_code=phone_code,
                                      invite_phone=invite_phone)
        self.log_reg.info("register msg = {}{}".format(desc, res.json()))
        assert_utils(self, res, status_code, status, description)

    # # 参数为随机小数时，获取验证码成功
    # def test001_get_img_code_random_float(self):
    #     r = random.random()
    #     res = self.login_api.getImgCode(self.session, r)
    #     self.assertEqual(200, res.status_code)
    #     self.log_reg.info("register msg = {}".format(res))
    #
    # # 参数为随机整数时，获取验证码成功
    # def test002_get_img_code_random_int(self):
    #     r = random.randint(1000000, 99999999)
    #     res = self.login_api.getImgCode(self.session, r)
    #     self.assertEqual(200, res.status_code)
    #     self.log_reg.info("register msg = {}".format(res))
    #
    # # 参数为空，获取验证码失败
    # def test003_get_img_code_empty(self):
    #     r = ''
    #     res = self.login_api.getImgCode(self.session, r)
    #     self.assertEqual(404, res.status_code)
    #     self.log_reg.info("register msg = {}".format(res))
    #
    # # 参数为字母时，获取验证码失败
    # def test004_get_img_code_random_letter(self):
    #     r = random.choice(string.ascii_letters)
    #     # r = random.sample('abcdefghigklmn', 10)
    #     res = self.login_api.getImgCode(self.session, r)
    #     self.assertEqual(400, res.status_code)
    #     self.log_reg.info("register msg = {}".format(res))
    #
    # # 参数正确获取短信验证码成功
    # def test005_get_msg_code_success(self):
    #     r = random.random()
    #     res = self.login_api.getImgCode(self.session, r)
    #     self.assertEqual(200, res.status_code)
    #
    #     res = self.login_api.getMsgCode(self.session, self.phone1, self.imgCode)
    #     # self.assertEqual(200, res.json().get('status'))
    #     # self.assertEqual("短信发送成功", res.json().get('description'))
    #     assert_utils(self, res, 200, 200, "短信发送成功")
    #     self.log_reg.info("register msg = {}".format(res.json()))
    #
    # # 图片验证码错误获取短信验证码失败
    # def test006_get_msg_code_fail_img_code_error(self):
    #     r = ''
    #     res = self.login_api.getImgCode(self.session, r)
    #     self.assertEqual(404, res.status_code)
    #
    #     res = self.login_api.getMsgCode(self.session, self.phone1, self.imgCodeError)
    #     assert_utils(self, res, 200, 100, "图片验证码错误")
    #     self.log_reg.info("register msg = {}".format(res.json()))
    #
    # # 图片验证码为空获取短信验证码失败
    # def test007_get_msg_code_fail_img_code_empty(self):
    #     r = ''
    #     res = self.login_api.getImgCode(self.session, r)
    #     self.assertEqual(404, res.status_code)
    #
    #     res = self.login_api.getMsgCode(self.session, self.phone1, r)
    #     assert_utils(self, res, 200, 100, "图片验证码错误")
    #     self.log_reg.info("register msg = {}".format(res.json()))
    #
    # # 手机号码为空获取短信验证码失败
    # def test008_get_msg_code_fail_phone_empty(self):
    #     r = random.random()
    #     res = self.login_api.getImgCode(self.session, r)
    #     self.assertEqual(200, res.status_code)
    #
    #     res = self.login_api.getMsgCode(self.session, '', self.imgCodeError)
    #     self.assertEqual(100, res.json().get('status'))
    #     self.log_reg.info("register msg = {}".format(res.json()))
    #
    # # 输入所有参数注册成功
    # def test009_register_success_params_all(self):
    #     r = random.random()
    #     res = self.login_api.getImgCode(self.session, r)
    #     self.assertEqual(200, res.status_code)
    #
    #     res = self.login_api.getMsgCode(self.session, self.phone1, self.imgCode)
    #     # self.assertEqual(200, res.json().get('status'))
    #     # self.assertEqual("短信发送成功", res.json().get('description'))
    #     assert_utils(self, res, 200, 200, "短信发送成功")
    #
    #     res = self.login_api.register(self.session, self.phone1, self.password, invite_phone='13012341234')
    #     self.log_reg.info("register msg = {}".format(res.json()))
    #     assert_utils(self, res, 200, 200, "注册成功")
    #
    # # 输入所有参数注册成功
    # def test010_register_success_params_required(self):
    #     r = random.random()
    #     res = self.login_api.getImgCode(self.session, r)
    #     self.assertEqual(200, res.status_code)
    #
    #     res = self.login_api.getMsgCode(self.session, self.phone2, self.imgCode)
    #     # self.assertEqual(200, res.json().get('status'))
    #     # self.assertEqual("短信发送成功", res.json().get('description'))
    #     assert_utils(self, res, 200, 200, "短信发送成功")
    #
    #     res = self.login_api.register(self.session, self.phone2, self.password)
    #     self.log_reg.info("register msg = {}".format(res.json()))
    #     assert_utils(self, res, 200, 200, "注册成功")
    #
    # # 输入正确的手机号密码登录成功
    # def test011_login_success(self):
    #     res = self.login_api.login(self.session, self.phone1, self.password)
    #     self.log_login.info("login msg = {}".format(res.json()))
    #     assert_utils(self, res, 200, 200, "登录成功")
