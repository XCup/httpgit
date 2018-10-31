from BmField import DefField
DefField = DefField('1111',1111,'111')
a = DefField.eq(1111,111111)
print(a)

#class 内函数调用
logic = 2
value = 1
def where(conf,value,logic):
	where = {conf:{value:logic}}
	print(where)
def eq(value,logic):
	print(logic)
	if logic == '':
		logic ='AND'
	where('eq',value,logic)
print(eq(1,''))