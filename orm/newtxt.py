# !/usr/bin/env 
# python  
# -*- coding: utf-8 -*-  
'makeTextFile.py--创建一个文本文件'
import os
#输入文件名  
while True :
    filename =input('输入文件名')
    if os.path.exists(filename):
        print('ERROR: %s already exists') % filename
    else:
        break
    #输入文件内容  
contents = []
print('/n输入每行文本，以#结束')
while True :
    entry = input('> ')
    if entry == '.':
        break
    else:
        contents.append(entry)
    #写入文件  
    fobj = open(filename, 'w')
    fobj.writelines(['%s%s'%(eachline,os.linesep)for eachline in contents])
    fobj.close()
    print('Done!')
