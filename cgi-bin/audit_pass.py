#!/usr/bin/python3
#encoding:utf-8

# 导入模块
import cgi, cgitb
import os
import MSSQL
import time

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

audit_formname_value=get_cookie('formname') #获取客户端cookie formname的值
auditor_username_value=get_cookie('username') #获取客户端cookie username的值
form_audit_date_time=time.strftime('%Y-%m-%d %X', time.localtime()) #获取服务器的系统时间来作为巡检表审核时间

if auditor_username_value=="cookie不存在": #如果没有获取到username的cookie值则返回登录界面
	print("Content-type:text/html;charset=gbk")
	print()
	print('<html xmlns="http://www.w3.org/1999/xhtml">')
	print('<head>')
	print('<meta http-equiv="refresh" content="1;url=../index.html";charset=utf-8" >')
	print('<meta name="viewport" content="width=device-width, initial-scale=1" />')
	print('<title>新建巡检表</title>')
	print('</head>')
	print('<body>')
	print('<div align="center">')
	print('<tr>')
	print('<td colspan="11"><div align="center">用户未登陆，请重新登录。</div></td>')
	print('</tr>')
	print('</div>')
	print('</body>')
	print('</html>')
elif audit_formname_value=="cookie不存在":#如果没有获取到formname的cookie值则返回操作界面
	print("Content-type:text/html;charset=gbk")
	print()
	print('<html xmlns="http://www.w3.org/1999/xhtml">')
	print('<head>')
	print('<meta http-equiv="refresh" content="1;url=../console_panel.html";charset=utf-8" >')
	print('<meta name="viewport" content="width=device-width, initial-scale=1" />')
	print('<title>新建巡检表</title>')
	print('</head>')
	print('<body>')
	print('<div align="center">')
	print('<tr>')

	print('<td colspan="11"><div align="center">未选定巡检表，请重新选择。</div></td>')

	print('</tr>')
	print('</div>')
	print('</body>')
	print('</html>')
else:
	#连接SQLServer数据库
	ms=MSSQL.MSSQL(host=MSSQL.database_ipaddr,user=MSSQL.database_login_id,pwd=MSSQL.database_login_password,db="data_center_inspection_system")
	#将formname对应的audit_state改为"1"
	ms.ExecNonQuery("UPDATE form_record SET audit_state='1' , auditor_username='"+str(auditor_username_value)+"' , form_audit_date_time='"+str(form_audit_date_time)+"' WHERE formname = "+"'"+str(audit_formname_value)+"'")

	print("Content-type:text/html;charset=gbk")
	print()
	print('<html xmlns="http://www.w3.org/1999/xhtml">')
	print('<head>')
	print('<meta http-equiv="refresh" content="1;url=../audit_form.html";charset=utf-8" >')
	print('<meta name="viewport" content="width=device-width, initial-scale=1" />')
	print('<title>新建巡检表</title>')
	print('</head>')
	print('<body>')
	print('<div align="center">')
	print('<tr>')

	print('<td colspan="11"><div align="center">巡检表'+str(audit_formname_value)+'审核通过。</div></td>')

	print('</tr>')
	print('</div>')
	print('</body>')
	print('</html>')