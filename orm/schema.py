import tornado
import tornado.web
import tornado.ioloop
import mysqlPy,asyncio
from models import entity
class MainHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.write("hello")
    def post(self, *args, **kwargs):
        message=self.get_argument('commit')
        type = 233
        async def test(loop):
            await mysqlPy.create_pool(loop,user='bm',password='bm!@#123',db='dev')
            u = entity(data=message)
            await u.save()


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
