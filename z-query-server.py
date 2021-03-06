#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
import xlrd
import sys
import pymysql
import json

def query_from_mysql(keywords):
	conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='Dw199719',db='QQQA',charset='utf8')
	cur = conn.cursor
		#create cursor
	cur = conn.cursor()
	#use DB QQQA
	cur.execute("USE QQQA")
	
	#multiKeywords
	query_exe = "select Question,Answer from `QA` where concat(Question,',',Answer) like '%{}%'".format(keywords[1])
	if len(keywords) > 2:
		for keyword in range(2,len(keywords)):
			query_exe = query_exe + " and concat(Question,',',Answer) like '%{}%'".format(keywords[keyword])
	
	#fetching result	
	query_nrow = cur.execute(query_exe)
	query_result = cur.fetchall()
	inventories = []
	
	#formatting it
	for row in query_result:
		inventroy = {}
		question = row[0]
		answer = row[1]
		inventroy['Q:'] = "Q:{}\n".format(question) 
		inventroy['A:'] = "A:{}\n".format(answer)
		inventroy_js = json.dumps(inventroy,ensure_ascii=False)
		print(inventroy)
		inventories.append(inventroy_js)
	print("\n共计{}个结果".format(str(query_nrow)))
	return_result = [inventories,json.dumps({'count':query_nrow},ensure_ascii=False)]
	#print(return_result)
	#close cursor
	cur.close()
	#conn_rollback
	try:
		conn.commit()
	except Exception:	
		conn.rollback()
	#close connection
	conn.close()
	return return_result
	
if __name__ == '__main__':
	query_from_mysql(sys.argv)