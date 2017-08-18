#!/usr/bin/python3

# CGI处理模块
import cgi, cgitb
import os
import MSSQL

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

if username_value=="cookie不存在": #如果没有获取到username的cookie值则返回登录界面
  print("Content-type:text/html;charset=gbk")
  print()
  print('<html xmlns="http://www.w3.org/1999/xhtml">')
  print('<head>')
  print('<meta http-equiv="refresh" content="1;url=../index.html";charset=utf-8" >')
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
	#FieldStorage 的实例化
	form = cgi.FieldStorage() 

	#获取气象路温湿度数据
	qxl_tem=[]#温度数据
	qxl_hum=[]#湿度数据
	for i in range(10):
	  qxl_tem.append(form.getvalue('qxl_tem'+str(i+1)))
	  qxl_hum.append(form.getvalue('qxl_hum'+str(i+1)))
	qxl_temandhum_des=form.getvalue('qxl_temandhum_des')#备注数据

	#获取气象路精密空调数据
	qxl_ac_tem=[]#空调温度数据
	qxl_ac_hum=[]#空调湿度数据
	qxl_ac_open=[]#空调开启状态,开启为0，关闭为1
	qxl_ac_state=[]#空调状态，正常为0，异常为1
	qxl_ac_voice=[]#异常噪音，无为0，有为1
	for i in range(2):
	  qxl_ac_tem.append(form.getvalue('qxl_ac_tem'+str(i+1)))
	  qxl_ac_hum.append(form.getvalue('qxl_ac_hum'+str(i+1)))
	  qxl_ac_open.append(form.getvalue('qxl_ac_open'+str(i+1)))
	  qxl_ac_state.append(form.getvalue('qxl_ac_state'+str(i+1)))
	  qxl_ac_voice.append(form.getvalue('qxl_ac_voice'+str(i+1)))
	qxl_aircondition_des=form.getvalue('qxl_aircondition_des')#备注数据

	#获取气象路环境数据
	qxl_leak_45m=form.getvalue('qxl_leak_45m')#气象路45m漏水绳状态 正常为0 漏水为1
	qxl_leak_45m_spot=form.getvalue('qxl_leak_45m_spot')#气象路45m漏水绳漏水位置
	qxl_leak_15m=form.getvalue('qxl_leak_15m')#气象路15m漏水绳状态 正常为0 漏水为1
	qxl_leak_15m_spot=form.getvalue('qxl_leak_15m_spot')#气象路15m漏水绳漏水位置
	qxl_door=[]#气象路门的状态
	for i in range(4):
		qxl_door.append(form.getvalue('qxl_door'+str(i+1)))
	qxl_defend_state=form.getvalue('qxl_defend_state')#气象路入侵状态 打开为0 关闭为1
	qxl_environment_des=form.getvalue('qxl_environment_des')#气象路环境备注

	#获取气象路PMM精密配电柜
	#1号PMM精密配电柜UPS1-P0201-A数据
	qxl_pmm1={'uab':None,'ubc':None,'uca':None,'ia':None,'ib':None,'ic':None,'state':None}
	qxl_pmm1['uab']=form.getvalue('qxl_pmm1_uab')
	qxl_pmm1['ubc']=form.getvalue('qxl_pmm1_ubc')
	qxl_pmm1['uca']=form.getvalue('qxl_pmm1_uca')
	qxl_pmm1['ia']=form.getvalue('qxl_pmm1_ia')
	qxl_pmm1['ib']=form.getvalue('qxl_pmm1_ib')
	qxl_pmm1['ic']=form.getvalue('qxl_pmm1_ic')
	qxl_pmm1['state']=form.getvalue('qxl_pmm1_state')
	#2号PMM精密配电柜UPS2-P0201-B数据
	qxl_pmm2={'uab':None,'ubc':None,'uca':None,'ia':None,'ib':None,'ic':None,'state':None}
	qxl_pmm2['uab']=form.getvalue('qxl_pmm2_uab')
	qxl_pmm2['ubc']=form.getvalue('qxl_pmm2_ubc')
	qxl_pmm2['uca']=form.getvalue('qxl_pmm2_uca')
	qxl_pmm2['ia']=form.getvalue('qxl_pmm2_ia')
	qxl_pmm2['ib']=form.getvalue('qxl_pmm2_ib')
	qxl_pmm2['ic']=form.getvalue('qxl_pmm2_ic')
	qxl_pmm2['state']=form.getvalue('qxl_pmm2_state')
	#气象路PMM精密配电柜备注
	qxl_pmm_des=form.getvalue('qxl_pmm_des')

	#获取气象路低压电柜数据
	qxl_cabinet_uab=[]
	qxl_cabinet_ubc=[]
	qxl_cabinet_uca=[]
	qxl_cabinet_ia=[]
	qxl_cabinet_ib=[]
	qxl_cabinet_ic=[]
	qxl_cabinet_breaker_state=[]
	for i in range(5):
		qxl_cabinet_uab.append(form.getvalue('qxl_cabinet'+str(i+1)+'_uab'))
		qxl_cabinet_ubc.append(form.getvalue('qxl_cabinet'+str(i+1)+'_ubc'))
		qxl_cabinet_uca.append(form.getvalue('qxl_cabinet'+str(i+1)+'_uca'))
		qxl_cabinet_ia.append(form.getvalue('qxl_cabinet'+str(i+1)+'_ia'))
		qxl_cabinet_ib.append(form.getvalue('qxl_cabinet'+str(i+1)+'_ib'))
		qxl_cabinet_ic.append(form.getvalue('qxl_cabinet'+str(i+1)+'_ic'))
		qxl_cabinet_breaker_state.append(form.getvalue('qxl_cabinet'+str(i+1)+'_breaker_state'))
	#获取气象路低压电柜备注
	qxl_cabinet_des=form.getvalue('qxl_cabinet_des')

	#获取气象路UPS数据
	qxl_ups1={'inpower_l1':None,'inpower_l2':None,'inpower_l3':None,'expower_l1':None,'expower_l2':None,'expower_l3':None,'ini_l1':None,'ini_l2':None,'ini_l3':None,'exi_l1':None,'exi_l2':None,'exi_l3':None,'inu_l12':None,'inu_l23':None,'inu_l31':None,'exu_l12':None,'exu_l23':None,'exu_l31':None,'battery_state':None}
	qxl_ups2={'inpower_l1':None,'inpower_l2':None,'inpower_l3':None,'expower_l1':None,'expower_l2':None,'expower_l3':None,'ini_l1':None,'ini_l2':None,'ini_l3':None,'exi_l1':None,'exi_l2':None,'exi_l3':None,'inu_l12':None,'inu_l23':None,'inu_l31':None,'exu_l12':None,'exu_l23':None,'exu_l31':None,'battery_state':None}

	qxl_ups1['inpower_l1']=form.getvalue('qxl_ups1_inpower_l1')
	qxl_ups1['inpower_l2']=form.getvalue('qxl_ups1_inpower_l2')
	qxl_ups1['inpower_l3']=form.getvalue('qxl_ups1_inpower_l3')
	qxl_ups1['expower_l1']=form.getvalue('qxl_ups1_expower_l1')
	qxl_ups1['expower_l2']=form.getvalue('qxl_ups1_expower_l2')
	qxl_ups1['expower_l3']=form.getvalue('qxl_ups1_expower_l3')
	qxl_ups1['ini_l1']=form.getvalue('qxl_ups1_ini_l1')
	qxl_ups1['ini_l2']=form.getvalue('qxl_ups1_ini_l2')
	qxl_ups1['ini_l3']=form.getvalue('qxl_ups1_ini_l3')
	qxl_ups1['exi_l1']=form.getvalue('qxl_ups1_exi_l1')
	qxl_ups1['exi_l2']=form.getvalue('qxl_ups1_exi_l2')
	qxl_ups1['exi_l3']=form.getvalue('qxl_ups1_exi_l3')
	qxl_ups1['inu_l12']=form.getvalue('qxl_ups1_inu_l12')
	qxl_ups1['inu_l23']=form.getvalue('qxl_ups1_inu_l23')
	qxl_ups1['inu_l31']=form.getvalue('qxl_ups1_inu_l31')
	qxl_ups1['exu_l12']=form.getvalue('qxl_ups1_exu_l12')
	qxl_ups1['exu_l23']=form.getvalue('qxl_ups1_exu_l23')
	qxl_ups1['exu_l31']=form.getvalue('qxl_ups1_exu_l31')
	qxl_ups1['battery_state']=form.getvalue('qxl_ups1_battery_state')

	qxl_ups2['inpower_l1']=form.getvalue('qxl_ups2_inpower_l1')
	qxl_ups2['inpower_l2']=form.getvalue('qxl_ups2_inpower_l2')
	qxl_ups2['inpower_l3']=form.getvalue('qxl_ups2_inpower_l3')
	qxl_ups2['expower_l1']=form.getvalue('qxl_ups2_expower_l1')
	qxl_ups2['expower_l2']=form.getvalue('qxl_ups2_expower_l2')
	qxl_ups2['expower_l3']=form.getvalue('qxl_ups2_expower_l3')
	qxl_ups2['ini_l1']=form.getvalue('qxl_ups2_ini_l1')
	qxl_ups2['ini_l2']=form.getvalue('qxl_ups2_ini_l2')
	qxl_ups2['ini_l3']=form.getvalue('qxl_ups2_ini_l3')
	qxl_ups2['exi_l1']=form.getvalue('qxl_ups2_exi_l1')
	qxl_ups2['exi_l2']=form.getvalue('qxl_ups2_exi_l2')
	qxl_ups2['exi_l3']=form.getvalue('qxl_ups2_exi_l3')
	qxl_ups2['inu_l12']=form.getvalue('qxl_ups2_inu_l12')
	qxl_ups2['inu_l23']=form.getvalue('qxl_ups2_inu_l23')
	qxl_ups2['inu_l31']=form.getvalue('qxl_ups2_inu_l31')
	qxl_ups2['exu_l12']=form.getvalue('qxl_ups2_exu_l12')
	qxl_ups2['exu_l23']=form.getvalue('qxl_ups2_exu_l23')
	qxl_ups2['exu_l31']=form.getvalue('qxl_ups2_exu_l31')
	qxl_ups2['battery_state']=form.getvalue('qxl_ups2_battery_state')

	qxl_ups_des=form.getvalue('qxl_ups_des')


	#连接SQLServer数据库
	ms=MSSQL.MSSQL(host=MSSQL.database_ipaddr,user=MSSQL.database_login_id,pwd=MSSQL.database_login_password,db="data_center_inspection_system")
	#定义空字符串sql_string
	sql_string=""
	#将所有气象路机房数据写入字符串sql_string，使得sql_string形如"column1 = 'value1'，column2 = 'value',..."
	sql_string=sql_string+"qxl_tem1 = '"+str(qxl_tem[0])+"',"
	sql_string=sql_string+"qxl_tem2 = '"+str(qxl_tem[1])+"',"
	sql_string=sql_string+"qxl_tem3 = '"+str(qxl_tem[2])+"',"
	sql_string=sql_string+"qxl_tem4 = '"+str(qxl_tem[3])+"',"
	sql_string=sql_string+"qxl_tem5 = '"+str(qxl_tem[4])+"',"
	sql_string=sql_string+"qxl_tem6 = '"+str(qxl_tem[5])+"',"
	sql_string=sql_string+"qxl_tem7 = '"+str(qxl_tem[6])+"',"
	sql_string=sql_string+"qxl_tem8 = '"+str(qxl_tem[7])+"',"
	sql_string=sql_string+"qxl_tem9 = '"+str(qxl_tem[8])+"',"
	sql_string=sql_string+"qxl_tem10 = '"+str(qxl_tem[9])+"',"
	sql_string=sql_string+"qxl_hum1 = '"+str(qxl_hum[0])+"',"
	sql_string=sql_string+"qxl_hum2 = '"+str(qxl_hum[1])+"',"
	sql_string=sql_string+"qxl_hum3 = '"+str(qxl_hum[2])+"',"
	sql_string=sql_string+"qxl_hum4 = '"+str(qxl_hum[3])+"',"
	sql_string=sql_string+"qxl_hum5 = '"+str(qxl_hum[4])+"',"
	sql_string=sql_string+"qxl_hum6 = '"+str(qxl_hum[5])+"',"
	sql_string=sql_string+"qxl_hum7 = '"+str(qxl_hum[6])+"',"
	sql_string=sql_string+"qxl_hum8 = '"+str(qxl_hum[7])+"',"
	sql_string=sql_string+"qxl_hum9 = '"+str(qxl_hum[8])+"',"
	sql_string=sql_string+"qxl_hum10 = '"+str(qxl_hum[9])+"',"
	sql_string=sql_string+"qxl_temandhum_des = '"+str(qxl_temandhum_des)+"',"
	sql_string=sql_string+"qxl_ac_tem1 = '"+str(qxl_ac_tem[0])+"',"
	sql_string=sql_string+"qxl_ac_tem2 = '"+str(qxl_ac_tem[1])+"',"
	sql_string=sql_string+"qxl_ac_hum1 = '"+str(qxl_ac_hum[0])+"',"
	sql_string=sql_string+"qxl_ac_hum2 = '"+str(qxl_ac_hum[1])+"',"
	sql_string=sql_string+"qxl_ac_open1 = '"+str(qxl_ac_open[0])+"',"
	sql_string=sql_string+"qxl_ac_open2 = '"+str(qxl_ac_open[1])+"',"
	sql_string=sql_string+"qxl_ac_state1 = '"+str(qxl_ac_state[0])+"',"
	sql_string=sql_string+"qxl_ac_state2 = '"+str(qxl_ac_state[1])+"',"
	sql_string=sql_string+"qxl_ac_voice1 = '"+str(qxl_ac_voice[0])+"',"
	sql_string=sql_string+"qxl_ac_voice2 = '"+str(qxl_ac_voice[1])+"',"
	sql_string=sql_string+"qxl_aircondition_des = '"+str(qxl_aircondition_des)+"',"
	sql_string=sql_string+"qxl_leak_45m = '"+str(qxl_leak_45m)+"',"
	sql_string=sql_string+"qxl_leak_45m_spot = '"+str(qxl_leak_45m_spot)+"',"
	sql_string=sql_string+"qxl_leak_15m = '"+str(qxl_leak_15m)+"',"
	sql_string=sql_string+"qxl_leak_15m_spot = '"+str(qxl_leak_15m_spot)+"',"
	sql_string=sql_string+"qxl_door1 = '"+str(qxl_door[0])+"',"
	sql_string=sql_string+"qxl_door2 = '"+str(qxl_door[1])+"',"
	sql_string=sql_string+"qxl_door3 = '"+str(qxl_door[2])+"',"
	sql_string=sql_string+"qxl_door4 = '"+str(qxl_door[3])+"',"
	sql_string=sql_string+"qxl_defend_state = '"+str(qxl_defend_state)+"',"
	sql_string=sql_string+"qxl_environment_des = '"+str(qxl_environment_des)+"',"
	sql_string=sql_string+"qxl_pmm1_uab = '"+str(qxl_pmm1['uab'])+"',"
	sql_string=sql_string+"qxl_pmm1_ubc = '"+str(qxl_pmm1['ubc'])+"',"
	sql_string=sql_string+"qxl_pmm1_uca = '"+str(qxl_pmm1['uca'])+"',"
	sql_string=sql_string+"qxl_pmm1_ia = '"+str(qxl_pmm1['ia'])+"',"
	sql_string=sql_string+"qxl_pmm1_ib = '"+str(qxl_pmm1['ib'])+"',"
	sql_string=sql_string+"qxl_pmm1_ic = '"+str(qxl_pmm1['ic'])+"',"
	sql_string=sql_string+"qxl_pmm1_state = '"+str(qxl_pmm1['state'])+"',"
	sql_string=sql_string+"qxl_pmm2_uab = '"+str(qxl_pmm2['uab'])+"',"
	sql_string=sql_string+"qxl_pmm2_ubc = '"+str(qxl_pmm2['ubc'])+"',"
	sql_string=sql_string+"qxl_pmm2_uca = '"+str(qxl_pmm2['uca'])+"',"
	sql_string=sql_string+"qxl_pmm2_ia = '"+str(qxl_pmm2['ia'])+"',"
	sql_string=sql_string+"qxl_pmm2_ib = '"+str(qxl_pmm2['ib'])+"',"
	sql_string=sql_string+"qxl_pmm2_ic = '"+str(qxl_pmm2['ic'])+"',"
	sql_string=sql_string+"qxl_pmm2_state = '"+str(qxl_pmm2['state'])+"',"
	sql_string=sql_string+"qxl_pmm_des = '"+str(qxl_pmm_des)+"',"
	sql_string=sql_string+"qxl_cabinet1_uab = '"+str(qxl_cabinet_uab[0])+"',"
	sql_string=sql_string+"qxl_cabinet1_ubc = '"+str(qxl_cabinet_ubc[0])+"',"
	sql_string=sql_string+"qxl_cabinet1_uca = '"+str(qxl_cabinet_uca[0])+"',"
	sql_string=sql_string+"qxl_cabinet1_ia = '"+str(qxl_cabinet_ia[0])+"',"
	sql_string=sql_string+"qxl_cabinet1_ib = '"+str(qxl_cabinet_ib[0])+"',"
	sql_string=sql_string+"qxl_cabinet1_ic = '"+str(qxl_cabinet_ic[0])+"',"
	sql_string=sql_string+"qxl_cabinet1_breaker_state = '"+str(qxl_cabinet_breaker_state[0])+"',"
	sql_string=sql_string+"qxl_cabinet2_uab = '"+str(qxl_cabinet_uab[1])+"',"
	sql_string=sql_string+"qxl_cabinet2_ubc = '"+str(qxl_cabinet_ubc[1])+"',"
	sql_string=sql_string+"qxl_cabinet2_uca = '"+str(qxl_cabinet_uca[1])+"',"
	sql_string=sql_string+"qxl_cabinet2_ia = '"+str(qxl_cabinet_ia[1])+"',"
	sql_string=sql_string+"qxl_cabinet2_ib = '"+str(qxl_cabinet_ib[1])+"',"
	sql_string=sql_string+"qxl_cabinet2_ic = '"+str(qxl_cabinet_ic[1])+"',"
	sql_string=sql_string+"qxl_cabinet2_breaker_state = '"+str(qxl_cabinet_breaker_state[1])+"',"
	sql_string=sql_string+"qxl_cabinet3_uab = '"+str(qxl_cabinet_uab[2])+"',"
	sql_string=sql_string+"qxl_cabinet3_ubc = '"+str(qxl_cabinet_ubc[2])+"',"
	sql_string=sql_string+"qxl_cabinet3_uca = '"+str(qxl_cabinet_uca[2])+"',"
	sql_string=sql_string+"qxl_cabinet3_ia = '"+str(qxl_cabinet_ia[2])+"',"
	sql_string=sql_string+"qxl_cabinet3_ib = '"+str(qxl_cabinet_ib[2])+"',"
	sql_string=sql_string+"qxl_cabinet3_ic = '"+str(qxl_cabinet_ic[2])+"',"
	sql_string=sql_string+"qxl_cabinet3_breaker_state = '"+str(qxl_cabinet_breaker_state[2])+"',"
	sql_string=sql_string+"qxl_cabinet4_uab = '"+str(qxl_cabinet_uab[3])+"',"
	sql_string=sql_string+"qxl_cabinet4_ubc = '"+str(qxl_cabinet_ubc[3])+"',"
	sql_string=sql_string+"qxl_cabinet4_uca = '"+str(qxl_cabinet_uca[3])+"',"
	sql_string=sql_string+"qxl_cabinet4_ia = '"+str(qxl_cabinet_ia[3])+"',"
	sql_string=sql_string+"qxl_cabinet4_ib = '"+str(qxl_cabinet_ib[3])+"',"
	sql_string=sql_string+"qxl_cabinet4_ic = '"+str(qxl_cabinet_ic[3])+"',"
	sql_string=sql_string+"qxl_cabinet4_breaker_state = '"+str(qxl_cabinet_breaker_state[3])+"',"
	sql_string=sql_string+"qxl_cabinet5_uab = '"+str(qxl_cabinet_uab[4])+"',"
	sql_string=sql_string+"qxl_cabinet5_ubc = '"+str(qxl_cabinet_ubc[4])+"',"
	sql_string=sql_string+"qxl_cabinet5_uca = '"+str(qxl_cabinet_uca[4])+"',"
	sql_string=sql_string+"qxl_cabinet5_ia = '"+str(qxl_cabinet_ia[4])+"',"
	sql_string=sql_string+"qxl_cabinet5_ib = '"+str(qxl_cabinet_ib[4])+"',"
	sql_string=sql_string+"qxl_cabinet5_ic = '"+str(qxl_cabinet_ic[4])+"',"
	sql_string=sql_string+"qxl_cabinet5_breaker_state = '"+str(qxl_cabinet_breaker_state[4])+"',"
	sql_string=sql_string+"qxl_cabinet_des = '"+str(qxl_cabinet_des)+"',"
	sql_string=sql_string+"qxl_ups1_inpower_l1 = '"+str(qxl_ups1['inpower_l1'])+"',"
	sql_string=sql_string+"qxl_ups1_inpower_l2 = '"+str(qxl_ups1['inpower_l2'])+"',"
	sql_string=sql_string+"qxl_ups1_inpower_l3 = '"+str(qxl_ups1['inpower_l3'])+"',"
	sql_string=sql_string+"qxl_ups1_expower_l1 = '"+str(qxl_ups1['expower_l1'])+"',"
	sql_string=sql_string+"qxl_ups1_expower_l2 = '"+str(qxl_ups1['expower_l2'])+"',"
	sql_string=sql_string+"qxl_ups1_expower_l3 = '"+str(qxl_ups1['expower_l3'])+"',"
	sql_string=sql_string+"qxl_ups1_ini_l1 = '"+str(qxl_ups1['ini_l1'])+"',"
	sql_string=sql_string+"qxl_ups1_ini_l2 = '"+str(qxl_ups1['ini_l2'])+"',"
	sql_string=sql_string+"qxl_ups1_ini_l3 = '"+str(qxl_ups1['ini_l3'])+"',"
	sql_string=sql_string+"qxl_ups1_exi_l1 = '"+str(qxl_ups1['exi_l1'])+"',"
	sql_string=sql_string+"qxl_ups1_exi_l2 = '"+str(qxl_ups1['exi_l2'])+"',"
	sql_string=sql_string+"qxl_ups1_exi_l3 = '"+str(qxl_ups1['exi_l3'])+"',"
	sql_string=sql_string+"qxl_ups1_inu_l12 = '"+str(qxl_ups1['inu_l12'])+"',"
	sql_string=sql_string+"qxl_ups1_inu_l23 = '"+str(qxl_ups1['inu_l23'])+"',"
	sql_string=sql_string+"qxl_ups1_inu_l31 = '"+str(qxl_ups1['inu_l31'])+"',"
	sql_string=sql_string+"qxl_ups1_exu_l12 = '"+str(qxl_ups1['exu_l12'])+"',"
	sql_string=sql_string+"qxl_ups1_exu_l23 = '"+str(qxl_ups1['exu_l23'])+"',"
	sql_string=sql_string+"qxl_ups1_exu_l31 = '"+str(qxl_ups1['exu_l31'])+"',"
	sql_string=sql_string+"qxl_ups1_battery_state = '"+str(qxl_ups1['battery_state'])+"',"
	sql_string=sql_string+"qxl_ups2_inpower_l1 = '"+str(qxl_ups2['inpower_l1'])+"',"
	sql_string=sql_string+"qxl_ups2_inpower_l2 = '"+str(qxl_ups2['inpower_l2'])+"',"
	sql_string=sql_string+"qxl_ups2_inpower_l3 = '"+str(qxl_ups2['inpower_l3'])+"',"
	sql_string=sql_string+"qxl_ups2_expower_l1 = '"+str(qxl_ups2['expower_l1'])+"',"
	sql_string=sql_string+"qxl_ups2_expower_l2 = '"+str(qxl_ups2['expower_l2'])+"',"
	sql_string=sql_string+"qxl_ups2_expower_l3 = '"+str(qxl_ups2['expower_l3'])+"',"
	sql_string=sql_string+"qxl_ups2_ini_l1 = '"+str(qxl_ups2['ini_l1'])+"',"
	sql_string=sql_string+"qxl_ups2_ini_l2 = '"+str(qxl_ups2['ini_l2'])+"',"
	sql_string=sql_string+"qxl_ups2_ini_l3 = '"+str(qxl_ups2['ini_l3'])+"',"
	sql_string=sql_string+"qxl_ups2_exi_l1 = '"+str(qxl_ups2['exi_l1'])+"',"
	sql_string=sql_string+"qxl_ups2_exi_l2 = '"+str(qxl_ups2['exi_l2'])+"',"
	sql_string=sql_string+"qxl_ups2_exi_l3 = '"+str(qxl_ups2['exi_l3'])+"',"
	sql_string=sql_string+"qxl_ups2_inu_l12 = '"+str(qxl_ups2['inu_l12'])+"',"
	sql_string=sql_string+"qxl_ups2_inu_l23 = '"+str(qxl_ups2['inu_l23'])+"',"
	sql_string=sql_string+"qxl_ups2_inu_l31 = '"+str(qxl_ups2['inu_l31'])+"',"
	sql_string=sql_string+"qxl_ups2_exu_l12 = '"+str(qxl_ups2['exu_l12'])+"',"
	sql_string=sql_string+"qxl_ups2_exu_l23 = '"+str(qxl_ups2['exu_l23'])+"',"
	sql_string=sql_string+"qxl_ups2_exu_l31 = '"+str(qxl_ups2['exu_l31'])+"',"
	sql_string=sql_string+"qxl_ups2_battery_state = '"+str(qxl_ups2['battery_state'])+"',"
	sql_string=sql_string+"qxl_ups_des = '"+str(qxl_ups_des)+"'" #根据SQL语句语法，最后一个值的末尾不要加逗号
	
	#将所有气象路机房数据更新进表form_record的条目（已经创建的巡检表），该条目的formname值与cookie的formname的值一致
	ms.ExecNonQuery("UPDATE form_record SET "+sql_string+" WHERE formname = "+"'"+str(formname_value)+"'")

	'''网页回显示测试代码
	print("Content-type:text/html")
	print()
	print('<html xmlns="http://www.w3.org/1999/xhtml">')
	print('<head>')
	print('<meta charset=utf-8" >')
	print('<title>提交确认</title>')
	print('</head>')
	print('<body>')
	print('<div>')
	print('<tr>')

	#打印气象路温湿度上传的值
	for i in range(9):
		print('<td colspan="11"><div>监控点%d的温度是：%s 湿度是：%s</div></td>' % (i+1,qxl_tem[i],qxl_hum[i]))
	print('<td colspan="11"><div>气象路温湿度备注：%s</div></td>' % (qxl_temandhum_des))

	#打印气象路精密空调上传的值
	for i in range(2):
		print('<td colspan="11"><div>空调AC-%d的回风温度：%s 回风湿度：%s 开启状态：%s 空调状态：%s  异常噪音：%s</div></td>' \
			% (i+1,qxl_ac_tem[i],qxl_ac_hum[i],qxl_ac_open[i],qxl_ac_state[i],qxl_ac_voice[i]))
	print('<td colspan="11"><div>气象路精密空调备注：%s</div></td>' % (qxl_aircondition_des))

	#打印气象路环境上传的值
	print('<td><div>气象路45m漏水绳状态：%s</div></td>' % (qxl_leak_45m))
	print('<td colspan="11"><div>气象路45m漏水位置：%s 米</div></td>' % (qxl_leak_45m_spot))
	print('<td><div>气象路15m漏水绳状态：%s</div></td>' % (qxl_leak_15m))
	print('<td colspan="11"><div>气象路15m漏水位置：%s 米</div></td>' % (qxl_leak_15m_spot))
	for i in range(4):
		print('<td><div>气象路门%d状态：%s</div></td>' % (i+1,qxl_door[i]))
	print('<td colspan="11"><div>气象路入侵状态：%s</div></td>' % (qxl_defend_state))
	print('<td colspan="11"><div>气象路环境备注：%s</div></td>' % (qxl_environment_des))


	#打印气象路PMM精密配电柜数据
	print('<td colspan="11"><div>1号精密配电柜 UPS1-P0201-A 线电压 uab：%s ubc：%s uca：%s 电流 ia:%s ib: %s ic：%s 运行状态：%s</div></td>' \
		% (qxl_pmm1['uab'],qxl_pmm1['ubc'],qxl_pmm1['uca'],qxl_pmm1['ia'],qxl_pmm1['ib'],qxl_pmm1['ic'],qxl_pmm1['state']))
	print('<td colspan="11"><div>2号精密配电柜 UPS2-P0201-B 线电压 uab：%s ubc：%s uca：%s 电流 ia:%s ib: %s ic：%s 运行状态：%s</div></td>' \
		% (qxl_pmm2['uab'],qxl_pmm2['ubc'],qxl_pmm2['uca'],qxl_pmm2['ia'],qxl_pmm2['ib'],qxl_pmm2['ic'],qxl_pmm2['state']))
	print('<td colspan="11"><div>气象路精密配电柜备注：%s</div></td>' % (qxl_pmm_des))

	#打印气象路低压电柜上传的值
	for i in range(5):
		print('<td colspan="11"><div>%d号电量仪 线电压Uab：%s Ubc：%s Uca：%s 输入电流Ia:%s Ib: %s Ic：%s 断路器状态：%s</div></td>' % (i+1,qxl_cabinet_uab[i],qxl_cabinet_ubc[i],qxl_cabinet_uca[i],qxl_cabinet_ia[i],qxl_cabinet_ib[i],qxl_cabinet_ic[i],qxl_cabinet_breaker_state[i]))
	print('<td colspan="11"><div>气象路低压电柜备注：%s</div></td>' % qxl_cabinet_des)

	#打印气象路UPS上传的值
	print('<td colspan="11"><div>UPS1 输入有功功率(KW) L1：%s L2：%s L3：%s</div></td>' % (qxl_ups1['inpower_l1'],qxl_ups1['inpower_l2'],qxl_ups1['inpower_l3']))
	print('<td colspan="11"><div>UPS1 输出有功功率(KW) L1：%s L2：%s L3：%s</div></td>' % (qxl_ups1['expower_l1'],qxl_ups1['expower_l2'],qxl_ups1['expower_l3']))
	print('<td colspan="11"><div>UPS1 输入电流 L1：%s L2：%s L3：%s</div></td>' % (qxl_ups1['ini_l1'],qxl_ups1['ini_l2'],qxl_ups1['ini_l3']))
	print('<td colspan="11"><div>UPS1 输出电流 L1：%s L2：%s L3：%s</div></td>' % (qxl_ups1['exi_l1'],qxl_ups1['exi_l2'],qxl_ups1['exi_l3']))
	print('<td colspan="11"><div>UPS1 输入线电压 L1：%s L2：%s L3：%s</div></td>' % (qxl_ups1['inu_l12'],qxl_ups1['inu_l23'],qxl_ups1['inu_l31']))
	print('<td colspan="11"><div>UPS1 输出线电压 L1：%s L2：%s L3：%s</div></td>' % (qxl_ups1['exu_l12'],qxl_ups1['exu_l23'],qxl_ups1['exu_l31']))

	print('<td colspan="11"><div>UPS2 输入有功功率(KW) L1：%s L2：%s L3：%s</div></td>' % (qxl_ups2['inpower_l1'],qxl_ups2['inpower_l2'],qxl_ups2['inpower_l3']))
	print('<td colspan="11"><div>UPS2 输出有功功率(KW) L1：%s L2：%s L3：%s</div></td>' % (qxl_ups2['expower_l1'],qxl_ups2['expower_l2'],qxl_ups2['expower_l3']))
	print('<td colspan="11"><div>UPS2 输入电流 L1：%s L2：%s L3：%s</div></td>' % (qxl_ups2['ini_l1'],qxl_ups2['ini_l2'],qxl_ups2['ini_l3']))
	print('<td colspan="11"><div>UPS2 输出电流 L1：%s L2：%s L3：%s</div></td>' % (qxl_ups2['exi_l1'],qxl_ups2['exi_l2'],qxl_ups2['exi_l3']))
	print('<td colspan="11"><div>UPS2 输入线电压 L1：%s L2：%s L3：%s</div></td>' % (qxl_ups2['inu_l12'],qxl_ups2['inu_l23'],qxl_ups2['inu_l31']))
	print('<td colspan="11"><div>UPS2 输出线电压 L1：%s L2：%s L3：%s</div></td>' % (qxl_ups2['exu_l12'],qxl_ups2['exu_l23'],qxl_ups2['exu_l31']))

	print('<td colspan="11"><div>UPS1 电池状态：%s UPS2 电池状态：%s</div></td>' % (qxl_ups1['battery_state'],qxl_ups2['battery_state']))

	print('<td colspan="11"><div>气象路UPS备注：%s</div></td>' % qxl_ups_des)


	print('</tr>')
	print('</div>')
	print('</body>')
	print('</html>')

	'''
	print("Content-type:text/html;charset=gbk")
	print()
	print('<html xmlns="http://www.w3.org/1999/xhtml">')
	print('<head>')
	print('<meta name="viewport" content="width=device-width, initial-scale=1" />')
	print('<title>提交确认</title>')
	print('</head>')
	print('<body>')
	print('<div align="center">')
	print('<tr>')
	print('<td colspan="11"><div align="center">气象路巡检数据保存成功。</div></td>')
	print('<td colspan="11"><div align="center">1秒后自动跳转。</div></td>')
	print('</tr>')
	#数据提交成功后仍然保持在该页面，并延迟600ms返回
	print('<script language="javascript">')
	print('setTimeout("window.history.go(-1)",600);')
	print('</script>')
	print('</body>')
	print('</html>')