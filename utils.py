import os
import logging, requests, pymysql
from logging import handlers
import json
import xlrd
import time
import app
from bs4 import BeautifulSoup


# 通用日志生成方法
def init_log_config(logname=''):
    # 初始化日志
    logger = logging.getLogger(logname)
    # 设置日志级别CRITICAL ERROR WARNING INFO DEBUG NOTSET
    logger.setLevel(logging.INFO)
    # 创建控制台日志处理器和文件日志处理器
    sh = logging.StreamHandler()
    # 设置日志输出地址
    # s = time.strftime("%Y-%m-%d %H-%M-%S")
    s = time.strftime("%Y-%m-%d")
    logfile = app.BASE_DIR + os.sep + "log" + os.sep + "{} {}.log".format(logname, s)
    # 输出日志到文件到处理器
    fh = logging.handlers.TimedRotatingFileHandler(logfile, when='M', interval=20, backupCount=0,
                                                   encoding='utf-8')
    # 设置日志格式，创建格式化器
    fmt = '%(asctime)s %(levelname)s [%(name)s] [%(filename)s(%(funcName)s:%(lineno)d)] - %(message)s'
    fmter = logging.Formatter(fmt=fmt)
    # 将格式化器设置到日志器中
    # sh.setLevel(logging.INFO)
    # fh.setLevel(logging.INFO)
    sh.setFormatter(fmter)
    fh.setFormatter(fmter)
    # 将处理器添加到日志器
    logger.addHandler(sh)
    logger.addHandler(fh)
    return logger


# 通用断言方法
def assert_utils(self, res, status_code, status, desc):
    self.assertEqual(status_code, res.status_code)
    self.assertEqual(status, res.json().get('status'))
    self.assertIn(desc, res.json().get('description'))


# 通用第三方接口
def request_third_party(res):
    html = res.json().get('description').get('form')
    soup = BeautifulSoup(html, 'html.parser')
    url = soup.form['action']
    data = {}
    for i in soup.find_all('input'):
        data.setdefault(i['name'], i['value'])
    res = requests.post(url, data=data)
    return res


# 数据库工具类
class DButils:
    __conn = None
    __cursor = None

    # 类方法可以不用实例化对象直接调用
    @classmethod
    def __get_coon(cls, database):
        if cls.__conn is None:
            cls.__conn = pymysql.connect(
                host=app.DB_URL,
                port=3306,
                user=app.DB_USERNAME,
                passwd=app.DB_PASSWORD,
                database=database,
                charset='utf8'
            )
        return cls.__conn

    @classmethod
    def __get_cursor(cls, database):
        if cls.__cursor is None:
            cls.__cursor = cls.__get_coon(database).cursor()
        return cls.__cursor

    @classmethod
    def exe_sql(cls, database, sql):
        try:
            cursor = cls.__get_cursor(database)
            cursor.execute(sql)

            if sql.split(' ')[0].lower() == 'select':
                return cursor.fetchall()
            else:
                cls.__conn.commit()
                return cursor.rowcount()
        except Exception as e:
            cls.__conn.rollback()
            print(e)
        finally:
            cls.__close()

    @classmethod
    def __close(cls):
        if cls.__cursor:
            cls.__cursor.close()
            cls.__cursor = None
        if cls.__conn:
            cls.__conn.close()
            cls.__conn = None


# 解析json文件的方法
def get_data(file_name, desc_name, params):
    # file_name文件名称
    # desc_name文件中的列表名称
    # params文件中的测试数据
    data = []
    file = app.BASE_DIR + "/data/" + file_name
    with open(file, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
        for i in json_data.get(desc_name):
            l_data = []
            for e in params:
                l_data.append(i.get(e))
            data.append(l_data)
        print(data)
    return data