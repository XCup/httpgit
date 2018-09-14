#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time,uuid
from mysqlPy import Model,StringField,FloatField,BooleanField
def next_id():
	return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)

class entity(Model):
	' User类映射MySQL数据库中的User表 '
	__table__ = 'entity' #表名
	id = StringField(primary_key=True, default=next_id, ddl='varchar(50)') #主键
	data = StringField(ddl='varchar(50)')
	platform = BooleanField ()
	system = BooleanField ()
	function = BooleanField ()
	type = BooleanField ()
	addtime =  FloatField(default=time.time)
