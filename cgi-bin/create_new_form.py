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

formname_value=get_cookie('formname') #获取客户端cookie formname的值
username_value=get_cookie('username') #获取客户端cookie username的值
form_create_date_time=time.strftime('%Y-%m-%d %X', time.localtime()) #获取服务器的系统时间来作为巡检表创建时间


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
	#查询formname对应的(formname)元组组成的列表
	query_tuple_list = ms.ExecQuery("SELECT formname FROM form_record WHERE formname='"+str(formname_value)+"'")
	if len(query_tuple_list)==0:#如果返回的列表是空，则表示数据库中没有该formname，则在数据库表form_record中插入该条目
		print("Content-type:text/html;charset=gbk")
		#将巡检表创建时间设置进Cookie
		print('Set-Cookie: form_create_date_time=%s;Path=/' % form_create_date_time) #将cookie路径改为/根目录，否则默认设置路径为/cgi-bin/。
		print()
		print('<html xmlns="http://www.w3.org/1999/xhtml">')
		print('<head>')
		print('<meta http-equiv="refresh" content="1;url=../new_form_input.html";charset=utf-8" >')
		print('<meta name="viewport" content="width=device-width, initial-scale=1" />')
		print('<title>新建巡检表</title>')
		print('</head>')
		print('<body>')
		print('<div align="center">')
		print('<tr>')

		#插入条目包含formname和recorder_name(username)和form_create_date_time
		ms.ExecNonQuery("INSERT INTO form_record (formname,recorder_username,form_create_date_time) VALUES ("+"'"+str(formname_value)+"'"+","+"'"+str(username_value)+"'"+","+"'"+str(form_create_date_time)+"'"+")")
		
		print('<td colspan="11"><div align="center">巡检表'+str(get_cookie('formname'))+'创建成功。1秒后自动跳转。</div></td>')

		print('</tr>')
		print('</div>')
		print('</body>')
		print('</html>')
	else:#否则表示formname存在于数据库，则不对数据库进行操作，返回console_panel.html
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

		print('<td colspan="11"><div align="center">巡检表'+str(get_cookie('formname'))+'已经存在，创建失败。1秒后自动跳转。</div></td>')

		print('</tr>')
		print('</div>')
		print('</body>')
		print('</html>')

