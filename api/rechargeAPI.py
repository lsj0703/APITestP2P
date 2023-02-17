import app
import requests


class rechargeAPI():
    def __init__(self):
        self.recharge_code_url = app.BASE_URL + "/common/public/verifycode/{}"
        self.recharge_info_url = app.BASE_URL + "/trust/trust/recharge"

    def get_recharge_code(self, session, r):
        url = self.recharge_code_url.format(r)
        res = session.get(url)
        return res

    def get_recharge_info(self, session, paymentType='chinapnrTrust', amount='1000', formStr='reForm', valicode='8888'):
        url = self.recharge_info_url
        data = {
            "paymentType": paymentType,
            "amount": amount,
            "formStr": formStr,
            "valicode": valicode
        }
        res = session.post(url, data=data)
        return res

# session = requests.Session()
# s = rechargeAPI()
# s.get_recharge_code()
