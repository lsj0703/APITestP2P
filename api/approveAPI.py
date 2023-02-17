import app

class approveAPI():
    def __init__(self):
        self.approve_url = app.BASE_URL + "/member/realname/approverealname"
        self.getapprove_url = app.BASE_URL + "/member/member/getapprove"
        self.trust_register_url = app.BASE_URL + "/trust/trust/register"

    def approve_realname(self, session, realname='李山丹', card_id='140203199211018203'):
        url = self.approve_url
        data = {
            "realname": realname,
            "card_id": card_id
        }
        # files多消息体传递参数multipart
        res = session.post(url, data=data, files={'x': 'y'})
        print(res)
        return res

    def get_approve(self, session):
        res = session.post(self.getapprove_url)
        return res

    def trust_register(self, session):
        res = session.post(self.trust_register_url)
        return res