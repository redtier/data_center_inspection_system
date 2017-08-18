#!/usr/bin/python3
#encoding:utf-8
import cgi, cgitb
import MSSQL

#FieldStorage 的实例化
form = cgi.FieldStorage() 

#获取console_panel.html的ajax传来的query_formname，即用户输入的需要查询的巡检表的名字
query_formname=form.getvalue('query_formname')

#连接SQLServer数据库
ms=MSSQL.MSSQL(host=MSSQL.database_ipaddr,user=MSSQL.database_login_id,pwd=MSSQL.database_login_password,db="data_center_inspection_system")
#查询formname对应的(formname)元组组成的列表
query_form_tuple_list = ms.ExecQuery("SELECT formname FROM form_record WHERE formname='"+str(query_formname)+"'")

if len(query_form_tuple_list)==0: #如果返回的列表为空，则表示查询的巡检表不存在，ajax响应文本为"false"
	xmlHttp_responseText='false'
else:
	xmlHttp_responseText='true' #如果返回的列表不为空，则表示查询的巡检表存在，ajax响应文本为"ture"

#将巡检表是否存在的结果xmlHttp_responseText通过cgi以文本格式响应给前端ajax,该文本格式将以JSON对象的方式发送给ajax。
print("Content-type: text/html")  #http 头信息必须
print() #这个空格一定要输入
print(xmlHttp_responseText)
