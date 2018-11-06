import os
import json
import re
import time
import hashlib
import uuid
import math
import BmBase

def curlmd5(src):
    m = hashlib.md5()
    m.update(src.encode('UTF-8'))
    return m.hexdigest()


 
		

class BmEntity:

	

	class BmEntitySource:
		PROTOCOL = ''
		INDEX = ''
		FILED = {}
		TABLE = ''
		OPEN = ''
		LIMIT = ''
		TABLEINFO = {}


		def __init__(self,entity):
			'''
			@desc 构造方法
			@param object $entity 实体对象
			@return void
			待修1: 用户级别的错误报告
			'''
			try:
				TABLE = entity.TABLE
			except Exception as e:
				print('table not found')
				
			indexField = entity.getIndexField()
			try:
				INEDX = indexField
			except Exception as e:
				print('index field not found')




		
		def setField(field):
			# /**
		    #  * @desc 设置实体数据栏位方法
		    #  * @param array $field 栏位数据数组
		    #  * @return void
		    #  */
			FILED = field

		

		def setProtocol(pro):
			# /**
			#  * @desc 设置协议方法
			#  * @param array $pro 协议
			#  * @return void
			#  */
			PROTOCOL = pro



	class BmPage:
		# /**
		#  * @desc 分页数据类型格式
		#  */ 待修2: 空变量
		page = None
		last = None
		displayline = None
		pre = None
		next = None
		totle = None

	TABLE = None
	_source = None
	_settingModel = False
	_list = {}
	_page = None
	_msg = ''
	_fields = {}
	_indexField = None


	def __init__(self):
		self._initConfig()
		self._initPorperty()
		self._source = BmEntity.BmEntitySource(self)
		self._initTable()
		self._page = None


	
	
	def _initConfig(self):
		# /**
		# * @desc 初始化模块配置
		# * @param array $field 栏位数据数组
		# * @return void
		pass
		
		
	def _bmFieldHandler(self,object,value):
		# /**
		#  * @desc   处理特殊属性
		#  * @param  object $object 当前对象
		#  * @param  object $value  数据
		#  * @return object    a ? a :b    =     a if(a == '') else b 返回值  a(if a !='') or b(if a == '')
		#  */  待修5: get IndexField 和 getProperty
		dbValue = ''

		if(getattr(object,'__name__') == 'bm\\BmField\\BMEnum'):
			enumData = object.enumData
			index = enumData.get(value)
			dbValue = index if(index == '') else 0

		if(getattr(object,'__name__') == 'bm\\BmField\\BMTime'):
			format = object.format
			data = value.asctime(format)
			dbValue = data.getTimestamp if (data == '') else 0

		if(getattr(object,'__name__') == 'bm\\BmField\\BMForeignKey'):
			if(type(value) == 'str'):
				dbValue = value
				value == None
			if(type(value) == 'object'):
				indexName = value.getIndexField()
				property1 = value.getProperty
				dbValue = property1[indexName].value

		object.value = value
		object.dbValue = dbValue
		return object

	def set(self,name,val):
		class1 = (getattr(self,'__name__'))
		if (not hasattr(self,name)):
			print("%s .property name not found" % getattr(self,'__name__'))

		pro = class1.getProperty(name)
		object = pro.getValue(self)

	def get(self, name):
		class1 = (getattr(self,'__name__'))
		if(hasattr(self,name) == None):
			print("%s .property name not found" % getattr(self,'__name__'))

		pro = class1.getProperty(name)
		return pro.getValue(self) if(self._settingModel == '') else pro.getValue(self).value

		
	def settingSpace(self,fun):
		"""	@desc 设置值
		@param  function  $fun 方法
		$str = 'f57d897691729fada425ea406f9f0170';
		$entity->settingSpace(function($obj){
		global $str;
		$obj->id->eq($str);
		})->select()->show();
		@return object"""
		self._settingModel == True
		fun(self)
		self._settingModel == False
		return self


	def getIndexField(self):

		# /**
		# * @desc 获取主键
		# * @return object
		# */
		return self._indexField


	def getProperty(self,isRefresh = False):
		# /**
		# * @desc 获取属性
		# * @param  boolean $isRefresh 
		# * @return object
		# */
		if (isRefresh):
			self._initPorperty()
			return self._fields



	def _callDBSource(self,oper):
		# /**
		# * 解析输出
		# * @param  string $oper 操作
		# * @return obj    对象
		# * PROTOCOL array(
		# *     protocol 协议 BmMysqli|Oracle|DB等
		# *     user  用户名
		# *     password 密码
		# *     host 地址
		# *     database 库名
		# *     language 编码格式
		# * )
		# * INDEX 主键
		# * FILED array(
		# *     entityName  实体名称
		# *     name 字段名
		# *     type 类型
		# *     value 值
		# *     cacheValue 缓存值
		# *     desc 备注
		# *     defValue 默认值
		# *     format 格式
		# *     key (primaryKey主键 foreignKey外键)
		# *     symbol 符号（null true false）
		# *     entity 实体
		# *     enumData array(0=>'a', 1=>'b')枚举
		# *     where array(['eq'=>['23', 'AND']];)条件
		# *     group 分组
		# *     selectField 是否被查询的字段 true or false
		# *     order 正序 | 倒序排序， 顺序 ['desc', '1']
		# * )
		# * TABLE 表名
		# * OPER 操作
		# * LIMIT 分页条数
		# * TABLEINFO 表介绍内容array(
		# *     protocol 链接array(
		# *         'r' => '读',
		# *         'w' => '写'
		# *     )
		# *     tablename 表名
		# *     prefix 表前缀
		# *     cache 缓存
		# * )
		# * PAGE  当前页码
		# */
		_list = {}
		_page = None
		_msg = ''

		self._source.OPER = oper
		sourceKey = 'r' if(oper == 'SELECT') else 'w'
		pro = self._source.TABLEINFO['protocol'][sourceKey]

		fields = self.getProperty(True)
		selectField = {}
		for name,property1 in fields:
			if (property1.selectField == None):
				continue
			fields[name].value = property1.dbValue
			selectField[name] = fields[name]

		self._source.setField(selectField)
		self._source.setProtocol(self._protocolHandler(pro))
		jsonSource = json.dumps(self._source)

		protocol = self._source.PROTOCOL['protocol']
		class1= "\\bm\\protocol"
		return json.dumps(class1.jsonSource)

	def checkDataShema(self):
		return self._callDBSource('CHECK')



	def insert(self):
		name = self.getIndexField()
		self.name = curlmd5(uuid.uuid1())
		self._msg = self._callDBSource('INSERT').msg
		return self

	def dele(self):
		self._msg = self._callDBSource('DELETE').msg
		return self

	def mod(self):
		self._msg = self._callDBSource('UPDATE').msg
		return self

	def select(self):
		json = self._callDBSource('SELECT').msg
		self.fromJson(json)
		return self



	def list(self,page,displayline = 9):
		# /**
		# * @desc list
		# *
		# * @param int $page 当前页码
		# * @param int $displayline 一页显示条数
		# * @return object
		# */
		totle = self.len()

		start = page - 1
		limit = '{start},{displayline}'
		self._source.LIMIT = limit
		self.select()

		lastpg = math.ceil (totle / displayline)

		pageObject = self.BmPage
		pageObject.page = page
		pageObject.last = lastpg
		pageObject.displayline = displayline
		pageObject.pre = (lastpg if(page == lastpg) else page +1)
		pageObject.totle = totle
		
		_page = pageObject

		return self

	def getCount(self):
		return self._callDBSource("COUNT")

	def getData(self):
		return self._list

	def getPage(self):
		return self._page

	def getMessage(self):
		return self._msg



	def isSuccess(self):
		# /**
		# * @desc 成功
		# * 
		# * @return bool
		# */
		return self._msg == 'success'



	def fromJson(self,json,obj = None):
		# /**
		# * @desc 整理json
		# * 
		# * @param json   $json   json串
		# * @param object $obj    当前对象
		# * 
		# * @return object
		# */
		if(obj ==None):
			class1 = getattr(self,'__name__')
			obj = class1()

		self._list =self._renderPropertyValue(json,obj)

		if(len(self._list) == 1):
			properties = obj.getProperty()
			obj = self._list[0]
			for name,property1 in properties:
				self.name = obj.name
		return self


	def _renderPropertyValue(json,object):
		# /**
		# * @desc 渲染
		# * 
		# * @param json   $json   json串
		# * @param object $object 当前对象
		# * 
		# * @return array
		# */

		properties = object.getProperty
		class1 = getattr(object,'__name__')
		foreignKeys = []

		if(type(json) != 'array'):
			json = [json]

		for name,property1 in properties:
			if (not property1.selectField or getattr(property1,'__name__') != 'bm\\BmField\\BMForeignKey'):
				continue
			data = list(set(json.get(name)))
			foreignKeys[name] = data

		for name,indexs in foreignKeys:
			entity = properties[name].entity
			fields = properties[name].fields

			if(indexs == None):
				data = object.getByIds(entity(),indexs,fields)
				foreignKeys[name] = data

		ret = {}
		for obj in json:
			arrData = class1()
			for name,property1 in properties:
				if(object.name == ''):
					value = object.name1
				if (getattr(property1,'__name__') == 'bm\\BmF	ield\\BMForeignKey'):
					value = foreignKeys[name] if(foreignKeys[value] == '') else None
				arrData.name = property1.dbValue2Value(value)
			ret = arrData
		return ret

	def func(self,obj):
		global ids
		IndexField = obj.getIndexField()
		obj.IndexField.In(ids)

	def getByIds(self,object,ids ,fields,obj):
		# /**
		# * @desc 根据ids查询
		# * 
		# * @param object $object 当前对象
		# * @param array  $ids    ids数组
		# * @param object $fields 查询字段
		# * 
		# * @return object
		# */
		object.setSelectFields(fields)
		res = object.settingSpace(self.func(obj)).select().getData()

		del ids
		ret = {}
		for obj in res:
			ret[obj.id] = obj
		return ret


	def func1(obj):
		global names
		properties = obj.getProperty
		for property1,name in properties:
			obj.name.selectField = True if(name in names) else False

	def setSelectFields(self,obj,names = None):
		# /**
		# * @desc 根据ids查询
		# * 
		# * @param object $object 当前对象
		# * @param array  $ids    ids数组
		# * @param object $fields 查询字段
		# * 
		# * @return object
		# */
		properties = self.getProperty()
		n = len(properties)
		num_properties = range(0,n)
		dict_properties = dict(zip(num_properties,properties))
		names = dict_properties if (names == None) else names
		self.settingSpace(self.func1(obj))
		del names


	def toJson(self):
		# /**
		# * @desc 转换为json
		# * 
		# * @param  
		# * 
		# * @return json
		# */	
		obj = self.stdclass()
		obj.entity = getattr(self,'__name__')
		obj.message = self._msg
		obj.page = self._page
		obj.content = self.stdclass()
		data = self._object2Json(self._list)
		if (len(self._list) < 1):
			obj.content = data[0] if(data[0] == '') else None
		else:
			obj.content.list = data
		return json.dumps(obj)

	def show(self,debug = ''):
		# /**
		# * @desc 显示json数据
		# * 
		# * @param  
		# * 
		# * @return void
		# */
		print(json.dumps(self.toJson()))


	def _protocolHandler(self,str1):
		# /**
		#  * @desc 根据SQL协议获得参数
		#  * 
		#  * @param  string $connStr 连接字符串
		#  * 
		#  * @return array
		#  */
		protocol_x = str1[0:str1.index('://')]
		protocol = protocol_x.capitalize()
		str1 = str1[str1.index('://')+3:len(str1)] 
		p_split = str1.split('@')
		n = len(str1)
		num = range(0,n)
		p = dict(zip(num,p_split))
		if(len(p)>3):
			p2 = p[len(p) - 1]
			p1 = p[len(p) - 2]
			p0 = str1.replace("'@' . p1 . '@' . p2" , '')
			strArray = {}
			strArray[0] = p0
			strArray[1] = p1
			strArray[2] = p2
		else:
			strArray = p
		u_split = strArray[0].split(':') 
		n = len(strArray)
		num = range(0,n)
		u = dict(zip(num,u_split))

		dl_split = strArray[2].split(':')
		n = len(strArray[2])
		num = range(0,n)
		dl = dict(zip(num,dl_split))

		return{
			'protocol' : protocol,
			'user' : u[0],
			'password' : u[1],
			'host' : strArray[1],
			'database' : dl[0],
			'language' : dl[1] if (dl[1] != None) else ''
		}



	def _initPorperty(self):
		# /**
		# * @desc 初始化属性
		# * 
		# * @param  
		# * 
		# * @return void
		# */

		# class1 = ReflectionClass(getattr(self,'__name__'))
		# propertys = class1.getProperties()
		# array = ['bm\\BmField\\BMPrimaryKey', 'bm\\BmField\\BMForeignKey', 'bm\\BmField\\BMString', 'bm\\BmField\\BMInt', 'bm\\BmField\\BMFloat', 'bm\\BmField\\BMMoney', 'bm\\BmField\\BMTime', 'bm\\BmField\\BMText', 'bm\\BmField\\BMEnum']
		# self._fields = {}
		# for k,v in propertys:
		# 	pro = class1.getProperty(v.name)
		# 	propertyObj = pro.getValue(self)

		# 	if (type(propertyObj) != 'boject' or not re.search(getattr(propertyObj,'__name__'),array)):
		# 		continue
		# 	if (getattr(propertyObj,'__name__') == 'bm\\BmField\\BMPrimaryKey'):
		# 		_indexField = v.name

		# 	propertyObj.entityName = getattr(self,'__name__')
		# 	self._fields[v.name] = propertyObj
		pass


	def _initTable(self):
		# /**
		# * @desc table信息
		# * 
		# * @param  
		# * 
		# * @return void
		# */

		class1 = getattr(self,'__name__')
		classArr_split = class1.split('\\')
		n = len(class1)
		num = range(0,n)
		classArr = dict(zip(num,classArr_split))
		namespace = classArr[0] if (classArr != None) else ''
		db = BmBase.getConfig('%s.db') %namespace
		if(db != ''):
			db = BmBase.getConfig('db')

		tableInfo = {
			'protocol' : db,
			'tablename' : self.TABLE,
			'prefix' : '',
			'cache' : ''
		}
		self._source.TABLEINFO = tableInfo


	def _object2Json(self,info):
		'''
		@desc 递归函数
		 
		@param $info  array|object
		
		@return array
		'''

		if(type(info) == 'array'):
			ret = {}
			for key,value in info:
				ret[key] = self._object2Json(value)
			return ret

		if (type(info) == 'object'):
			ret = {}
			names_key = info.getProperty()
			n = len(info.getProperty)
			num = range(0,n)
			names = dict(zip(num,names_key))
			for name in names:
				ret.name = self._object2Json(info.name)
			return ret
		return info



#getValue 什么意思   