<<<<<<< HEAD
import pymysql

#class mysqlConPython ():
# def connectmysql(self):
#
#     #cursor.execute('SELECT VERSION()') #查询数据库信息
#     #data = cursor.fetchone()
#     #print("Database version: %s" % data)
#     return db

def selectsql(sql):
    db = pymysql.connect('localhost', 'root', '123456', 'gitdb',charset = 'utf8')
    cursor = db.cursor()
    print(sql)
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        return results
    except:
        print("error:unable to fetch data")
    db.close()

def insertsql(sql):
    db = pymysql.connect('localhost', 'root', '123456', 'gitdb',charset = 'utf8')
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
        print("error:mother fucker")
    db.close()

# sql = "DELETE FROM Users" #删除数据
# try:
#     cursor.execute(sql)
#     db.commit()
# except:
#     db.rollback()
# db.close()

# import mysql.connector #廖雪峰 mysql python 链接
# conn=mysql.connector.connect(user='root',password='123456',database='gitdb')
# cursor = conn.cursor()
# cursor.execute('insert into users (username,passwd,lv) values (%s,%s,%d)',['XCup','123456',10])
=======
import pymysql

#class mysqlConPython ():
# def connectmysql(self):
#
#     #cursor.execute('SELECT VERSION()') #查询数据库信息
#     #data = cursor.fetchone()
#     #print("Database version: %s" % data)
#     return db

def selectsql(sql):
    db = pymysql.connect('localhost', 'root', '123456', 'gitdb',charset = 'utf8')
    cursor = db.cursor()
    print(sql)
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        return results
    except:
        print("error:unable to fetch data")
    db.close()

def insertsql(sql):
    db = pymysql.connect('localhost', 'root', '123456', 'gitdb',charset = 'utf8')
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
        print("error:mother fucker")
    db.close()

# sql = "DELETE FROM Users" #删除数据
# try:
#     cursor.execute(sql)
#     db.commit()
# except:
#     db.rollback()
# db.close()

# import mysql.connector #廖雪峰 mysql python 链接
# conn=mysql.connector.connect(user='root',password='123456',database='gitdb')
# cursor = conn.cursor()
# cursor.execute('insert into users (username,passwd,lv) values (%s,%s,%d)',['XCup','123456',10])
>>>>>>> 79d6a477cdaf6ace01063f6a4412dd7d8bb10d22
# "INSERT INTO Users(username,passwd,lv) VALUES ('%s','%s','%d')" % ('XCup','123456',10) # 增加数据