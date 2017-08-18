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

	#获取负1楼温湿度数据
	b1_tem=[]#温度数据
	b1_hum=[]#湿度数据
	for i in range(9):
	  b1_tem.append(form.getvalue('b1_tem2'+str(i+1)))
	  b1_hum.append(form.getvalue('b1_hum2'+str(i+1)))
	b1_temandhum_des=form.getvalue('b1_temandhum_des')#备注数据

	#获取负1楼精密空调数据
	b1_ac_tem=[]#空调温度数据
	b1_ac_hum=[]#空调湿度数据
	b1_ac_open=[]#空调开启状态,开启为0，关闭为1
	b1_ac_state=[]#空调状态，正常为0，异常为1
	b1_ac_voice=[]#异常噪音，无为0，有为1
	for i in range(4):
	  b1_ac_tem.append(form.getvalue('ac_tem'+str(i+14)))
	  b1_ac_hum.append(form.getvalue('ac_hum'+str(i+14)))
	  b1_ac_open.append(form.getvalue('ac_open'+str(i+14)))
	  b1_ac_state.append(form.getvalue('ac_state'+str(i+14)))
	  b1_ac_voice.append(form.getvalue('ac_voice'+str(i+14)))
	b1_aircondition_des=form.getvalue('b1_aircondition_des')#备注数据

	#获取负1楼环境数据
	b1_leak_ac=form.getvalue('b1_leak_ac')#负1楼空调漏水绳状态 正常为0 漏水为1
	b1_leak_ac_spot=form.getvalue('b1_leak_ac_spot')#负1楼空调漏水位置
	b1_leak_well=form.getvalue('b1_leak_well')#负1楼水井漏水 正常为0 漏水为1
	b1_jxc_state=form.getvalue('b1_jxc_state')#负1楼新风机状态 正常为0 异常为1
	b1_jxc_open=form.getvalue('b1_jxc_open')#负1楼新风机打开或关闭 打开为0 关闭为1
	b1_fire_state=form.getvalue('b1_fire_state')#负1楼消防状态 正常为0 异常为1
	b1_smell_state=form.getvalue('b1_smell_state')#负1楼异味状态 正常为0 异常为1
	b1_defend_state=form.getvalue('b1_defend_state')#负1楼入侵状态 正常为0 异常为1
	b1_trace_state=form.getvalue('b1_trace_state')#负1楼痕迹状态 正常为0 异常为1
	b1_left_door=form.getvalue('b1_left_door')#负1楼左边门 正常为0 异常为1
	b1_right_door=form.getvalue('b1_right_door')#负1楼右边门 正常为0 异常为1
	b1_environment_des=form.getvalue('b1_environment_des')#负1楼环境备注

	#获取负1楼UPS数据
	UPSA1={'power_l1':None,'power_l2':None,'power_l3':None,'battery_voltage':None,'FCNC':None,'usage':None,'alert_state':None,'battery_state':None}
	UPSA2={'power_l1':None,'power_l2':None,'power_l3':None,'battery_voltage':None,'FCNC':None,'usage':None,'alert_state':None,'battery_state':None}
	UPSB1={'power_l1':None,'power_l2':None,'power_l3':None,'battery_voltage':None,'FCNC':None,'usage':None,'alert_state':None,'battery_state':None}
	UPSB2={'power_l1':None,'power_l2':None,'power_l3':None,'battery_voltage':None,'FCNC':None,'usage':None,'alert_state':None,'battery_state':None}
	#UPSA1获取数据
	UPSA1['power_l1']=form.getvalue('UPSA1_power_l1')
	UPSA1['power_l2']=form.getvalue('UPSA1_power_l2')
	UPSA1['power_l3']=form.getvalue('UPSA1_power_l3')
	UPSA1['battery_voltage']=form.getvalue('UPSA1_battery_voltage')
	UPSA1['FCNC']=form.getvalue('UPSA1_FCNC')
	UPSA1['usage']=form.getvalue('UPSA1_usage')
	UPSA1['alert_state']=form.getvalue('UPSA1_alert_state')
	UPSA1['battery_state']=form.getvalue('UPSA1_battery_state')
	#UPSA2获取数据
	UPSA2['power_l1']=form.getvalue('UPSA2_power_l1')
	UPSA2['power_l2']=form.getvalue('UPSA2_power_l2')
	UPSA2['power_l3']=form.getvalue('UPSA2_power_l3')
	UPSA2['battery_voltage']=form.getvalue('UPSA2_battery_voltage')
	UPSA2['FCNC']=form.getvalue('UPSA2_FCNC')
	UPSA2['usage']=form.getvalue('UPSA2_usage')
	UPSA2['alert_state']=form.getvalue('UPSA2_alert_state')
	UPSA2['battery_state']=form.getvalue('UPSA2_battery_state')
	#UPSB1获取数据
	UPSB1['power_l1']=form.getvalue('UPSB1_power_l1')
	UPSB1['power_l2']=form.getvalue('UPSB1_power_l2')
	UPSB1['power_l3']=form.getvalue('UPSB1_power_l3')
	UPSB1['battery_voltage']=form.getvalue('UPSB1_battery_voltage')
	UPSB1['FCNC']=form.getvalue('UPSB1_FCNC')
	UPSB1['usage']=form.getvalue('UPSB1_usage')
	UPSB1['alert_state']=form.getvalue('UPSB1_alert_state')
	UPSB1['battery_state']=form.getvalue('UPSB1_battery_state')
	#UPSB2获取数据
	UPSB2['power_l1']=form.getvalue('UPSB2_power_l1')
	UPSB2['power_l2']=form.getvalue('UPSB2_power_l2')
	UPSB2['power_l3']=form.getvalue('UPSB2_power_l3')
	UPSB2['battery_voltage']=form.getvalue('UPSB2_battery_voltage')
	UPSB2['FCNC']=form.getvalue('UPSB2_FCNC')
	UPSB2['usage']=form.getvalue('UPSB2_usage')
	UPSB2['alert_state']=form.getvalue('UPSB2_alert_state')
	UPSB2['battery_state']=form.getvalue('UPSB2_battery_state')
	#获取UPS备注
	b1_UPS_des=form.getvalue('b1_UPS_des')


	#获取低压电柜数据
	cabinet_uab=[]
	cabinet_ubc=[]
	cabinet_uca=[]
	cabinet_ia=[]
	cabinet_ib=[]
	cabinet_ic=[]
	cabinet_breaker_state=[]
	for i in range(9):
		cabinet_uab.append(form.getvalue('cabinet'+str(i+1)+'_uab'))
		cabinet_ubc.append(form.getvalue('cabinet'+str(i+1)+'_ubc'))
		cabinet_uca.append(form.getvalue('cabinet'+str(i+1)+'_uca'))
		cabinet_ia.append(form.getvalue('cabinet'+str(i+1)+'_ia'))
		cabinet_ib.append(form.getvalue('cabinet'+str(i+1)+'_ib'))
		cabinet_ic.append(form.getvalue('cabinet'+str(i+1)+'_ic'))
		cabinet_breaker_state.append(form.getvalue('cabinet'+str(i+1)+'_breaker_state'))
	#获取低压电柜备注
	b1_cabinet_des=form.getvalue('b1_cabinet_des')
	
	#连接SQLServer数据库
	ms=MSSQL.MSSQL(host=MSSQL.database_ipaddr,user=MSSQL.database_login_id,pwd=MSSQL.database_login_password,db="data_center_inspection_system")
	#定义空字符串sql_string
	sql_string=""
	#将所有负1楼机房数据写入字符串sql_string，使得sql_string形如"column1 = 'value1'，column2 = 'value',..."
	sql_string=sql_string+"b1_tem21 = '"+str(b1_tem[0])+"',"
	sql_string=sql_string+"b1_tem22 = '"+str(b1_tem[1])+"',"
	sql_string=sql_string+"b1_tem23 = '"+str(b1_tem[2])+"',"
	sql_string=sql_string+"b1_tem24 = '"+str(b1_tem[3])+"',"
	sql_string=sql_string+"b1_tem25 = '"+str(b1_tem[4])+"',"
	sql_string=sql_string+"b1_tem26 = '"+str(b1_tem[5])+"',"
	sql_string=sql_string+"b1_tem27 = '"+str(b1_tem[6])+"',"
	sql_string=sql_string+"b1_tem28 = '"+str(b1_tem[7])+"',"
	sql_string=sql_string+"b1_tem29 = '"+str(b1_tem[8])+"',"
	sql_string=sql_string+"b1_hum21 = '"+str(b1_hum[0])+"',"
	sql_string=sql_string+"b1_hum22 = '"+str(b1_hum[1])+"',"
	sql_string=sql_string+"b1_hum23 = '"+str(b1_hum[2])+"',"
	sql_string=sql_string+"b1_hum24 = '"+str(b1_hum[3])+"',"
	sql_string=sql_string+"b1_hum25 = '"+str(b1_hum[4])+"',"
	sql_string=sql_string+"b1_hum26 = '"+str(b1_hum[5])+"',"
	sql_string=sql_string+"b1_hum27 = '"+str(b1_hum[6])+"',"
	sql_string=sql_string+"b1_hum28 = '"+str(b1_hum[7])+"',"
	sql_string=sql_string+"b1_hum29 = '"+str(b1_hum[8])+"',"
	sql_string=sql_string+"b1_temandhum_des = '"+str(b1_temandhum_des)+"',"
	sql_string=sql_string+"ac_tem14 = '"+str(b1_ac_tem[0])+"',"
	sql_string=sql_string+"ac_tem15 = '"+str(b1_ac_tem[1])+"',"
	sql_string=sql_string+"ac_tem16 = '"+str(b1_ac_tem[2])+"',"
	sql_string=sql_string+"ac_tem17 = '"+str(b1_ac_tem[3])+"',"
	sql_string=sql_string+"ac_hum14 = '"+str(b1_ac_hum[0])+"',"
	sql_string=sql_string+"ac_hum15 = '"+str(b1_ac_hum[1])+"',"
	sql_string=sql_string+"ac_hum16 = '"+str(b1_ac_hum[2])+"',"
	sql_string=sql_string+"ac_hum17 = '"+str(b1_ac_hum[3])+"',"
	sql_string=sql_string+"ac_open14 = '"+str(b1_ac_open[0])+"',"
	sql_string=sql_string+"ac_open15 = '"+str(b1_ac_open[1])+"',"
	sql_string=sql_string+"ac_open16 = '"+str(b1_ac_open[2])+"',"
	sql_string=sql_string+"ac_open17 = '"+str(b1_ac_open[3])+"',"
	sql_string=sql_string+"ac_state14 = '"+str(b1_ac_state[0])+"',"
	sql_string=sql_string+"ac_state15 = '"+str(b1_ac_state[1])+"',"
	sql_string=sql_string+"ac_state16 = '"+str(b1_ac_state[2])+"',"
	sql_string=sql_string+"ac_state17 = '"+str(b1_ac_state[3])+"',"
	sql_string=sql_string+"ac_voice14 = '"+str(b1_ac_voice[0])+"',"
	sql_string=sql_string+"ac_voice15 = '"+str(b1_ac_voice[1])+"',"
	sql_string=sql_string+"ac_voice16 = '"+str(b1_ac_voice[2])+"',"
	sql_string=sql_string+"ac_voice17 = '"+str(b1_ac_voice[3])+"',"
	sql_string=sql_string+"b1_aircondition_des = '"+str(b1_aircondition_des)+"',"
	sql_string=sql_string+"b1_leak_ac = '"+str(b1_leak_ac)+"',"
	sql_string=sql_string+"b1_leak_ac_spot = '"+str(b1_leak_ac_spot)+"',"
	sql_string=sql_string+"b1_leak_well = '"+str(b1_leak_well)+"',"
	sql_string=sql_string+"b1_jxc_state = '"+str(b1_jxc_state)+"',"
	sql_string=sql_string+"b1_jxc_open = '"+str(b1_jxc_open)+"',"
	sql_string=sql_string+"b1_fire_state = '"+str(b1_fire_state)+"',"
	sql_string=sql_string+"b1_smell_state = '"+str(b1_smell_state)+"',"
	sql_string=sql_string+"b1_defend_state = '"+str(b1_defend_state)+"',"
	sql_string=sql_string+"b1_trace_state = '"+str(b1_trace_state)+"',"
	sql_string=sql_string+"b1_left_door = '"+str(b1_left_door)+"',"
	sql_string=sql_string+"b1_right_door = '"+str(b1_right_door)+"',"
	sql_string=sql_string+"b1_environment_des = '"+str(b1_environment_des)+"',"
	sql_string=sql_string+"UPSA1_power_l1 = '"+str(UPSA1['power_l1'])+"',"
	sql_string=sql_string+"UPSA1_power_l2 = '"+str(UPSA1['power_l2'])+"',"
	sql_string=sql_string+"UPSA1_power_l3 = '"+str(UPSA1['power_l3'])+"',"
	sql_string=sql_string+"UPSA1_battery_voltage = '"+str(UPSA1['battery_voltage'])+"',"
	sql_string=sql_string+"UPSA1_FCNC = '"+str(UPSA1['FCNC'])+"',"
	sql_string=sql_string+"UPSA1_usage = '"+str(UPSA1['usage'])+"',"
	sql_string=sql_string+"UPSA1_alert_state = '"+str(UPSA1['alert_state'])+"',"
	sql_string=sql_string+"UPSA1_battery_state = '"+str(UPSA1['battery_state'])+"',"
	sql_string=sql_string+"UPSA2_power_l1 = '"+str(UPSA2['power_l1'])+"',"
	sql_string=sql_string+"UPSA2_power_l2 = '"+str(UPSA2['power_l2'])+"',"
	sql_string=sql_string+"UPSA2_power_l3 = '"+str(UPSA2['power_l3'])+"',"
	sql_string=sql_string+"UPSA2_battery_voltage = '"+str(UPSA2['battery_voltage'])+"',"
	sql_string=sql_string+"UPSA2_FCNC = '"+str(UPSA2['FCNC'])+"',"
	sql_string=sql_string+"UPSA2_usage = '"+str(UPSA2['usage'])+"',"
	sql_string=sql_string+"UPSA2_alert_state = '"+str(UPSA2['alert_state'])+"',"
	sql_string=sql_string+"UPSA2_battery_state = '"+str(UPSA2['battery_state'])+"',"
	sql_string=sql_string+"UPSB1_power_l1 = '"+str(UPSB1['power_l1'])+"',"
	sql_string=sql_string+"UPSB1_power_l2 = '"+str(UPSB1['power_l2'])+"',"
	sql_string=sql_string+"UPSB1_power_l3 = '"+str(UPSB1['power_l3'])+"',"
	sql_string=sql_string+"UPSB1_battery_voltage = '"+str(UPSB1['battery_voltage'])+"',"
	sql_string=sql_string+"UPSB1_FCNC = '"+str(UPSB1['FCNC'])+"',"
	sql_string=sql_string+"UPSB1_usage = '"+str(UPSB1['usage'])+"',"
	sql_string=sql_string+"UPSB1_alert_state = '"+str(UPSB1['alert_state'])+"',"
	sql_string=sql_string+"UPSB1_battery_state = '"+str(UPSB1['battery_state'])+"',"
	sql_string=sql_string+"UPSB2_power_l1 = '"+str(UPSB2['power_l1'])+"',"
	sql_string=sql_string+"UPSB2_power_l2 = '"+str(UPSB2['power_l2'])+"',"
	sql_string=sql_string+"UPSB2_power_l3 = '"+str(UPSB2['power_l3'])+"',"
	sql_string=sql_string+"UPSB2_battery_voltage = '"+str(UPSB2['battery_voltage'])+"',"
	sql_string=sql_string+"UPSB2_FCNC = '"+str(UPSB2['FCNC'])+"',"
	sql_string=sql_string+"UPSB2_usage = '"+str(UPSB2['usage'])+"',"
	sql_string=sql_string+"UPSB2_alert_state = '"+str(UPSB2['alert_state'])+"',"
	sql_string=sql_string+"UPSB2_battery_state = '"+str(UPSB2['battery_state'])+"',"
	sql_string=sql_string+"b1_UPS_des = '"+str(b1_UPS_des)+"',"
	sql_string=sql_string+"cabinet9_uab = '"+str(cabinet_uab[8])+"',"
	sql_string=sql_string+"cabinet9_ubc = '"+str(cabinet_ubc[8])+"',"
	sql_string=sql_string+"cabinet9_uca = '"+str(cabinet_uca[8])+"',"
	sql_string=sql_string+"cabinet9_ia = '"+str(cabinet_ia[8])+"',"
	sql_string=sql_string+"cabinet9_ib = '"+str(cabinet_ib[8])+"',"
	sql_string=sql_string+"cabinet9_ic = '"+str(cabinet_ic[8])+"',"
	sql_string=sql_string+"cabinet9_breaker_state = '"+str(cabinet_breaker_state[8])+"',"
	sql_string=sql_string+"cabinet4_uab = '"+str(cabinet_uab[3])+"',"
	sql_string=sql_string+"cabinet4_ubc = '"+str(cabinet_ubc[3])+"',"
	sql_string=sql_string+"cabinet4_uca = '"+str(cabinet_uca[3])+"',"
	sql_string=sql_string+"cabinet4_ia = '"+str(cabinet_ia[3])+"',"
	sql_string=sql_string+"cabinet4_ib = '"+str(cabinet_ib[3])+"',"
	sql_string=sql_string+"cabinet4_ic = '"+str(cabinet_ic[3])+"',"
	sql_string=sql_string+"cabinet4_breaker_state = '"+str(cabinet_breaker_state[3])+"',"
	sql_string=sql_string+"cabinet7_uab = '"+str(cabinet_uab[6])+"',"
	sql_string=sql_string+"cabinet7_ubc = '"+str(cabinet_ubc[6])+"',"
	sql_string=sql_string+"cabinet7_uca = '"+str(cabinet_uca[6])+"',"
	sql_string=sql_string+"cabinet7_ia = '"+str(cabinet_ia[6])+"',"
	sql_string=sql_string+"cabinet7_ib = '"+str(cabinet_ib[6])+"',"
	sql_string=sql_string+"cabinet7_ic = '"+str(cabinet_ic[6])+"',"
	sql_string=sql_string+"cabinet7_breaker_state = '"+str(cabinet_breaker_state[6])+"',"
	sql_string=sql_string+"cabinet8_uab = '"+str(cabinet_uab[7])+"',"
	sql_string=sql_string+"cabinet8_ubc = '"+str(cabinet_ubc[7])+"',"
	sql_string=sql_string+"cabinet8_uca = '"+str(cabinet_uca[7])+"',"
	sql_string=sql_string+"cabinet8_ia = '"+str(cabinet_ia[7])+"',"
	sql_string=sql_string+"cabinet8_ib = '"+str(cabinet_ib[7])+"',"
	sql_string=sql_string+"cabinet8_ic = '"+str(cabinet_ic[7])+"',"
	sql_string=sql_string+"cabinet8_breaker_state = '"+str(cabinet_breaker_state[7])+"',"
	sql_string=sql_string+"cabinet3_uab = '"+str(cabinet_uab[2])+"',"
	sql_string=sql_string+"cabinet3_ubc = '"+str(cabinet_ubc[2])+"',"
	sql_string=sql_string+"cabinet3_uca = '"+str(cabinet_uca[2])+"',"
	sql_string=sql_string+"cabinet3_ia = '"+str(cabinet_ia[2])+"',"
	sql_string=sql_string+"cabinet3_ib = '"+str(cabinet_ib[2])+"',"
	sql_string=sql_string+"cabinet3_ic = '"+str(cabinet_ic[2])+"',"
	sql_string=sql_string+"cabinet3_breaker_state = '"+str(cabinet_breaker_state[2])+"',"
	sql_string=sql_string+"cabinet6_uab = '"+str(cabinet_uab[5])+"',"
	sql_string=sql_string+"cabinet6_ubc = '"+str(cabinet_ubc[5])+"',"
	sql_string=sql_string+"cabinet6_uca = '"+str(cabinet_uca[5])+"',"
	sql_string=sql_string+"cabinet6_ia = '"+str(cabinet_ia[5])+"',"
	sql_string=sql_string+"cabinet6_ib = '"+str(cabinet_ib[5])+"',"
	sql_string=sql_string+"cabinet6_ic = '"+str(cabinet_ic[5])+"',"
	sql_string=sql_string+"cabinet6_breaker_state = '"+str(cabinet_breaker_state[5])+"',"
	sql_string=sql_string+"cabinet5_uab = '"+str(cabinet_uab[4])+"',"
	sql_string=sql_string+"cabinet5_ubc = '"+str(cabinet_ubc[4])+"',"
	sql_string=sql_string+"cabinet5_uca = '"+str(cabinet_uca[4])+"',"
	sql_string=sql_string+"cabinet5_ia = '"+str(cabinet_ia[4])+"',"
	sql_string=sql_string+"cabinet5_ib = '"+str(cabinet_ib[4])+"',"
	sql_string=sql_string+"cabinet5_ic = '"+str(cabinet_ic[4])+"',"
	sql_string=sql_string+"cabinet5_breaker_state = '"+str(cabinet_breaker_state[4])+"',"
	sql_string=sql_string+"cabinet2_uab = '"+str(cabinet_uab[1])+"',"
	sql_string=sql_string+"cabinet2_ubc = '"+str(cabinet_ubc[1])+"',"
	sql_string=sql_string+"cabinet2_uca = '"+str(cabinet_uca[1])+"',"
	sql_string=sql_string+"cabinet2_ia = '"+str(cabinet_ia[1])+"',"
	sql_string=sql_string+"cabinet2_ib = '"+str(cabinet_ib[1])+"',"
	sql_string=sql_string+"cabinet2_ic = '"+str(cabinet_ic[1])+"',"
	sql_string=sql_string+"cabinet2_breaker_state = '"+str(cabinet_breaker_state[1])+"',"
	sql_string=sql_string+"cabinet1_uab = '"+str(cabinet_uab[0])+"',"
	sql_string=sql_string+"cabinet1_ubc = '"+str(cabinet_ubc[0])+"',"
	sql_string=sql_string+"cabinet1_uca = '"+str(cabinet_uca[0])+"',"
	sql_string=sql_string+"cabinet1_ia = '"+str(cabinet_ia[0])+"',"
	sql_string=sql_string+"cabinet1_ib = '"+str(cabinet_ib[0])+"',"
	sql_string=sql_string+"cabinet1_ic = '"+str(cabinet_ic[0])+"',"
	sql_string=sql_string+"cabinet1_breaker_state = '"+str(cabinet_breaker_state[0])+"',"
	sql_string=sql_string+"b1_cabinet_des = '"+str(b1_cabinet_des)+"'"#根据SQL语句语法，最后一个值的末尾不要加逗号
	
	#将所有负1楼机房数据更新进表form_record的条目（已经创建的巡检表），该条目的formname值与cookie的formname的值一致
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

	#打印负1楼温湿度上传的值
	for i in range(9):
		print('<td colspan="11"><div>负1楼监控点2%d的温度是：%s 湿度是：%s</div></td>' % (i+1,b1_tem[i],b1_hum[i]))
	print('<td colspan="11"><div>负1楼温湿度备注：%s</div></td>' % (b1_temandhum_des))

	#打印负1楼精密空调上传的值
	for i in range(4):
		print('<td colspan="11"><div>空调AC-%d的回风温度：%s 回风湿度：%s 开启状态：%s 空调状态：%s  异常噪音：%s</div></td>' % (i+14,b1_ac_tem[i],b1_ac_hum[i],b1_ac_open[i],b1_ac_state[i],b1_ac_voice[i]))
	print('<td colspan="11"><div>负1楼精密空调备注：%s</div></td>' % (b1_aircondition_des))

	#打印负1楼环境上传的值
	print('<td><div>负1楼空调漏水绳状态：%s</div></td>' % (b1_leak_ac))
	print('<td colspan="11"><div>负1楼空调漏水位置：%s 米</div></td>' % (b1_leak_ac_spot))
	print('<td colspan="11"><div>负1楼水井状态：%s</div></td>' % (b1_leak_well))
	print('<td colspan="11"><div>负1楼新风机状态：%s</div></td>' % (b1_jxc_state))
	print('<td colspan="11"><div>负1楼新风机打开或关闭：%s</div></td>' % (b1_jxc_open))
	print('<td colspan="11"><div>负1楼消防状态：%s</div></td>' % (b1_fire_state))
	print('<td colspan="11"><div>负1楼异味状态：%s</div></td>' % (b1_smell_state))
	print('<td colspan="11"><div>负1楼入侵状态：%s</div></td>' % (b1_defend_state))
	print('<td colspan="11"><div>负1楼痕迹状态：%s</div></td>' % (b1_trace_state))
	print('<td colspan="11"><div>负1楼左边门：%s</div></td>' % (b1_left_door))
	print('<td colspan="11"><div>负1楼右边门：%s</div></td>' % (b1_right_door))
	print('<td colspan="11"><div>负1楼环境备注：%s</div></td>' % (b1_environment_des))

	#打印负1楼机房不间断电源上传的值
	print('<td colspan="11"><div>UPSA1 有功功率L1：%s L2：%s L3：%s 电池组电压:%s 中性线电流: %s 用量：%s 报警状态：%s 蓄电池状态：%s</div></td>' % (UPSA1['power_l1'],UPSA1['power_l2'],UPSA1['power_l3'],UPSA1['battery_voltage'],UPSA1['FCNC'],UPSA1['usage'],UPSA1['alert_state'],UPSA1['battery_state']))
	print('<td colspan="11"><div>UPSA2 有功功率L1：%s L2：%s L3：%s 电池组电压:%s 中性线电流: %s 用量：%s 报警状态：%s 蓄电池状态：%s</div></td>' % (UPSA2['power_l1'],UPSA2['power_l2'],UPSA2['power_l3'],UPSA2['battery_voltage'],UPSA2['FCNC'],UPSA2['usage'],UPSA2['alert_state'],UPSA2['battery_state']))
	print('<td colspan="11"><div>UPSB1 有功功率L1：%s L2：%s L3：%s 电池组电压:%s 中性线电流: %s 用量：%s 报警状态：%s 蓄电池状态：%s</div></td>' % (UPSB1['power_l1'],UPSB1['power_l2'],UPSB1['power_l3'],UPSB1['battery_voltage'],UPSB1['FCNC'],UPSB1['usage'],UPSB1['alert_state'],UPSB1['battery_state']))
	print('<td colspan="11"><div>UPSB2 有功功率L1：%s L2：%s L3：%s 电池组电压:%s 中性线电流: %s 用量：%s 报警状态：%s 蓄电池状态：%s</div></td>' % (UPSB2['power_l1'],UPSB2['power_l2'],UPSB2['power_l3'],UPSB2['battery_voltage'],UPSB2['FCNC'],UPSB2['usage'],UPSB2['alert_state'],UPSB2['battery_state']))
	print('<td colspan="11"><div>负1楼不间断电源备注：%s</div></td>' % (b1_UPS_des))

	#打印负1楼机房低压供电系统上传的值
	print('<td colspan="11"><div>B1B1-电柜9 线电压Uab：%s Ubc：%s Uca：%s 输入电流Ia:%s Ib: %s Ic：%s 断路器状态：%s</div></td>' % (cabinet_uab[8],cabinet_ubc[8],cabinet_uca[8],cabinet_ia[8],cabinet_ib[8],cabinet_ic[8],cabinet_breaker_state[8]))
	print('<td colspan="11"><div>B1A1-电柜4 线电压Uab：%s Ubc：%s Uca：%s 输入电流Ia:%s Ib: %s Ic：%s 断路器状态：%s</div></td>' % (cabinet_uab[3],cabinet_ubc[3],cabinet_uca[3],cabinet_ia[3],cabinet_ib[3],cabinet_ic[3],cabinet_breaker_state[3]))
	print('<td colspan="11"><div>B1AP3-电柜7 线电压Uab：%s Ubc：%s Uca：%s 输入电流Ia:%s Ib: %s Ic：%s 断路器状态：%s</div></td>' % (cabinet_uab[6],cabinet_ubc[6],cabinet_uca[6],cabinet_ia[6],cabinet_ib[6],cabinet_ic[6],cabinet_breaker_state[6]))
	print('<td colspan="11"><div>B1AP1-电柜8 线电压Uab：%s Ubc：%s Uca：%s 输入电流Ia:%s Ib: %s Ic：%s 断路器状态：%s</div></td>' % (cabinet_uab[7],cabinet_ubc[7],cabinet_uca[7],cabinet_ia[7],cabinet_ib[7],cabinet_ic[7],cabinet_breaker_state[7]))
	print('<td colspan="11"><div>B1AP5-电柜3 线电压Uab：%s Ubc：%s Uca：%s 输入电流Ia:%s Ib: %s Ic：%s 断路器状态：%s</div></td>' % (cabinet_uab[2],cabinet_ubc[2],cabinet_uca[2],cabinet_ia[2],cabinet_ib[2],cabinet_ic[2],cabinet_breaker_state[2]))
	print('<td colspan="11"><div>1UPSB2-电柜6 线电压Uab：%s Ubc：%s Uca：%s 输入电流Ia:%s Ib: %s Ic：%s 断路器状态：%s</div></td>' % (cabinet_uab[5],cabinet_ubc[5],cabinet_uca[5],cabinet_ia[5],cabinet_ib[5],cabinet_ic[5],cabinet_breaker_state[5]))
	print('<td colspan="11"><div>1UPSB1-电柜5 线电压Uab：%s Ubc：%s Uca：%s 输入电流Ia:%s Ib: %s Ic：%s 断路器状态：%s</div></td>' % (cabinet_uab[4],cabinet_ubc[4],cabinet_uca[4],cabinet_ia[4],cabinet_ib[4],cabinet_ic[4],cabinet_breaker_state[4]))
	print('<td colspan="11"><div>1UPSA2-电柜2 线电压Uab：%s Ubc：%s Uca：%s 输入电流Ia:%s Ib: %s Ic：%s 断路器状态：%s</div></td>' % (cabinet_uab[1],cabinet_ubc[1],cabinet_uca[1],cabinet_ia[1],cabinet_ib[1],cabinet_ic[1],cabinet_breaker_state[1]))
	print('<td colspan="00"><div>1UPSA1-电柜1 线电压Uab：%s Ubc：%s Uca：%s 输入电流Ia:%s Ib: %s Ic：%s 断路器状态：%s</div></td>' % (cabinet_uab[0],cabinet_ubc[0],cabinet_uca[0],cabinet_ia[0],cabinet_ib[0],cabinet_ic[0],cabinet_breaker_state[0]))

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
	print('<td colspan="11"><div align="center">负1楼配电间巡检数据保存成功。</div></td>')
	print('</tr>')
	#数据提交成功后仍然保持在该页面，并延迟600ms返回
	print('<script language="javascript">')
	print('setTimeout("window.history.go(-1)",600);')
	print('</script>')

	print('</body>')
	print('</html>')