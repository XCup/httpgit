import json
import pymysql
class BmMysqli:
	'''
	 * @desc mysqli类
	 * @copyright Copyright 2010-2020 黑室计算机技术研究团队(www.000room.net)
	'''
	data = {} 
	_conn = None
	_column = {}
	_signEnum = {
		'eq' : '=',
		'neq' : '!=',
		'gt' : '>',
		'lt' : '<',
		'gteq' : '>=',
		'lteq' : '<=',
		'like' : 'LIKE',
		'In' : 'IN',
		'notIn' : 'NOT IN'
	}

	_sql = {}




	def run(self,data):
		# /**
		#  * @desc 调用run
		#  * 
		#  */
		obj = BmMysqli()
		obj.data = json.dumps(data)

		if obj.data['OPER'] == 'SELECT':
			return obj.select()
		elif obj.data['OPER'] == 'INSERT':
			return obj.add()
		elif obj.data['OPER'] == 'UPDATE':
			return obj.mod()
		elif obj.data['OPER'] == 'DELETE':
			return obj.delete()
		elif obj.data['OPER'] == 'COUNT':
			return obj.count()
		else:
			return None

	def count(self):
		'''
		@desc count 数据

		'''
		# 查询字段
		whereString = ''
		order = {}
		group = {}
		for fieldName,info in self.data['FILED']:
			#where 处理
			if (not info['where'] == None):
				for sign,where in info['where']:
					whereString = whereString + self._getWhere(fieldName,where,sign)
			#order 处理
			if (info['order'] == None):
				order = "{$fieldName} {$info['order']"
			#group 处理
			if(info['group'] == None):
				group = '{$fieldName}'

		orderString = ''
		if (not order == None):
			orderString = ' ORDER BY ' + ','.join(order)

		if (not group == None):
			groupString = ' GROUP BY' + ','.join(group)


		table = self.data['TABLE']
		sql = "SELECT count(*) as number FROM %s WHERE 1%s%s%s"% (table,whereString,groupString,orderString)
		res = self._sesql(sql)
		return res[0]['number']


		def select(self):
			#查询字段
			selectFields = {}
			whereString = ''
			order = {}
			group = {}
			for fieldName,info in self.data['FILED']:
				if(info['selectFields'] == ''):
					selectFields = fieldName

				if(not info['where'] == None):
					for where,sign in info['where']:
						whereString = whereString + self._getWhereString(fieldName ,where ,sign)

			if(info['order'] == None):
				order = fieldName + info['order']

			if(info['group'] == None):
				group = fieldName

			selectFields = "`" + "`,`".join(selectFields) + "`"

			orderString = ''
			if(not order == None):
				orderString = ' ORDER BY ' + ",".join(order)

			groupString = ''
			if(not group == None):
				groupString = ' GROUP BY ' + ",".join(group)

			limitString = ''
			if(not self.data['LIMIT'] == None):
				limitString = ' LIMIT ' + self.data['LIMIT']

			table = self.data['TABLE']
			self._conn()
			sql = "SELECT %s FROM %s WHERE %s%s%s%s" %(selectFields,table,whereString,groupString,orderString,limitString)
			res = self._sesql
			return json.dumps(res)

		def add(self):
			# 添加数据
			field = ''
			values = ''
			data = self.data['FILED']
			into = {}

			for name,Object in data:
				value = Object['value']
				into = "%s : '%s'" %(name,value)

			sql = "INSERT INTO %s SET " % self.data['TABLE'] + ",".join(into)
			res = self._query(sql)
			return res

		def mod(self):
			#修改数据
			ret = self.testColumn()
			if(ret != 'success'):
				return self.msg == '字段与数据库不符'
			fields = ''
			whereString = ''
			data = self.data['FILED']
			#拼接sql
			for value,key in data:
				if (not info['where'] == None):
					for where,sign in info['where']:
						whereString = whereString + self._getWhereString(fieldName,where,sign)

				if(value['value'] == None):
					continue
				fields = fields + key + "='%s',"% value['value']

			fields = fields[0:-1]
			sql = "UPDATE"+self.data['TABLE'] + "SET %s WHERE 1" %fields + whereString
			res = self._query(sql)
			return res

		def delete(self):
			#删除数据
			whereString = ''
			for fieldName,info in self.data['FILED']:
				#where处理
				if(not info['where'] == None):
					for sign,where in info['where']:
						whereString = whereString + self._getWhereString(fieldName,where,sign)

			sql = 'DELETE FROM '+ self.data['TABLE'] + ' WHERE 1' + whereString
			res = self._query(sql)
			return res

		def isexist(self):
			#判断是否存在该表
			data = {}
			self._conn()
			msg = 'error'
			cursor = self.conn.cursor(cursor = pymysql.cursor.DictCursor)
			result = cursor.execute('SHOW TABLES')
			key = 'Tables_in_' + self.data['PROTOCOL']['user']
			self._close
			if (self.data['TABLE'].lower() in data):
				msg = 'success'
			return msg


		def	_createTable(self):
			#创建数据库表
			sql = "CREAT TABLE" + self.data['TABLE'] + '('
			data = self.data['FILED']

			for key,value in data:
				sql = sql + key + ' ' + value['type']
				if(not value['defValue'] == None):
					#默认值
					sql = sql + ' DEFAULT' + value['defValue']
				if(value['key'] == 'primaryKey'):
					#是否主键
					sql = sql + ' PRIMARY KEY'
				if(value['symbol'] == False):
					sql = sql + " UNSIGNED"

				sql = sql + " COMMENT '%s'," %value['desc']

			sql = sql[0:-1]
			sql = sql + ')'

			res = self._query(sql)
			return res

		def addColumn(self):
			#在已有表中添加字段
			data = self._column
			arr = {}
			for key,value in self.data['FILED']:
				if(key in data):
					arr[key] = value

			sql = "ALTER TABLE %s ADD" % self.data['TABLE']
			for key,value in arr:
				sql = sql + key + ' ' + value['defValue']
				if(not value['defValue'] == None):
					sql = sql + ' DEFAULT' + value['defValue']
				if(value['symbol'] == False):
					sql = sql + ' UNSIGNED'

				sql = sql + " COMMENT '%s',"% value["desc"]

			sql = sql[0:-1]
			self._query(sql)




		def testColumn(self):
			#检测数据库的栏位和应用数据是否匹配
			msg = 'success'
			data = self.data['FILED']
			tablename = self.data['TABLE']

			sql = "select column_name from information_schema.COLUMNS where table_name = '%s'" % tablename

			res = self._sesql(sql)

			#判断和数据库是否匹配
			for key,value in data:
				if (not value in res):
					self._column[key] = value
					msg = 'error'

			return msg
		def _getWhereString(self,fieldName,arr,sign):
			#获取Where数据
			logic = arr[1]
			value = arr[0]

			if(sign == 'In' or sign == 'notIn'):
				value = "('" + "','".join(value) + "'"
			else:
				value = "'%s'" % value

			sign = self._signEnum[sign] if(self._signEnum[sign] == '') else sign
			return "%s `%s` %s %s" %(logic,fieldName,sign,value)

		def _sesql(self,sql):
			#执行 查
			self._conn()
			try:
				cursor = self.conn.cursor(cursor = pymysql.cursor.DictCursor)
				cursor.execute(sql)
				retval = cursor.fetchall
			except:
				print("ERROR:" + sql + "<br>")
			self._close
			return retval

		def _query(self,sql):
			#执行 增，删，改
			self._conn()
			try:
				self.cursor.execute(sql)
				self.conn.commit()
			except:
				self.conn.rollback()
			self._close
			return 'success'

		def _conn(self):
			#连接数据库
			conn = pymysql.connect(self.data['PROTOCOL']['host'],self.data['PROTOCOL']['user'],self.data['PROTOCOL']['password'],self.data['PROTOCOL']['database'])
			cursor = conn.cursor()
			if(conn == None):
				exit('Could not connect:' )
			else:
				self._conn = conn

		def _close(self):
			#关闭数据库
			self._conn._close()
			
		def _output(self,msg = 'success',s_data = ''):
			seeSql = ''
			if(1):
				seeSql = self._sql
			arr = {
				'msg' : msg,
				'data' : s_data,
				'sql' : seeSql
			}
			return json.dumps(arr)

