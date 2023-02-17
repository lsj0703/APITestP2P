import unittest
import requests
import random, string
from api.loginAPI import loginAPI
from api.approveAPI import approveAPI
from utils import init_log_config, assert_utils, request_third_party
import json, logging
from bs4 import BeautifulSoup


class TestApprove(unittest.TestCase):
    phone1 = '13012341111'
    password = 'qwer1234'
    realname = "李山丹"
    cardId = "140203199211018203"
    data = {}

    @classmethod
    def setUpClass(cls) -> None:
        cls.login_api = loginAPI()
        cls.approve_api = approveAPI()
        cls.log_approve = init_log_config('approve')
        cls.session = requests.Session()
    @classmethod
    def tearDown(cls):
        if cls.session:
            cls.session.close()

    # 输入正确的实名认证信息
    def test001_approve_realname_params_all(self):
        res = self.login_api.login(self.session, self.phone1, self.password)
        self.log_approve.info("login msg = {}".format(res.json()))
        assert_utils(self, res, 200, 200, "登录成功")

        # res = self.approve_api.approve_realname(self.session, self.realname, self.cardId)
        res = self.approve_api.approve_realname(self.session, self.realname, self.cardId)
        self.log_approve.info("login msg = {}".format(res.json()))
        assert_utils(self, res, 200, 200, "提交成功")
        self.assertIn('140****203', res.json().get('data').get('card_id'))

    # 获取实名认证信息和开户信息
    def test002_get_approve(self):
        res = self.login_api.login(self.session, self.phone1, self.password)
        self.log_approve.info("login msg = {}".format(res.json()))
        assert_utils(self, res, 200, 200, "登录成功")

        res = self.approve_api.get_approve(self.session)
        print(res.json())
        self.assertEqual(200, res.status_code)

    # 获取开户信息,发送给第三方接口开户
    def test003_trust_approve(self):
        res = self.login_api.login(self.session, self.phone1, self.password)
        self.log_approve.info("login msg = {}".format(res.json()))
        assert_utils(self, res, 200, 200, "登录成功")
        # 获取开户信息
        res = self.approve_api.trust_register(self.session)
        # 调用第三方开户接口
        res = request_third_party(res)
        self.log_approve.info("approve msg = {}".format(res.text))
        self.assertEqual(200, res.status_code)
        self.assertEqual('UserRegister OK', res.text)
