import json
import pymysql
class BmMysqli:
	'''
	 * @desc mysqli类
	 * @copyright Copyright 2010-2020 黑室计算机技术研究团队(www.000room.net)
	'''
	data = [] 
	_conn = None
	_column = []
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
		for info in self.data['FILED']:
			#where 处理
			if (not info['where'] == None):
				for where in info['where']:
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
		sql = "SELECT count(*) as number FROM {$table} WHERE 1{$whereString}{$groupString}{$orderString}"
		res = BmMysqli._sesql(sql)
		return res[0]['number']


		def select(self):
			#查询字段
			selectFields = {}
			whereString = ''
			order = {}
			group = {}
			for info in self.data['FILED']:
				if(info['selectFields'] == ''):
					selectFields{} = fieldName