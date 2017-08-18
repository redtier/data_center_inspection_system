#!/usr/bin/python3

# CGI处理模块
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

formname_value=get_cookie('formname') #获取客户端cookie formname的值
username_value=get_cookie('username') #获取客户端cookie username的值
form_submit_date_time=time.strftime('%Y-%m-%d %X', time.localtime()) #获取服务器的系统时间来作为巡检表提交时间

if username_value=="cookie不存在": #如果没有获取到username的cookie值则返回登录界面
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
elif formname_value=="cookie不存在":#如果没有获取到formname的cookie值则返回操作界面
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
	#formname的submit_state值改为1，即已提交状态;将form_submit_date_time巡检表的提交日期和时间写入数据库。
	ms.ExecNonQuery("UPDATE form_record SET submit_state = '1', form_submit_date_time = '"+str(form_submit_date_time)+"' WHERE formname = "+"'"+str(formname_value)+"'")

	print("Content-type:text/html;charset=gbk")
	##将Cookie提交状态submit_state的值设置为"1"
	print('Set-Cookie: submit_state=1;Path=/')
	print()
	print('<html xmlns="http://www.w3.org/1999/xhtml">')
	print('<head>')
	print('<meta http-equiv="refresh" content="1;url=../form_query_export.html";charset=utf-8" >')
	print('<meta name="viewport" content="width=device-width, initial-scale=1" />')
	print('<title>提交审核</title>')
	print('</head>')
	print('<body>')
	print('<div align="center">')
	print('<tr>')
	print('<td colspan="11"><div align="center">已成功提交审核。1秒后自动跳转。</div></td>')
	print('</tr>')
	print('</body>')
	print('</html>')