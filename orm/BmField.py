import time

class DefField(object):
	entityName = ''
	#数据源相关
	name = None #字段名
	type = None#类型
	value = None #值
	desc = None #字段描述
	defValue = None #默认值
	fromat = None #格式化参数
	entity = None #外建模型
	fields = [] #外键参数
	key = None #是否为键
	symbol = True #是否有符号

	#数据源操作相关
	where = {} #格式['eq'=>['23','AND']]
	group = False
	selectField = True
	order = [] #排序，顺序

	#属性特点相关
	dbValue = None #数据库格式值
	enumData = []

	def __init__( self,name, defValue, desc):
		self.desc = desc if (len(desc)>0) else None #三目运算符
		self.name = name if (len(name)>0) else None
		self.defValue = defValue


	# def __call(name,arg):
	# 	methods = ('eq','neq','gt','lt','like','in','notIn')
	# 	if name in methods:
	# 		if (arg[1]!=None):
	# 			arg.append('AND')
	# 			arg.insert(1,name)
	# 			#return call_user_func_array(array($this,'where'),$arg) 向函数'where'传 参数 arg		
		
		
		#错误提示
		# $methodsArray = [];
  #       foreach($methods as $met)
  #       {
  #           $methodsArray[] = "{$this->entityName}->{$this->name}->{$met}();";
  #       }
		#trigger_error("entity method is not found!  {$this->entityName}->{$this->name}->{$name}(".json_encode($arg).") \n\nmethods contain: \n" . implode("\n", $methodsArray) . "\n\n");
	
	def dbValue2Value(value):
		return value

    # /**
    #  * where object
    #  *
    #  * @param  [type] $conf  eq | lt | gt | lteq
    #  * @param  [type] $value value
    #  * @param  [type] $logic AND | OR
    #  *
    #  * @return void
    #  */
    	
	def where(self,conf, value, logic):
		self.where = {conf:{value:logic}}



	def eq (self,value,logic):
		print(logic)
		if logic == '':
			logic = 'AND'
		self.where('eq', value, logic)


	def neq(self,value,logic):
		if logic == '':
			logic = 'AND'
		self.where( 'neq', value, logic )


	def gt(self,value,logic):
		if logic == '':
			logic = 'AND'
		self.where('gt', value, logic)

	def lt (self,value,logic):
		if logic == '':
			logic = 'AND'
		self.where('lt', value, logic)

	def gteq (self,value,logic):
		if logic == '':
			logic = 'AND'
		self.where('gteq', value, logic)

	def like (self,value,logic):
		if logic == '':
			self.logic = 'AND'
		self.where('like', value, logic)

	def In (self,value,logic):
		if logic == '':
			logic = 'AND'
		self.where('In', value, logic)

	def notIn(self,value,logic):
		if logic == '':
			logic = 'AND'
		self.where('notIn', value, logic)

	def asc(order = 0):
		order = ['ASC',order]

	def desc(order = 0):
		order = ['DESC',order]

# //主键
# /**
#  * @desc 主键
#  * @param  string $name 字段名称
#  * @param  string $desc 备注
#  * @return object
#  */

class BMPrimaryKey(DefField):
	def __init__(self,name,desc):
		self.type = 'char(32)'
		self.key = 'primaryKey'

# /**
#  * @desc 外键
#  * @param  string $name   字段名称
#  * @param  string $entity 模型名称
#  * @param  string $desc   备注
#  * @param  array  $fields 外键需要的字段
#  * @return void
#  */

class BMForeignKey(DefField):
	def __init__(self,name,entity,desc,fields = []):
		self.type = 'char(32)'
		self.key = 'foregnKey'
		self.entity = entity
		self.fields = fields

# /**
#  * @desc String类型
#  * @param  string $name   字段名称
#  * @param  string $name   备注
#  * @param  string $defValue 默认值
#  * @return void
#  */
class BMString(DefField):
	def __init__(self,name,defValue,desc):
		self.type = 'char(255)'


# /**
#  * @desc Int类型
#  * @param  string $name   字段名称
#  * @param  string $name   备注
#  * @param  string $defValue 默认值
#  * @return void
#  */

class BMInt(DefField):
	def __init__(self,name,defValue,desc):
		self.type = 'int(20)'

# /**
#  * @desc float类型
#  * @param  string $name   字段名称
#  * @param  string $name   备注
#  * @param  string $defValue 默认值
#  * @return void
#  */

class BMFloat(DefField):
	def __init__(self,name,defValue,desc):
		self.type = 'float(10,10)'

# /**
#  * @desc money金钱类型
#  * @param  string $name   字段名称
#  * @param  string $name   备注
#  * @param  string $defValue 默认值
#  * @return void
#  */

class BMMoney(DefField):
	def __init__(self,name,defValue,desc):
		self.type = 'float(10,2)'

# /**
#  * @desc Time时间类型
#  * @param  string $name   字段名称
#  * @param  string $name   备注
#  * @param  string $defValue 默认值
#  * @return void
#  */

class BMTime(DefField):
	def __init__(self,name,defValue,desc,format = 'Y年m月d日 H时i分s秒'):
		self.type = 'int(10)'
		self.format = format

    # /**
    #  * @desc 转换格式
    #  * @param  string $format 格式样式
    #  * @return void
    #  */

	def formatValue(dbValue,fromat = 'Y年m月d日 H时i分s秒'):
		format = format
		if (dbValue == None):
			value = time.asctime(format)

    # /**
    #  * @desc 转换格式
    #  * @param  string $value 时间戳
    #  * @return string
    #  */

	def dbValue2Value(value):
		return time.asctime(format,value)

    # /**
    #  * @desc 设置值
    #  * @param  string $timestamp 时间戳
    #  * @return void
    #  */
	def setTimestamp(timestamp = ''):
		value = time.strftime() if(timestamp == None) else timestamp

# /**
#  * @desc Text文本类型
#  * @param  string $name   字段名称
#  * @param  string $name   备注
#  * @param  string $defValue 默认值
#  * @return void
#  */

	class BMText(DefField):
		def __init__(self,name,defValue,desc):
			self.type = 'text'

# /**
#  * @desc Enum枚举类型
#  * @param  string $name   字段名称
#  * @param  string $name   备注
#  * @param  string $defValue 默认值
#  * @return void
#  */

	class BMEnum(DefField):
		def __init__(self, defValue, desc ,enumData = {}):
			self.type = 'int(1)'
			self.enumData = enumData

		def dbValue2Value(value,enumData):
			return enumData [value] == enumData[0] if(enumData == None) else enumData[value]