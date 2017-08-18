#!/usr/bin/python3
#encoding:utf-8

# CGI处理模块
import cgi, cgitb
import MSSQL

#FieldStorage 的实例化
form = cgi.FieldStorage() 

username=form.getvalue('username')
password=form.getvalue('password')

#查询数据库，判断用户名和密码是否匹配，如果匹配返回对应的真实名字truthname，并用unicode编码，如果不匹配则返回False
def get_truthname(usrname,passd):
	#连接SQLServer数据库
	ms=MSSQL.MSSQL(host=MSSQL.database_ipaddr,user=MSSQL.database_login_id,pwd=MSSQL.database_login_password,db="data_center_inspection_system")
	#查询username对应的(password,truthname,authorized)元组组成的列表
	query_tuple_list = ms.ExecQuery("SELECT password,truthname FROM credentials WHERE username='"+username+"'")
	
	if len(query_tuple_list)==0: #当返回的元组列表为空时，表示username没有在数据库中查询到
		return '账户不存在'
	elif password==query_tuple_list[0][0]: #当数据库中的密码query_tuple_list[0][0]等于用户输入的密码password，返回真实名字。真实名字编码成utf-8，便于传值给cookie，cookie无法识别中文
		return query_tuple_list[0][1].encode('utf-8')
	else:
		return '密码错误' #当username存在，且密码不匹配，则返回“密码错误”


'''
get_name的测试版本
def sample_get_truthname(usrname,passd):
	if usrname=='admin' and passd=='admin123':
		return '管理员'.encode('utf-8') #编码成utf-8，便于传值给cookie，cookie无法识别中文
	else:
		return False
'''

#将python的utf-8编码格式转换为utf-8的URL编码格式
def transfer_utf8_to_URL(utf8code):
	utf8code=utf8code.replace("\\","%")
	utf8code=utf8code.replace("x","")
	utf8code=utf8code.replace("'","")
	utf8code=utf8code[1:] #去掉python的utf-8编码的首个字符'b'
	return utf8code

#将返回的名字或False的结果赋予变量truthname，该变量类型是byte，经过utf8编码后的二进制码
#truthname=sample_get_truthname(username,password)
truthname=get_truthname(username,password)
if truthname=='账户不存在':
	#如果truthname返回值是账户不存在，说明username输入错误，重新加载登录界面
	print("Content-type:text/html;charset=gbk")
	print()
	print('<html xmlns="http://www.w3.org/1999/xhtml">')
	print('<head>')
	print('<meta http-equiv="refresh" content="1;url=../index.html";charset=utf-8" >')
	print('<meta name="viewport" content="width=device-width, initial-scale=1" />')
	print('<title>登录提醒</title>')
	print('</head>')
	print('<body>')
	print('<div align="center">')
	print('<tr>')
	print('<td colspan="11"><div align="center">账户不存在，请重新输入。1秒后自动跳转。</div></td>')
	print('</tr>')
	print('</body>')
	print('</html>')
elif truthname=='密码错误':
	#如果truthname返回值是密码错误，说明password输入错误，重新加载登录界面
	print("Content-type:text/html;charset=gbk")
	print()
	print('<html xmlns="http://www.w3.org/1999/xhtml">')
	print('<head>')
	print('<meta http-equiv="refresh" content="1;url=../index.html";charset=utf-8" >')
	print('<meta name="viewport" content="width=device-width, initial-scale=1" />')
	print('<title>登录提醒</title>')
	print('</head>')
	print('<body>')
	print('<div align="center">')
	print('<tr>')
	print('<td colspan="11"><div align="center">密码错误，请重新输入。1秒后自动跳转。</div></td>')
	print('</tr>')
	print('</body>')
	print('</html>')
elif truthname:#如果取到了真实名字，且不是返回“账户不存在”或“密码错误”说明登录成功，并设定Cookie
	#从数据库中获取用户级别
	#连接SQLServer数据库
	ms=MSSQL.MSSQL(host=MSSQL.database_ipaddr,user=MSSQL.database_login_id,pwd=MSSQL.database_login_password,db="data_center_inspection_system")
	#查询username对应的(password,authorized)元组组成的列表
	password_and_authorized_list = ms.ExecQuery("SELECT password,authorized FROM credentials WHERE username='"+username+"'")
	authorized=password_and_authorized_list[0][1]
	password_value=password_and_authorized_list[0][0]
	print('Content-type:text/html;charset=gbk')
	#将用户名设置进入Cookie
	print('Set-Cookie: username=%s;Path=/' % username) #将cookie路径改为/根目录，否则默认设置路径为/cgi-bin/。
	#将真实的名字设置进入Cookie
	print('Set-Cookie: truthname=%s;Path=/' % transfer_utf8_to_URL(str(truthname))) #将utf8编码转换成URL编码，并将类型改为字符串
	#将用户级别设置进入Cookie
	print('Set-Cookie: authorized=%s;Path=/' % authorized)
	#将用户密码设置进入Cookie
	print('Set-Cookie: password=%s;Path=/' % password_value)
	print()
	print('<html xmlns="http://www.w3.org/1999/xhtml">')
	print('<head>')
	print('<meta http-equiv="refresh" content="1;url=../console_panel.html";charset=utf-8" >')
	print('<meta name="viewport" content="width=device-width, initial-scale=1" />')
	print('<title>登录提醒</title>')
	print('</head>')
	print('<body>')
	print('<div align="center">')
	print('<tr>')
	#显示登录成功信息，跳转到主页
	print('<td colspan="11"><div align="center">登录成功，欢迎%s。1秒后自动跳转。</div></td>' % truthname.decode('utf-8'))
	print('</tr>')
	print('</body>')
	print('</html>')