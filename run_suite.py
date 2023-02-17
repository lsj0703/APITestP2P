import unittest, time
import app, utils
from lib.HTMLTestRunner import HTMLTestRunner
from script.login import TestLogin
from script.approve import TestApprove
from script.recharge import TestRecharge

suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(TestLogin))
suite.addTest(unittest.makeSuite(TestApprove))
suite.addTest(unittest.makeSuite(TestRecharge))

report = app.BASE_DIR + f"/report/report-{time.strftime('%Y-%m-%d %H_%M_%S')}.html"

with open(report, 'wb')as f:
    runner = HTMLTestRunner(f, title="P2P项目测试报告")
    runner.run(suite)
