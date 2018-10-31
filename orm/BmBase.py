#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-10-21 23:36:48
# @Author  : Copyright 2018-2028 黑室计算机技术研究团队(www.000room.net)
# @Version : python 3.6.3

import os
import json
import uuid
import base64
import traceback

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.netutil import bind_sockets
from tornado.web import Application, RequestHandler
from tornado.process import fork_processes, task_id


def print_r(objects):
    if BmBase.HANDLER is not None:
        BmBase.HANDLER.write(objects)

    print("BM DEBUG: ")
    print(objects)
    print("\n\n")


class BmBase(object):

    def execute(self, config):
        BmBase.CONTEXT = {}
        BmBase.CONFIG = {}
        BmBase.INPUT = {}
        BmBase.COOKIE = {}
        BmBase.FILES = {}
        BmBase.INFO = {}

        BmBase.HANDLER = None
        BmBase.MODULEPATH = os.sys.path[1]

        self._config(config)
        BmBase.CmdServer().do(self.initApp())

    def initApp(self):
        settings = {
            'gzip': True,
            'cookie_secret': base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes),
            'debug': BmBase.CONFIG['server']['scenes'] == 'debug',
            # 'template_path' : '',
            #'xheaders' : '',
            #'log_file_prefix' : '',
            #'ui_module':
            #'static_path':
        }
        return Application(
            [("/.*", BmBase.RootHandler)], BmBase.CONFIG['server']['host'], None, **settings)

    class RootHandler(RequestHandler):

        def initialize(self):
            BmBase.HANDLER = self

        def get(self, *args, **kwargs):
            self._requestHandler(args)

        def post(self, *args, **kwargs):
            self._requestHandler(args)

        def _requestHandler(self, *args, **kwargs):

            for name in self.request.arguments:
                data = self.get_arguments(name)
                if len(data) > 1:
                    BmBase.INPUT[name] = data
                else:
                    BmBase.INPUT[name] = data[0]

            for name in self.request.body_arguments:
                data = self.get_body_argument(name)
                if len(data) > 1:
                    BmBase.INPUT[name] = data
                else:
                    BmBase.INPUT[name] = data[0]

            for name in self.request.cookies:
                BmBase.COOKIE[name] = self.get_cookie(name)

            router = BmBase.CONFIG['router']
            if 'v' in BmBase.INPUT:
                router['v'] = BmBase.INPUT['v']

            BmBase.CONTEXT = BmBase.INPUT
            importString = router['s'] + '.' + router['m'] + '.' + router['v']
            __import__(importString)

    def _config(self, config):
        data = __import__(config)
        BmBase.CONFIG = data.config

    class CmdServer(object):

        _app = None

        def do(self, app):
            self._app = app
            file = os.path.abspath(os.sys.argv[0])
            file = file.replace(BmBase.MODULEPATH, '')
            BmBase.CmdServer.key = file.replace(os.path.sep, '.')
            self.config = BmBase.CONFIG['server']

            if len(os.sys.argv) > 1:
                cmd = os.sys.argv[1]
            else:
                cmd = ''

            if cmd == 'start':
                self.start()
            elif cmd == 'stop':
                self.stop()
            elif cmd == 'restart':
                self.restart()
            elif cmd == 'status':
                self.status()
            elif cmd == 'test':
                self.test()
            elif cmd == BmBase.CmdServer.key:
                self.serverStart()
            else:
                print("error params please use: start | stop | restart | status | test")

        def test(self):
            self.serverStart()

        def start(self):
            print("server start ip: " + self.config['ip'] +
                  " port: " + str(self.config['port']))
            string = self.config['python'] + " " + os.sys.argv[0] + ' ' + BmBase.CmdServer.key + \
                " > /tmp/http_" + BmBase.CmdServer.key + ".log &"
            os.system(string)

        def stop(self):
            pids = self.getPids()
            print("close server")
            for pid in pids:
                shell = 'kill ' + pid
                print("stop pid " + pid)
                os.system(shell)

        def restart(self):
            self.stop()
            self.start()

        def status(self):
            print("server status: ")
            shell = 'ps -ef|grep ' + BmBase.CmdServer.key
            dataArray = os.popen(shell).read().split("\n")
            msgArray = []
            for data in dataArray:
                if data.find(os.sys.argv[0]) > 0:
                    msgArray.append(data)
            print("\n".join(msgArray))
            print("server process count: " + str(len(msgArray)))

        def getPids(self):
            shell = 'ps -ef|grep ' + BmBase.CmdServer.key + \
                '|grep -v grep|grep -v PPID|awk \'{ print $2}\''
            dataArray = os.popen(shell).read().split("\n")
            pids = []
            for data in dataArray:
                if data != "":
                    pids.append(data)
            return pids

        def serverStart(self):
            socket = bind_sockets(
                self.config['port'], self.config['ip'])
            if (self.config['scenes'] != 'debug'):
                fork_processes(self.config['thread'])
            server = HTTPServer(self._app)
            server.add_sockets(socket)
            IOLoop.current().start()
