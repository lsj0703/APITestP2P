import unittest, requests, random
from api.rechargeAPI import rechargeAPI
from api.loginAPI import loginAPI
from utils import assert_utils, init_log_config, request_third_party, DButils
import app


class TestRecharge(unittest.TestCase):
    phone1 = '13012341111'
    password = 'qwer1234'

    @classmethod
    def setUpClass(cls) -> None:
        cls.login_api = loginAPI()
        cls.recharge_api = rechargeAPI()
        cls.log_recharge = init_log_config()
        cls.session = requests.Session()

    # def setUp(self) -> None:
    #     self.session = requests.Session()
    @classmethod
    def tearDown(cls) -> None:
        if cls.session:
            cls.session.close()

        # =======清除数据======
        # sql1 = "delete i.* from m_member_login_log i inner join m_meber m on i.id = m.id where m.phone in('13012341111','13012341112')"
        # DButils.exe_sql(app.DB_MEMBER, sql1)
        # cls.log_recharge.info("delete sql = {}").format(sql1)
        # sql2 = "delete i.* from m_member_login_log i inner join m_meber m on i.id = m.id where m.phone in('13012341111','13012341112')"
        # DButils.exe_sql(app.DB_MEMBER, sql2)
        # cls.log_recharge.info("delete sql = {}").format(sql2)
        # sql3 = "delete  from m_member where phone in('13012341111','13012341112')"
        # DButils.exe_sql(app.DB_MEMBER, sql3)
        # cls.log_recharge.info("delete sql = {}").format(sql3)

    def test001_get_recharge_code_float(self):
        res = self.login_api.login(self.session, self.phone1, self.password)
        assert_utils(self, res, 200, 200, "登录成功")
        # 获取充值验证码
        r = random.random()
        res = self.recharge_api.get_recharge_code(self.session, r)
        # self.log_recharge.info("recharge msg = {}".format(res.json()))
        self.assertEqual(200, res.status_code)

    def test002_get_recharge_info(self):
        res = self.login_api.login(self.session, self.phone1, self.password)
        assert_utils(self, res, 200, 200, "登录成功")
        # 获取充值验证码
        r = random.random()
        res = self.recharge_api.get_recharge_code(self.session, r)
        # self.log_recharge.info("recharge msg = {}".format(res.json()))
        self.assertEqual(200, res.status_code)

        res = self.recharge_api.get_recharge_info(self.session)
        self.log_recharge.info("recharge msg = {}".format(res.json()))
        self.assertEqual(200, res.status_code)

        res = request_third_party(res)
        print(res)
        self.assertEqual('NetSave OK', res.text)
