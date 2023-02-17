import pymysql


# 创建数据库测试数据
class BuildDB():
    __conn = None
    __cursor = None

    def __get_conn(self):
        if self.__conn is None:
            self.__conn = pymysql.connect(
                host='localhost',
                port=3306,
                user='root',
                passwd='root',
                database='books',
                charset='utf8'
            )
        return self.__conn

    def __get_cursor(self):
        if self.__cursor is None:
            self.__cursor = self.__get_conn().cursor()
        return self.__cursor

    def exe_sql(self, sql):
        try:
            cursor = self.__get_cursor()
            cursor.execute(sql)

            if sql.split(' ')[0].lower() == 'select':
                return cursor.fetchall()
            else:
                self.__conn.commit()
                return cursor.rowcount()
        except Exception as e:
            self.__conn.rollback()
            print(e)
        finally:
            self.__close()

    def __close(self):
        if self.__cursor:
            self.__cursor.close()
            self.__cursor = None

        if self.__conn:
            self.__conn.close()
            self.__conn = None
