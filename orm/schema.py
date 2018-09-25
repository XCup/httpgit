import tornado
import tornado.web
import tornado.ioloop
import demjson
import pymysql
import mysqlPy,asyncio
import simplejson as json
from models import entity
class MainHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.write("hello")
    def post(self, *args, **kwargs):
        message=self.get_argument('commit')
        data1 = self.get_argument('name[]')
        data2 = self.get_argument('length[]')
        data3 = self.get_argument('type[]')
        data4 = self.get_argument('desc[]')
        fields = [{"name":data1,"length":data2,"type":data3,"desc":data4}]
        u1 = {"table":message,"fields":fields}
        u = str(u1)
        json = demjson.encode(u)
        print(u)
        print(u1)
        print(json)

        async def test(loop):
            await mysqlPy.create_pool(loop,user='bm',password='bm!@#123',db="dev" )
            fin = entity(data = json)
            await fin.save()


        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait([test(loop)]))
        loop.run_forever()
class SelectHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        print("setting headers!!!")
        self.set_header("Access-Control-Allow-Origin", "*") # 这个地方可以写域名123
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    def get(self):
        self.write("hello")
    def post(self, *args, **kwargs):
        db = pymysql.connect ('www.000room.com', 'bm', 'bm!@#123', 'dev', charset='utf8')        # 打开数据库连接
        cursor = db.cursor ()# 使用cursor()方法获取操作游标
        sql = "SELECT COLUMN_NAME 列名,COLUMN_TYPE 数据类型,DATA_TYPE 字段类型,CHARACTER_MAXIMUM_LENGTH 长度,IS_NULLABLE 是否为空,COLUMN_DEFAULT 默认值,COLUMN_COMMENT 备注 FROM INFORMATION_SCHEMA.COLUMNS where table_name  = 'entity' "
        try:
            cursor.execute (sql)            # 执行SQL语句
            results = cursor.fetchall ()            # 获取所有记录列表
            print (results)
        except:
            print ("Error: unable to fetch data")
        db.close ()        # 关闭数据库连接
        self.set_header ('Content-Type', 'application/json; charset=UTF-8')
        self.write (json.dumps ({ 'entity': results}))
        self.finish ()
if __name__ == '__main__':
    app = tornado.web.Application ([
        ('/save', MainHandler),
        ('/read',SelectHandler)
    ])
    app.listen (8887)
    tornado.ioloop.IOLoop.instance ().start ()
