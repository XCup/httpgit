import BmBase
import BmHelper
class BmProcessInput:
	#过程输入的保准格式类
	value = ''
	valedation = '{"method":"","params":""}'
	desc = ''


	def __init__(self,valedation = '', desc = ''):
		#@desc 构造函数
		#@param  string  $valedation json串 需要验证的字段
		#@param  string  $desc       备注
		#@return void

		self.valedation = valedation
		self.desc = desc

 
class BmProcess:
#BM过程基类


	Input = None
	# 输入对象
	output = None
	#输出对象
	context = None
	#上下文对象

	def getInstance(self,args = {}):
	#获得实例
	#array args 参数
	# return class
		Class = getattr()
		return Class(args)

	def run(self,args = {}):
		#执行
		# arry args 参数
		#return object

		obj = self.getInstance(args)
		res = obj.Input()

		if(res != False):
			res = obj.valedation()
		if(res !=False):
			res = obj.process()
		if(res !=False):
			obj.output()

	def Input(self):
		#处理输入基础方法
		pass

	def valedation(self):
		#处理验证基础方法
		pass

	def process(self):
		#处理过程基础方法
		pass

	def output(self):
		#处理输出基础方法
		for value,key in self.context:
			if (self.output.key != None):
				BmBase.setContext(value,key)
				self.output.key = value

	def getInput(self,key):
		#获取上下文
		#string value 值
		#string key 键
		#return array
		return self.Input.key.value if(self.Input.key.value == None) else None

	def setContext(self,value,key):
		#设置上下文
		#string value 值
		#string key 键
		#return array
		self.context = BmHelper.setArrayValueByStringKey(self.context,value,key)

	def setContext(self,key = 'all'):
		#获取上下文
		#string key 键名
		#string | nono | array | object
		return BmHelper.getArrayValueByStringKey(self.context,key)

