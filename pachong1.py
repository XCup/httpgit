import tornado
import tornado.web
import tornado.ioloop
import demjson
import pymysql
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write()
    def post(self, *args, **kwargs):
        time = self.get_argument('commit')
        print(time)
if __name__ == '__main__':
    app = tornado.web.Application ([
        ('/save', MainHandler)
    ])
    app.listen (8884)
    tornado.ioloop.IOLoop.instance ().start ()
