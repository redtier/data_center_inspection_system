#!/usr/bin/python3
#encoding:utf-8
import cgi, cgitb
import os
import MSSQL
import json

def get_cookie(cookiename):
	cookie_dic={}
	if 'HTTP_COOKIE' in os.environ:
		cookie_string=os.environ.get('HTTP_COOKIE')
		cookie_string=cookie_string.replace('=',';') #将cookie字符串中的等号替换成分号
		cookie_string=cookie_string.replace(' ','') #删除cookie字符串中的空格
		cookie_string=cookie_string.split(';') #以分号为分界，将字符串变为数组，数组偶数为cookie名，数组奇数为cookie值
		for i in range(len(cookie_string)-1):#将数组的奇数位和偶数位对应成为字典cookie_dic
			if (i%2)==0:
				cookie_dic[cookie_string[i]]=cookie_string[i+1]
			else:
				continue		
	try:
		return cookie_dic[cookiename] #返回所要查询的cookie名所对应的值
	except KeyError:
		return "cookie不存在"#如果Key不存在，则返回空字符串

query_formname=get_cookie('formname') #获取客户端cookie formname的值
#query_formname="2017070305"
#query_formname="2017072402"
#query_formname="2017072002"

#连接SQLServer数据库
ms=MSSQL.MSSQL(host=MSSQL.database_ipaddr,user=MSSQL.database_login_id,pwd=MSSQL.database_login_password,db="data_center_inspection_system")
#查询formname对应的(表form_record所有列)元组组成的列表
query_form_tuple_list = ms.ExecQuery("SELECT * FROM form_record WHERE formname='"+str(query_formname)+"'")
#将查询到的元组列表中的元组元素转换为列表，即形成2元列表，用于insert操作
query_form_tuple_list[0]=list(query_form_tuple_list[0])

#将查询的巡检表的巡检人的用户名赋予变量query_recorder_username
query_recorder_username=query_form_tuple_list[0][1]
#将查询的巡检表的审核人的用户名赋予变量query_auditor_username
query_auditor_username=query_form_tuple_list[0][2]

#将巡检人的真实名字recorder_truthname插入query_form_tuple_list[0]第2个位置
#查询recorder_username对应的(表credentials的truthname)列表组成的列表
query_recorder_truthname_tuple_list = ms.ExecQuery("SELECT truthname FROM credentials WHERE username='"+str(query_recorder_username)+"'")
if len(query_recorder_truthname_tuple_list)!=0: #如果数据库credentials中巡检人的真实名字的查询结果不为空
	query_form_tuple_list[0].insert(2,query_recorder_truthname_tuple_list[0][0])#巡检人的真实名字插入到列表query_form_tuple_list[0]的第2位置
else:#否则在列表query_form_tuple_list[0]的第2位置插入None
	query_form_tuple_list[0].insert(2,None)

#将审核人的真实名字auditor_truthname插入query_form_tuple_list[0]第4个位置
#查询auditor_username对应的(表credentials的truthname)列表组成的列表
query_auditor_truthname_tuple_list = ms.ExecQuery("SELECT truthname FROM credentials WHERE username='"+str(query_auditor_username)+"'")
if len(query_auditor_truthname_tuple_list)!=0:#如果数据库credentials中审核人的真实名字的查询结果不为空
	query_form_tuple_list[0].insert(4,query_auditor_truthname_tuple_list[0][0])#巡检人的真实名字插入到列表query_form_tuple_list[0]的第4位置
else:#否则在列表query_form_tuple_list[0]的第4位置插入None
	query_form_tuple_list[0].insert(4,None)

#将巡检表表单状态query_form_state插入query_form_tuple_list[0]第7个位置
if query_form_tuple_list[0][5]=="1":#如果提交状态submit_state为1表示已提交（0表示未提交）
	query_form_state="已提交"
	if query_form_tuple_list[0][6]=="1":#如果提交状态audit_state为1表示已审核（0表示未审核）
		query_form_state="已审核"
else:query_form_state="未提交" #否则表单状态为未提交
query_form_tuple_list[0].insert(7,query_form_state)#将巡检表表单状态query_form_state插入query_form_tuple_list[0]第7个位置

#将最终表单列表query_form_tuple_list[0][]中的所有为字符串"None"值的元素，替换为None
for i in range(len(query_form_tuple_list[0])):
	if query_form_tuple_list[0][i]=="None":
		query_form_tuple_list[0][i]=None

print("Content-type:text/html")
print()
print(json.dumps(query_form_tuple_list))#将最终形成的2元列表即list[[]]转换成为JSON对象传给前端