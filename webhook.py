import sys, subprocess

__author__ = "liuzhenwei"


class Trigger(object):

    def __init__(self):
        '''
        初始化文件列表信息，提交者信息，提交时间,当前操作的分支
        '''
        self.pushAuthor = ""
        self.pushTime = ""
        self.fileList = []
        self.ref = ""

    def __getGitInfo(self):
        '''
        '''
        self.oldObject, self.newObject, self.ref = sys.stdin.readline().strip().split(' ')

    def __getPushInfo(self):
        '''
        git show命令获取push作者，时间，以及文件列表
        文件的路径为相对于版本库根目录的一个相对路径
        '''

        rev = subprocess.Popen('git rev-list ' + self.newObject, shell=True, stdout=subprocess.PIPE)
        revList = rev.stdout.readlines()
        revList = [x.strip() for x in revList]

        # 查找从上次提交self.oldObject之后还有多少次提交，即本次push提交的object列表
        indexOld = revList.index(self.oldObject)
        pushList = revList[:indexOld]

        # 循环获取每次提交的文件列表
        for pObject in pushList:
            p = subprocess.Popen('git show ' + pObject, shell=True, stdout=subprocess.PIPE)
            pipe = p.stdout.readlines()
            pipe = [x.strip() for x in pipe]

            self.pushAuthor = pipe[1].strip("Author:").strip()
            self.pushTime = pipe[2].strip("Date:").strip()

            self.fileList.extend(['/'.join(fileName.split("/")[1:]) for fileName in pipe if
                                  fileName.startswith("+++") and not fileName.endswith("null")])

    def getGitPushInfo(self):
        '''
        返回文件列表信息，提交者信息，提交时间
        '''
        self.__getGitInfo()
        self.__getPushInfo()

        print("Time:", self.pushTime)
        print("Author:", self.pushAuthor)
        print("Ref:", self.ref)
        print("Files:", self.fileList)


if __name__ == "__main__":
    t = Trigger()
    t.getGitPushInfo()