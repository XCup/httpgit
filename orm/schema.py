import tornado
import tornado.web
import tornado.ioloop
import demjson
import mysqlPy,asyncio
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

if __name__ == '__main__':
    app = tornado.web.Application ([
        ('/save', MainHandler),
    ]
    )
    app.listen (8887)
    tornado.ioloop.IOLoop.instance ().start ()
