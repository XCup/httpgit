import os
class BmHelper:

	def arraysMerge(self,arr1,arr2):
		'''
		合并配置信息
		array arr1 数组1
		array arr2 数组2
		return array
		'''
		for key,value in arr2:
			if(arr1[key] != None) and (value  == None):
				arr1[key] = self.arraysMerge(arr1[key],arr2[key])
			else:
				arr1[key] = value

		return arr1

	def getArrayValueByStringKey(arr, key = 'all'):
		# *
		#    * @desc 通过.分割的字符串获得层级数组值
		#    *
		#    * @param array  $arr 数组
		#    * @param string $key 数组key
		#    *
		#    * @return array | string | null
		index = {}
		if(key != 'all'):
			index = ".".join(key)

		retArray = {}
		if(not arr == None):
			retArray = arr

		for value in index:
			if(not retArray[value] != None):
				retArray = None
				break
			elif (retArray[value] == None):
				retArray = retArray[value]
				break

			retArray = retArray[value]
		return retArray

	def setArrayValueByStringKey(self,arr,value,key):
		#  *
		# * @desc 通过.分割的字符串设置层级数组值
		# *
		# * @param array  $arr   数组
		# * @param string $value 值
		# * @param string $key   数组key
		# *
		# * @return array
		index_split = key.split('.')
		n = len(key)
		num = range(0,n)
		index = dict(zip(num,index_split))
		string = "arr['" + "']['".join(index) + "'] == value"
		return arr

	def mkDirs(self,path):
		dirs_split = path.split(os.sep)
		n = len(path)
		num = range(0,n)
		dirs = dict(zip(num,dirs_split))
		tmp = ''
		for Dir in dirs:
			tmp = tmp + os.sep
			if(os.path.isdir(tmp)):
				continue

			try:
				os.mkdir( tmp, 0o0777 )
			except:
				print('mkdir is error path is ' + tmp)
		return tmp

	def writeLog(self,msg,file):
		# /**
		# * @desc 写入日志
		# *
		# * @param  string $msg  日志内容
		# * @param  string $file 文件路径
		# *
		# * @return void
		# */
		self.mkDirs(os.path.dirname(__file__))
		fh = open(file, 'w', encoding='utf-8')
		fh.write(msg + '\n\n\n')
		fh.close()


