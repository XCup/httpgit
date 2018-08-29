# -*- coding: utf-8 -*-
import tornado
import tornado.web
import subprocess
import tornado.ioloop
import simplejson as json
import requests
import re
from bs4 import BeautifulSoup
class indexHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        print("setting headers!!!")
        self.set_header("Access-Control-Allow-Origin", "*") # 这个地方可以写域名123
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    def get(self, *args, **kwargs):
        self.write()
    def post(self, *args, **kwargs):
        message=self.get_argument('commit')
        type = 233


        def status():
            archiveCmd = 'git status'
            process = subprocess.Popen(archiveCmd, shell=True)
            process.wait()
            archiveReturnCode = process.returncode
            if archiveReturnCode != 0:
                print("查看工作区状态错误")
                self.set_header('Content-Type', 'application/json; charset=UTF-8')
                self.write(json.dumps({'type': 1}))
                self.finish()
            else:
                add()

            return True

        def add():
            archiveCmd = 'git add --all'
            process = subprocess.Popen(archiveCmd, shell=True)
            process.wait()
            archiveReturnCode = process.returncode
            if archiveReturnCode != 0:
                print("添加到缓存区错误")
                self.set_header('Content-Type', 'application/json; charset=UTF-8')
                self.write(json.dumps({'type': 2}))
                self.finish()
            else:
                commit()

        # 提交本地版本库
        def commit():
            archiveCmd = "git commit -m "+message
            process = subprocess.Popen(archiveCmd, shell=True)
            process.wait()
            archiveReturnCode = process.returncode
            if archiveReturnCode != 0:
                print("提交失败")
                self.set_header('Content-Type', 'application/json; charset=UTF-8')
                self.write(json.dumps({'type': 3}))
            else:
                print("提交成功"), message
                pull()

        # 拉取
        def pull():
            archiveCmd = 'git pull'
            process = subprocess.Popen(archiveCmd, shell=True)
            process.wait()
            archiveReturnCode = process.returncode
            if archiveReturnCode != 0:
                print("拉取远程代码失败")
                self.set_header('Content-Type', 'application/json; charset=UTF-8')
                self.write(json.dumps({'type': 4}))
                self.finish()
            else:
                push()

        # 推送
        def push():
            archiveCmd = 'git push'
            process = subprocess.Popen(archiveCmd, shell=True)
            process.wait()
            archiveReturnCode = process.returncode
            if archiveReturnCode != 0:
                print("上传远程git服务器失败")
                self.set_header('Content-Type', 'application/json; charset=UTF-8')
                self.write(json.dumps({'type': 5}))
                self.finish()
            else:
                r = requests.get('https://github.com/XCup/httpgit.git')
                # print(r.text)

                soup = BeautifulSoup(r.text, 'lxml')
                find = str(soup.find_all('span'))
                # print(find)
                key = find
                # p1 = r"(?<=title=\").*?(?=\">)"
                pattern1 = re.findall('(?<=title=\").*?(?=\">)', key, re.S)
                # pattern1 = re.compile(p1)
                # matcher1 = re.search(pattern1,key)
                # print(matcher1.group())
                # 123
                print(pattern1)
                print("上传成功")
                self.set_header('Content-Type', 'application/json; charset=UTF-8')
                self.write(json.dumps({'type': 0,'filename':pattern1}))
                self.finish()

        # 执行一哈
        def main():
            status()



        if __name__ == '__main__':
            main()

    def options(self):
        # no body
        self.set_status(204)
        self.finish()
class indexHandler1(tornado.web.RequestHandler):
    def set_default_headers(self):
        print("setting headers!!!")
        self.set_header("Access-Control-Allow-Origin", "*")  # 这个地方可以写域名
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    def get(self, *args, **kwargs):
        self.write()
    def post(self, *args, **kwargs):
        #message=self.get_argument('commit')


        def status():
            archiveCmd = 'git status'
            process = subprocess.Popen(archiveCmd, shell=True)
            process.wait()
            archiveReturnCode = process.returncode
            if archiveReturnCode != 0:
                print("查看工作区状态错误")
                self.set_header('Content-Type', 'application/json; charset=UTF-8')
                self.write(json.dumps({'type': 0}))
                self.finish()
            else:
                pull()

            return True

        # 拉取
        def pull():
            archiveCmd = 'git pull'
            process = subprocess.Popen(archiveCmd, shell=True)
            process.wait()
            archiveReturnCode = process.returncode
            if archiveReturnCode != 0:
                print("拉取远程代码失败")
                self.set_header('Content-Type', 'application/json; charset=UTF-8')
                self.write(json.dumps({'type': 4}))
                self.finish()
            else:
                print("拉取成功")
                self.set_header('Content-Type', 'application/json; charset=UTF-8')
                self.write(json.dumps({'type':0}))
                self.finish()


        def main():
            status()

        if __name__ == '__main__':
            main()
if __name__ == '__main__':
    app=tornado.web.Application([
        ('/pull',indexHandler1),
        ('/push', indexHandler),
    ]
    )
    app.listen(8889)
    tornado.ioloop.IOLoop.instance().start()