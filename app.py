import os


# 绝对路径，解决相对路径运行报错问题
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

BASE_URL = "http://user-p2p-test.itheima.net/"

headers = {"Content-Type": "application/x-www-form-urlencoded"}

DB_URL = "52.83.144.39"
DB_USERNAME = "root"
DB_PASSWORD = "Itcast_p2p_20191228"
DB_MEMBER = "czbk_member"
DB_FINANCE = "czbk_finance"
