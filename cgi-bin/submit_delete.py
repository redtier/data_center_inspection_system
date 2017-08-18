#!/usr/bin/python3
#encoding:utf-8
import cgi, cgitb
import MSSQL
import json

#FieldStorage 的实例化
form = cgi.FieldStorage() 

#获取form_query_export.html的ajax传来的delete_formname，即用户输入的需要删除的巡检表的名字
delete_formname=form.getvalue('delete_formname')

#连接SQLServer数据库
ms=MSSQL.MSSQL(host=MSSQL.database_ipaddr,user=MSSQL.database_login_id,pwd=MSSQL.database_login_password,db="data_center_inspection_system")

#将formname为delete_formname从数据库表form_record中删除
ms.ExecNonQuery("DELETE FROM form_record WHERE formname="+str(delete_formname))

#构建删除结果的字典，将delete_success（删除成功）返还给ajax
delete_result_dic={"delete_result":"delete_success"}

print("Content-type:text/html")
print()
print(json.dumps(delete_result_dic))#将字典转换成为JSON对象传给前端