#!/usr/bin/python3
#encoding:utf-8
import cgi, cgitb
import MSSQL
import json

#连接SQLServer数据库
ms=MSSQL.MSSQL(host=MSSQL.database_ipaddr,user=MSSQL.database_login_id,pwd=MSSQL.database_login_password,db="data_center_inspection_system")

#查询submit_state=1并且audit_state=0的(formname)元组组成的列表，即提交但未审核的巡检表
submit_unaudit_forms_list = ms.ExecQuery("SELECT formname FROM form_record WHERE submit_state='1' AND audit_state='0' ORDER BY formname")

print("Content-type:text/html")
print()
print(json.dumps(submit_unaudit_forms_list))#将字典转换成为JSON对象传给前端
