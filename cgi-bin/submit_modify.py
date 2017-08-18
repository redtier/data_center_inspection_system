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
  # 创建 FieldStorage 的实例化
  form = cgi.FieldStorage() 

  # 获取2楼温湿度数据
  f2_tem=[]#温度数据
  f2_hum=[]#湿度数据
  for i in range(31):
    f2_tem.append(form.getvalue('f2_tem'+str(i+1)))
    f2_hum.append(form.getvalue('f2_hum'+str(i+1)))
  f2_temandhum_des=form.getvalue('f2_temandhum_des')#备注数据

  #获取2楼空调数据
  ac_tem=[]#空调温度数据
  ac_hum=[]#空调湿度数据
  ac_open=[]#空调开启状态,开启为0，关闭为1
  ac_state=[]#空调状态，正常为0，异常为1
  ac_voice=[]#异常噪音，无为0，有为1
  for i in range(13):
    ac_tem.append(form.getvalue('ac_tem'+str(i+1)))
    ac_hum.append(form.getvalue('ac_hum'+str(i+1)))
    ac_open.append(form.getvalue('ac_open'+str(i+1)))
    ac_state.append(form.getvalue('ac_state'+str(i+1)))
    ac_voice.append(form.getvalue('ac_voice'+str(i+1)))
  f2_aircondition_des=form.getvalue('f2_aircondition_des')#备注数据

  #获取2楼PMM精密配电柜数据
  # state正常为0 异常为1
  Dic11A={'state':None,'voltage':None,'ia':None,'ib':None,'ic':None}
  Dic11B={'state':None,'voltage':None,'ia':None,'ib':None,'ic':None}
  Dic10A={'state':None,'voltage':None,'ia':None,'ib':None,'ic':None}
  Dic10B={'state':None,'voltage':None,'ia':None,'ib':None,'ic':None}
  Dic09A={'state':None,'voltage':None,'ia':None,'ib':None,'ic':None}
  Dic09B={'state':None,'voltage':None,'ia':None,'ib':None,'ic':None}
  Dic08A={'state':None,'voltage':None,'ia':None,'ib':None,'ic':None}
  Dic08B={'state':None,'voltage':None,'ia':None,'ib':None,'ic':None}
  Dic07A={'state':None,'voltage':None,'ia':None,'ib':None,'ic':None}
  Dic07B={'state':None,'voltage':None,'ia':None,'ib':None,'ic':None}
  Dic06A={'state':None,'voltage':None,'ia':None,'ib':None,'ic':None}
  Dic06B={'state':None,'voltage':None,'ia':None,'ib':None,'ic':None}
  Dic05A={'state':None,'voltage':None,'ia':None,'ib':None,'ic':None}
  Dic05B={'state':None,'voltage':None,'ia':None,'ib':None,'ic':None}
  Dic04A={'state':None,'voltage':None,'ia':None,'ib':None,'ic':None}
  Dic04B={'state':None,'voltage':None,'ia':None,'ib':None,'ic':None}
  Dic03A={'state':None,'voltage':None,'ia':None,'ib':None,'ic':None}
  Dic03B={'state':None,'voltage':None,'ia':None,'ib':None,'ic':None}
  Dic01A={'state':None,'voltage':None,'ia':None,'ib':None,'ic':None}
  Dic01B={'state':None,'voltage':None,'ia':None,'ib':None,'ic':None}

  #P1101A获取数据
  Dic11A['state']=form.getvalue('P1101A_state')
  Dic11A['voltage']=form.getvalue('P1101A_voltage')
  Dic11A['ia']=form.getvalue('P1101A_ia')
  Dic11A['ib']=form.getvalue('P1101A_ib')
  Dic11A['ic']=form.getvalue('P1101A_ic')
  #P1101B获取数据
  Dic11B['state']=form.getvalue('P1101B_state')
  Dic11B['voltage']=form.getvalue('P1101B_voltage')
  Dic11B['ia']=form.getvalue('P1101B_ia')
  Dic11B['ib']=form.getvalue('P1101B_ib')
  Dic11B['ic']=form.getvalue('P1101B_ic')
  #P1001A获取数据
  Dic10A['state']=form.getvalue('P1001A_state')
  Dic10A['voltage']=form.getvalue('P1001A_voltage')
  Dic10A['ia']=form.getvalue('P1001A_ia')
  Dic10A['ib']=form.getvalue('P1001A_ib')
  Dic10A['ic']=form.getvalue('P1001A_ic')
  #P1001B获取数据
  Dic10B['state']=form.getvalue('P1001B_state')
  Dic10B['voltage']=form.getvalue('P1001B_voltage')
  Dic10B['ia']=form.getvalue('P1001B_ia')
  Dic10B['ib']=form.getvalue('P1001B_ib')
  Dic10B['ic']=form.getvalue('P1001B_ic')
  #P0901A获取数据
  Dic09A['state']=form.getvalue('P0901A_state')
  Dic09A['voltage']=form.getvalue('P0901A_voltage')
  Dic09A['ia']=form.getvalue('P0901A_ia')
  Dic09A['ib']=form.getvalue('P0901A_ib')
  Dic09A['ic']=form.getvalue('P0901A_ic')
  #P0901B获取数据
  Dic09B['state']=form.getvalue('P0901B_state')
  Dic09B['voltage']=form.getvalue('P0901B_voltage')
  Dic09B['ia']=form.getvalue('P0901B_ia')
  Dic09B['ib']=form.getvalue('P0901B_ib')
  Dic09B['ic']=form.getvalue('P0901B_ic')
  #P0801A获取数据
  Dic08A['state']=form.getvalue('P0801A_state')
  Dic08A['voltage']=form.getvalue('P0801A_voltage')
  Dic08A['ia']=form.getvalue('P0801A_ia')
  Dic08A['ib']=form.getvalue('P0801A_ib')
  Dic08A['ic']=form.getvalue('P0801A_ic')
  #P0801B获取数据
  Dic08B['state']=form.getvalue('P0801B_state')
  Dic08B['voltage']=form.getvalue('P0801B_voltage')
  Dic08B['ia']=form.getvalue('P0801B_ia')
  Dic08B['ib']=form.getvalue('P0801B_ib')
  Dic08B['ic']=form.getvalue('P0801B_ic')
  #P0701A获取数据
  Dic07A['state']=form.getvalue('P0701A_state')
  Dic07A['voltage']=form.getvalue('P0701A_voltage')
  Dic07A['ia']=form.getvalue('P0701A_ia')
  Dic07A['ib']=form.getvalue('P0701A_ib')
  Dic07A['ic']=form.getvalue('P0701A_ic')
  #P0701B获取数据
  Dic07B['state']=form.getvalue('P0701B_state')
  Dic07B['voltage']=form.getvalue('P0701B_voltage')
  Dic07B['ia']=form.getvalue('P0701B_ia')
  Dic07B['ib']=form.getvalue('P0701B_ib')
  Dic07B['ic']=form.getvalue('P0701B_ic')
  #P0601A获取数据
  Dic06A['state']=form.getvalue('P0601A_state')
  Dic06A['voltage']=form.getvalue('P0601A_voltage')
  Dic06A['ia']=form.getvalue('P0601A_ia')
  Dic06A['ib']=form.getvalue('P0601A_ib')
  Dic06A['ic']=form.getvalue('P0601A_ic')
  #P0601B获取数据
  Dic06B['state']=form.getvalue('P0601B_state')
  Dic06B['voltage']=form.getvalue('P0601B_voltage')
  Dic06B['ia']=form.getvalue('P0601B_ia')
  Dic06B['ib']=form.getvalue('P0601B_ib')
  Dic06B['ic']=form.getvalue('P0601B_ic')
  #P0501A获取数据
  Dic05A['state']=form.getvalue('P0501A_state')
  Dic05A['voltage']=form.getvalue('P0501A_voltage')
  Dic05A['ia']=form.getvalue('P0501A_ia')
  Dic05A['ib']=form.getvalue('P0501A_ib')
  Dic05A['ic']=form.getvalue('P0501A_ic')
  #P0501B获取数据
  Dic05B['state']=form.getvalue('P0501B_state')
  Dic05B['voltage']=form.getvalue('P0501B_voltage')
  Dic05B['ia']=form.getvalue('P0501B_ia')
  Dic05B['ib']=form.getvalue('P0501B_ib')
  Dic05B['ic']=form.getvalue('P0501B_ic')
  #P0401A获取数据
  Dic04A['state']=form.getvalue('P0401A_state')
  Dic04A['voltage']=form.getvalue('P0401A_voltage')
  Dic04A['ia']=form.getvalue('P0401A_ia')
  Dic04A['ib']=form.getvalue('P0401A_ib')
  Dic04A['ic']=form.getvalue('P0401A_ic')
  #P0401B获取数据
  Dic04B['state']=form.getvalue('P0401B_state')
  Dic04B['voltage']=form.getvalue('P0401B_voltage')
  Dic04B['ia']=form.getvalue('P0401B_ia')
  Dic04B['ib']=form.getvalue('P0401B_ib')
  Dic04B['ic']=form.getvalue('P0401B_ic')
  #P0301A获取数据
  Dic03A['state']=form.getvalue('P0301A_state')
  Dic03A['voltage']=form.getvalue('P0301A_voltage')
  Dic03A['ia']=form.getvalue('P0301A_ia')
  Dic03A['ib']=form.getvalue('P0301A_ib')
  Dic03A['ic']=form.getvalue('P0301A_ic')
  #P0301B获取数据
  Dic03B['state']=form.getvalue('P0301B_state')
  Dic03B['voltage']=form.getvalue('P0301B_voltage')
  Dic03B['ia']=form.getvalue('P0301B_ia')
  Dic03B['ib']=form.getvalue('P0301B_ib')
  Dic03B['ic']=form.getvalue('P0301B_ic')
  #P0101A获取数据
  Dic01A['state']=form.getvalue('P0101A_state')
  Dic01A['voltage']=form.getvalue('P0101A_voltage')
  Dic01A['ia']=form.getvalue('P0101A_ia')
  Dic01A['ib']=form.getvalue('P0101A_ib')
  Dic01A['ic']=form.getvalue('P0101A_ic')
  #P0101B获取数据
  Dic01B['state']=form.getvalue('P0101B_state')
  Dic01B['voltage']=form.getvalue('P0101B_voltage')
  Dic01B['ia']=form.getvalue('P0101B_ia')
  Dic01B['ib']=form.getvalue('P0101B_ib')
  Dic01B['ic']=form.getvalue('P0101B_ic')
  #备注获取数据
  f2_pmm_des=form.getvalue('f2_pmm_des')

  #2楼机房环境数据获取
  f2_fire_host=form.getvalue('f2_fire_host') #2楼消防主机运行状态 正常为0 异常为1
  f2_fire_bottle=form.getvalue('f2_fire_bottle') #2楼消防钢瓶 正压为0 负压为1
  f2_fire_sensor=form.getvalue('f2_fire_sensor') #2楼温感烟感运行状态 正常为0 异常为1
  f2_fire_access=form.getvalue('f2_fire_access') #2楼消防通道 通畅为0 阻塞为1
  f2_fire_sign=form.getvalue('f2_fire_sign') #2楼消防指示牌 清晰为0 模糊为1
  f2_fire_alarm=form.getvalue('f2_fire_alarm') #2楼声光报警 正常未0 异常为1
  f2_jxc_state=form.getvalue('f2_jxc_state') #2楼新风机状态 正常为0 异常为1
  f2_jxc_open=form.getvalue('f2_jxc_open') #2楼新风机打开或关闭 打开为0 关闭为1
  f2_leak_ac=form.getvalue('f2_leak_ac') #2楼空调漏水绳状态 正常为0 异常为1
  f2_leak_ac_spot=form.getvalue('f2_leak_ac_spot') #2楼空调漏水位置
  f2_leak_corridor=form.getvalue('f2_leak_corridor') #2楼走廊漏水绳状态 正常为0 异常为1
  f2_leak_corridor_spot=form.getvalue('f2_leak_corridor_spot') #2楼走廊漏水位置
  screen_state=form.getvalue('screen_state') #2楼大屏幕状态 正常为0 异常为1
  observer_state=form.getvalue('observer_state') #动环状态 正常为0 异常为1
  f2_defend_state=form.getvalue('f2_defend_state') #2楼入侵状态 正常为0 异常为1
  f2_trace_state=form.getvalue('f2_trace_state') #2楼痕迹 正常为0 异常为1
  monitorroom_door=form.getvalue('monitorroom_door') #2楼监控室门状态 正常为0 异常为1
  testroom_door=form.getvalue('testroom_door') #2楼测试间门状态 正常为0 异常为1
  gate_door=form.getvalue('gate_door') #2楼机房大门状态 正常为0 异常为1
  bottleroom_door=form.getvalue('bottleroom_door') #2楼钢瓶间门状态 正常为0 异常为1
  floor_door=form.getvalue('floor_door') #2楼楼梯门口门状态 正常为0 异常为1
  glass_door1=form.getvalue('glass_door1') #2楼玻璃门1 正常为0 异常为1
  glass_door2=form.getvalue('glass_door2') #2楼玻璃门2 正常为0 异常为1
  glass_door3=form.getvalue('glass_door3') #2楼玻璃门3 正常为0 异常为1
  glass_door4=form.getvalue('glass_door4') #2楼玻璃门4 正常为0 异常为1
  rack_door=form.getvalue('rack_door') #机柜门锁门情况 正常为0 异常为1
  f2_environment_des=form.getvalue('f2_environment_des') #2楼环境备注

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
  #将所有2楼机房数据写入字符串sql_string，使得sql_string形如"column1 = 'value1'，column2 = 'value',..."
  sql_string=sql_string+"f2_tem1 = '"+str(f2_tem[0])+"',"
  sql_string=sql_string+"f2_tem2 = '"+str(f2_tem[1])+"',"
  sql_string=sql_string+"f2_tem3 = '"+str(f2_tem[2])+"',"
  sql_string=sql_string+"f2_tem4 = '"+str(f2_tem[3])+"',"
  sql_string=sql_string+"f2_tem5 = '"+str(f2_tem[4])+"',"
  sql_string=sql_string+"f2_tem6 = '"+str(f2_tem[5])+"',"
  sql_string=sql_string+"f2_tem7 = '"+str(f2_tem[6])+"',"
  sql_string=sql_string+"f2_tem8 = '"+str(f2_tem[7])+"',"
  sql_string=sql_string+"f2_tem9 = '"+str(f2_tem[8])+"',"
  sql_string=sql_string+"f2_tem10 = '"+str(f2_tem[9])+"',"
  sql_string=sql_string+"f2_tem11 = '"+str(f2_tem[10])+"',"
  sql_string=sql_string+"f2_tem12 = '"+str(f2_tem[11])+"',"
  sql_string=sql_string+"f2_tem13 = '"+str(f2_tem[12])+"',"
  sql_string=sql_string+"f2_tem14 = '"+str(f2_tem[13])+"',"
  sql_string=sql_string+"f2_tem15 = '"+str(f2_tem[14])+"',"
  sql_string=sql_string+"f2_tem16 = '"+str(f2_tem[15])+"',"
  sql_string=sql_string+"f2_tem17 = '"+str(f2_tem[16])+"',"
  sql_string=sql_string+"f2_tem18 = '"+str(f2_tem[17])+"',"
  sql_string=sql_string+"f2_tem19 = '"+str(f2_tem[18])+"',"
  sql_string=sql_string+"f2_tem20 = '"+str(f2_tem[19])+"',"
  sql_string=sql_string+"f2_tem21 = '"+str(f2_tem[20])+"',"
  sql_string=sql_string+"f2_tem22 = '"+str(f2_tem[21])+"',"
  sql_string=sql_string+"f2_tem23 = '"+str(f2_tem[22])+"',"
  sql_string=sql_string+"f2_tem24 = '"+str(f2_tem[23])+"',"
  sql_string=sql_string+"f2_tem25 = '"+str(f2_tem[24])+"',"
  sql_string=sql_string+"f2_tem26 = '"+str(f2_tem[25])+"',"
  sql_string=sql_string+"f2_tem27 = '"+str(f2_tem[26])+"',"
  sql_string=sql_string+"f2_tem28 = '"+str(f2_tem[27])+"',"
  sql_string=sql_string+"f2_tem29 = '"+str(f2_tem[28])+"',"
  sql_string=sql_string+"f2_tem30 = '"+str(f2_tem[29])+"',"
  sql_string=sql_string+"f2_tem31 = '"+str(f2_tem[30])+"',"
  sql_string=sql_string+"f2_hum1 = '"+str(f2_hum[0])+"',"
  sql_string=sql_string+"f2_hum2 = '"+str(f2_hum[1])+"',"
  sql_string=sql_string+"f2_hum3 = '"+str(f2_hum[2])+"',"
  sql_string=sql_string+"f2_hum4 = '"+str(f2_hum[3])+"',"
  sql_string=sql_string+"f2_hum5 = '"+str(f2_hum[4])+"',"
  sql_string=sql_string+"f2_hum6 = '"+str(f2_hum[5])+"',"
  sql_string=sql_string+"f2_hum7 = '"+str(f2_hum[6])+"',"
  sql_string=sql_string+"f2_hum8 = '"+str(f2_hum[7])+"',"
  sql_string=sql_string+"f2_hum9 = '"+str(f2_hum[8])+"',"
  sql_string=sql_string+"f2_hum10 = '"+str(f2_hum[9])+"',"
  sql_string=sql_string+"f2_hum11 = '"+str(f2_hum[10])+"',"
  sql_string=sql_string+"f2_hum12 = '"+str(f2_hum[11])+"',"
  sql_string=sql_string+"f2_hum13 = '"+str(f2_hum[12])+"',"
  sql_string=sql_string+"f2_hum14 = '"+str(f2_hum[13])+"',"
  sql_string=sql_string+"f2_hum15 = '"+str(f2_hum[14])+"',"
  sql_string=sql_string+"f2_hum16 = '"+str(f2_hum[15])+"',"
  sql_string=sql_string+"f2_hum17 = '"+str(f2_hum[16])+"',"
  sql_string=sql_string+"f2_hum18 = '"+str(f2_hum[17])+"',"
  sql_string=sql_string+"f2_hum19 = '"+str(f2_hum[18])+"',"
  sql_string=sql_string+"f2_hum20 = '"+str(f2_hum[19])+"',"
  sql_string=sql_string+"f2_hum21 = '"+str(f2_hum[20])+"',"
  sql_string=sql_string+"f2_hum22 = '"+str(f2_hum[21])+"',"
  sql_string=sql_string+"f2_hum23 = '"+str(f2_hum[22])+"',"
  sql_string=sql_string+"f2_hum24 = '"+str(f2_hum[23])+"',"
  sql_string=sql_string+"f2_hum25 = '"+str(f2_hum[24])+"',"
  sql_string=sql_string+"f2_hum26 = '"+str(f2_hum[25])+"',"
  sql_string=sql_string+"f2_hum27 = '"+str(f2_hum[26])+"',"
  sql_string=sql_string+"f2_hum28 = '"+str(f2_hum[27])+"',"
  sql_string=sql_string+"f2_hum29 = '"+str(f2_hum[28])+"',"
  sql_string=sql_string+"f2_hum30 = '"+str(f2_hum[29])+"',"
  sql_string=sql_string+"f2_hum31 = '"+str(f2_hum[30])+"',"
  sql_string=sql_string+"f2_temandhum_des = '"+str(f2_temandhum_des)+"',"
  sql_string=sql_string+"ac_tem1 = '"+str(ac_tem[0])+"',"
  sql_string=sql_string+"ac_tem2 = '"+str(ac_tem[1])+"',"
  sql_string=sql_string+"ac_tem3 = '"+str(ac_tem[2])+"',"
  sql_string=sql_string+"ac_tem4 = '"+str(ac_tem[3])+"',"
  sql_string=sql_string+"ac_tem5 = '"+str(ac_tem[4])+"',"
  sql_string=sql_string+"ac_tem6 = '"+str(ac_tem[5])+"',"
  sql_string=sql_string+"ac_tem7 = '"+str(ac_tem[6])+"',"
  sql_string=sql_string+"ac_tem8 = '"+str(ac_tem[7])+"',"
  sql_string=sql_string+"ac_tem9 = '"+str(ac_tem[8])+"',"
  sql_string=sql_string+"ac_tem10 = '"+str(ac_tem[9])+"',"
  sql_string=sql_string+"ac_tem11 = '"+str(ac_tem[10])+"',"
  sql_string=sql_string+"ac_tem12 = '"+str(ac_tem[11])+"',"
  sql_string=sql_string+"ac_tem13 = '"+str(ac_tem[12])+"',"
  sql_string=sql_string+"ac_hum1 = '"+str(ac_hum[0])+"',"
  sql_string=sql_string+"ac_hum2 = '"+str(ac_hum[1])+"',"
  sql_string=sql_string+"ac_hum3 = '"+str(ac_hum[2])+"',"
  sql_string=sql_string+"ac_hum4 = '"+str(ac_hum[3])+"',"
  sql_string=sql_string+"ac_hum5 = '"+str(ac_hum[4])+"',"
  sql_string=sql_string+"ac_hum6 = '"+str(ac_hum[5])+"',"
  sql_string=sql_string+"ac_hum7 = '"+str(ac_hum[6])+"',"
  sql_string=sql_string+"ac_hum8 = '"+str(ac_hum[7])+"',"
  sql_string=sql_string+"ac_hum9 = '"+str(ac_hum[8])+"',"
  sql_string=sql_string+"ac_hum10 = '"+str(ac_hum[9])+"',"
  sql_string=sql_string+"ac_hum11 = '"+str(ac_hum[10])+"',"
  sql_string=sql_string+"ac_hum12 = '"+str(ac_hum[11])+"',"
  sql_string=sql_string+"ac_hum13 = '"+str(ac_hum[12])+"',"
  sql_string=sql_string+"ac_open1 = '"+str(ac_open[0])+"',"
  sql_string=sql_string+"ac_open2 = '"+str(ac_open[1])+"',"
  sql_string=sql_string+"ac_open3 = '"+str(ac_open[2])+"',"
  sql_string=sql_string+"ac_open4 = '"+str(ac_open[3])+"',"
  sql_string=sql_string+"ac_open5 = '"+str(ac_open[4])+"',"
  sql_string=sql_string+"ac_open6 = '"+str(ac_open[5])+"',"
  sql_string=sql_string+"ac_open7 = '"+str(ac_open[6])+"',"
  sql_string=sql_string+"ac_open8 = '"+str(ac_open[7])+"',"
  sql_string=sql_string+"ac_open9 = '"+str(ac_open[8])+"',"
  sql_string=sql_string+"ac_open10 = '"+str(ac_open[9])+"',"
  sql_string=sql_string+"ac_open11 = '"+str(ac_open[10])+"',"
  sql_string=sql_string+"ac_open12 = '"+str(ac_open[11])+"',"
  sql_string=sql_string+"ac_open13 = '"+str(ac_open[12])+"',"
  sql_string=sql_string+"ac_state1 = '"+str(ac_state[0])+"',"
  sql_string=sql_string+"ac_state2 = '"+str(ac_state[1])+"',"
  sql_string=sql_string+"ac_state3 = '"+str(ac_state[2])+"',"
  sql_string=sql_string+"ac_state4 = '"+str(ac_state[3])+"',"
  sql_string=sql_string+"ac_state5 = '"+str(ac_state[4])+"',"
  sql_string=sql_string+"ac_state6 = '"+str(ac_state[5])+"',"
  sql_string=sql_string+"ac_state7 = '"+str(ac_state[6])+"',"
  sql_string=sql_string+"ac_state8 = '"+str(ac_state[7])+"',"
  sql_string=sql_string+"ac_state9 = '"+str(ac_state[8])+"',"
  sql_string=sql_string+"ac_state10 = '"+str(ac_state[9])+"',"
  sql_string=sql_string+"ac_state11 = '"+str(ac_state[10])+"',"
  sql_string=sql_string+"ac_state12 = '"+str(ac_state[11])+"',"
  sql_string=sql_string+"ac_state13 = '"+str(ac_state[12])+"',"
  sql_string=sql_string+"ac_voice1 = '"+str(ac_voice[0])+"',"
  sql_string=sql_string+"ac_voice2 = '"+str(ac_voice[1])+"',"
  sql_string=sql_string+"ac_voice3 = '"+str(ac_voice[2])+"',"
  sql_string=sql_string+"ac_voice4 = '"+str(ac_voice[3])+"',"
  sql_string=sql_string+"ac_voice5 = '"+str(ac_voice[4])+"',"
  sql_string=sql_string+"ac_voice6 = '"+str(ac_voice[5])+"',"
  sql_string=sql_string+"ac_voice7 = '"+str(ac_voice[6])+"',"
  sql_string=sql_string+"ac_voice8 = '"+str(ac_voice[7])+"',"
  sql_string=sql_string+"ac_voice9 = '"+str(ac_voice[8])+"',"
  sql_string=sql_string+"ac_voice10 = '"+str(ac_voice[9])+"',"
  sql_string=sql_string+"ac_voice11 = '"+str(ac_voice[10])+"',"
  sql_string=sql_string+"ac_voice12 = '"+str(ac_voice[11])+"',"
  sql_string=sql_string+"ac_voice13 = '"+str(ac_voice[12])+"',"
  sql_string=sql_string+"f2_aircondition_des = '"+str(f2_aircondition_des)+"',"
  sql_string=sql_string+"P1101A_state = '"+str(Dic11A['state'])+"',"
  sql_string=sql_string+"P1101A_voltage = '"+str(Dic11A['voltage'])+"',"
  sql_string=sql_string+"P1101A_ia = '"+str(Dic11A['ia'])+"',"
  sql_string=sql_string+"P1101A_ib = '"+str(Dic11A['ib'])+"',"
  sql_string=sql_string+"P1101A_ic = '"+str(Dic11A['ic'])+"',"
  sql_string=sql_string+"P1101B_state = '"+str(Dic11B['state'])+"',"
  sql_string=sql_string+"P1101B_voltage = '"+str(Dic11B['voltage'])+"',"
  sql_string=sql_string+"P1101B_ia = '"+str(Dic11B['ia'])+"',"
  sql_string=sql_string+"P1101B_ib = '"+str(Dic11B['ib'])+"',"
  sql_string=sql_string+"P1101B_ic = '"+str(Dic11B['ic'])+"',"
  sql_string=sql_string+"P1001A_state = '"+str(Dic10A['state'])+"',"
  sql_string=sql_string+"P1001A_voltage = '"+str(Dic10A['voltage'])+"',"
  sql_string=sql_string+"P1001A_ia = '"+str(Dic10A['ia'])+"',"
  sql_string=sql_string+"P1001A_ib = '"+str(Dic10A['ib'])+"',"
  sql_string=sql_string+"P1001A_ic = '"+str(Dic10A['ic'])+"',"
  sql_string=sql_string+"P1001B_state = '"+str(Dic10B['state'])+"',"
  sql_string=sql_string+"P1001B_voltage = '"+str(Dic10B['voltage'])+"',"
  sql_string=sql_string+"P1001B_ia = '"+str(Dic10B['ia'])+"',"
  sql_string=sql_string+"P1001B_ib = '"+str(Dic10B['ib'])+"',"
  sql_string=sql_string+"P1001B_ic = '"+str(Dic10B['ic'])+"',"
  sql_string=sql_string+"P0901A_state = '"+str(Dic09A['state'])+"',"
  sql_string=sql_string+"P0901A_voltage = '"+str(Dic09A['voltage'])+"',"
  sql_string=sql_string+"P0901A_ia = '"+str(Dic09A['ia'])+"',"
  sql_string=sql_string+"P0901A_ib = '"+str(Dic09A['ib'])+"',"
  sql_string=sql_string+"P0901A_ic = '"+str(Dic09A['ic'])+"',"
  sql_string=sql_string+"P0901B_state = '"+str(Dic09B['state'])+"',"
  sql_string=sql_string+"P0901B_voltage = '"+str(Dic09B['voltage'])+"',"
  sql_string=sql_string+"P0901B_ia = '"+str(Dic09B['ia'])+"',"
  sql_string=sql_string+"P0901B_ib = '"+str(Dic09B['ib'])+"',"
  sql_string=sql_string+"P0901B_ic = '"+str(Dic09B['ic'])+"',"
  sql_string=sql_string+"P0801A_state = '"+str(Dic08A['state'])+"',"
  sql_string=sql_string+"P0801A_voltage = '"+str(Dic08A['voltage'])+"',"
  sql_string=sql_string+"P0801A_ia = '"+str(Dic08A['ia'])+"',"
  sql_string=sql_string+"P0801A_ib = '"+str(Dic08A['ib'])+"',"
  sql_string=sql_string+"P0801A_ic = '"+str(Dic08A['ic'])+"',"
  sql_string=sql_string+"P0801B_state = '"+str(Dic08B['state'])+"',"
  sql_string=sql_string+"P0801B_voltage = '"+str(Dic08B['voltage'])+"',"
  sql_string=sql_string+"P0801B_ia = '"+str(Dic08B['ia'])+"',"
  sql_string=sql_string+"P0801B_ib = '"+str(Dic08B['ib'])+"',"
  sql_string=sql_string+"P0801B_ic = '"+str(Dic08B['ic'])+"',"
  sql_string=sql_string+"P0701A_state = '"+str(Dic07A['state'])+"',"
  sql_string=sql_string+"P0701A_voltage = '"+str(Dic07A['voltage'])+"',"
  sql_string=sql_string+"P0701A_ia = '"+str(Dic07A['ia'])+"',"
  sql_string=sql_string+"P0701A_ib = '"+str(Dic07A['ib'])+"',"
  sql_string=sql_string+"P0701A_ic = '"+str(Dic07A['ic'])+"',"
  sql_string=sql_string+"P0701B_state = '"+str(Dic07B['state'])+"',"
  sql_string=sql_string+"P0701B_voltage = '"+str(Dic07B['voltage'])+"',"
  sql_string=sql_string+"P0701B_ia = '"+str(Dic07B['ia'])+"',"
  sql_string=sql_string+"P0701B_ib = '"+str(Dic07B['ib'])+"',"
  sql_string=sql_string+"P0701B_ic = '"+str(Dic07B['ic'])+"',"
  sql_string=sql_string+"P0601A_state = '"+str(Dic06A['state'])+"',"
  sql_string=sql_string+"P0601A_voltage = '"+str(Dic06A['voltage'])+"',"
  sql_string=sql_string+"P0601A_ia = '"+str(Dic06A['ia'])+"',"
  sql_string=sql_string+"P0601A_ib = '"+str(Dic06A['ib'])+"',"
  sql_string=sql_string+"P0601A_ic = '"+str(Dic06A['ic'])+"',"
  sql_string=sql_string+"P0601B_state = '"+str(Dic06B['state'])+"',"
  sql_string=sql_string+"P0601B_voltage = '"+str(Dic06B['voltage'])+"',"
  sql_string=sql_string+"P0601B_ia = '"+str(Dic06B['ia'])+"',"
  sql_string=sql_string+"P0601B_ib = '"+str(Dic06B['ib'])+"',"
  sql_string=sql_string+"P0601B_ic = '"+str(Dic06B['ic'])+"',"
  sql_string=sql_string+"P0501A_state = '"+str(Dic05A['state'])+"',"
  sql_string=sql_string+"P0501A_voltage = '"+str(Dic05A['voltage'])+"',"
  sql_string=sql_string+"P0501A_ia = '"+str(Dic05A['ia'])+"',"
  sql_string=sql_string+"P0501A_ib = '"+str(Dic05A['ib'])+"',"
  sql_string=sql_string+"P0501A_ic = '"+str(Dic05A['ic'])+"',"
  sql_string=sql_string+"P0501B_state = '"+str(Dic05B['state'])+"',"
  sql_string=sql_string+"P0501B_voltage = '"+str(Dic05B['voltage'])+"',"
  sql_string=sql_string+"P0501B_ia = '"+str(Dic05B['ia'])+"',"
  sql_string=sql_string+"P0501B_ib = '"+str(Dic05B['ib'])+"',"
  sql_string=sql_string+"P0501B_ic = '"+str(Dic05B['ic'])+"',"
  sql_string=sql_string+"P0401A_state = '"+str(Dic04A['state'])+"',"
  sql_string=sql_string+"P0401A_voltage = '"+str(Dic04A['voltage'])+"',"
  sql_string=sql_string+"P0401A_ia = '"+str(Dic04A['ia'])+"',"
  sql_string=sql_string+"P0401A_ib = '"+str(Dic04A['ib'])+"',"
  sql_string=sql_string+"P0401A_ic = '"+str(Dic04A['ic'])+"',"
  sql_string=sql_string+"P0401B_state = '"+str(Dic04B['state'])+"',"
  sql_string=sql_string+"P0401B_voltage = '"+str(Dic04B['voltage'])+"',"
  sql_string=sql_string+"P0401B_ia = '"+str(Dic04B['ia'])+"',"
  sql_string=sql_string+"P0401B_ib = '"+str(Dic04B['ib'])+"',"
  sql_string=sql_string+"P0401B_ic = '"+str(Dic04B['ic'])+"',"
  sql_string=sql_string+"P0301A_state = '"+str(Dic03A['state'])+"',"
  sql_string=sql_string+"P0301A_voltage = '"+str(Dic03A['voltage'])+"',"
  sql_string=sql_string+"P0301A_ia = '"+str(Dic03A['ia'])+"',"
  sql_string=sql_string+"P0301A_ib = '"+str(Dic03A['ib'])+"',"
  sql_string=sql_string+"P0301A_ic = '"+str(Dic03A['ic'])+"',"
  sql_string=sql_string+"P0301B_state = '"+str(Dic03B['state'])+"',"
  sql_string=sql_string+"P0301B_voltage = '"+str(Dic03B['voltage'])+"',"
  sql_string=sql_string+"P0301B_ia = '"+str(Dic03B['ia'])+"',"
  sql_string=sql_string+"P0301B_ib = '"+str(Dic03B['ib'])+"',"
  sql_string=sql_string+"P0301B_ic = '"+str(Dic03B['ic'])+"',"
  sql_string=sql_string+"P0101A_state = '"+str(Dic01A['state'])+"',"
  sql_string=sql_string+"P0101A_voltage = '"+str(Dic01A['voltage'])+"',"
  sql_string=sql_string+"P0101A_ia = '"+str(Dic01A['ia'])+"',"
  sql_string=sql_string+"P0101A_ib = '"+str(Dic01A['ib'])+"',"
  sql_string=sql_string+"P0101A_ic = '"+str(Dic01A['ic'])+"',"
  sql_string=sql_string+"P0101B_state = '"+str(Dic01B['state'])+"',"
  sql_string=sql_string+"P0101B_voltage = '"+str(Dic01B['voltage'])+"',"
  sql_string=sql_string+"P0101B_ia = '"+str(Dic01B['ia'])+"',"
  sql_string=sql_string+"P0101B_ib = '"+str(Dic01B['ib'])+"',"
  sql_string=sql_string+"P0101B_ic = '"+str(Dic01B['ic'])+"',"
  sql_string=sql_string+"f2_pmm_des = '"+str(f2_pmm_des)+"',"
  sql_string=sql_string+"f2_fire_host = '"+str(f2_fire_host)+"',"
  sql_string=sql_string+"f2_fire_bottle = '"+str(f2_fire_bottle)+"',"
  sql_string=sql_string+"f2_fire_sensor = '"+str(f2_fire_sensor)+"',"
  sql_string=sql_string+"f2_fire_access = '"+str(f2_fire_access)+"',"
  sql_string=sql_string+"f2_fire_sign = '"+str(f2_fire_sign)+"',"
  sql_string=sql_string+"f2_fire_alarm = '"+str(f2_fire_alarm)+"',"
  sql_string=sql_string+"f2_jxc_state = '"+str(f2_jxc_state)+"',"
  sql_string=sql_string+"f2_jxc_open = '"+str(f2_jxc_open)+"',"
  sql_string=sql_string+"f2_leak_ac = '"+str(f2_leak_ac)+"',"
  sql_string=sql_string+"f2_leak_ac_spot = '"+str(f2_leak_ac_spot)+"',"
  sql_string=sql_string+"f2_leak_corridor = '"+str(f2_leak_corridor)+"',"
  sql_string=sql_string+"f2_leak_corridor_spot = '"+str(f2_leak_corridor_spot)+"',"
  sql_string=sql_string+"screen_state = '"+str(screen_state)+"',"
  sql_string=sql_string+"observer_state = '"+str(observer_state)+"',"
  sql_string=sql_string+"f2_defend_state = '"+str(f2_defend_state)+"',"
  sql_string=sql_string+"f2_trace_state = '"+str(f2_trace_state)+"',"
  sql_string=sql_string+"monitorroom_door = '"+str(monitorroom_door)+"',"
  sql_string=sql_string+"testroom_door = '"+str(testroom_door)+"',"
  sql_string=sql_string+"gate_door = '"+str(gate_door)+"',"
  sql_string=sql_string+"bottleroom_door = '"+str(bottleroom_door)+"',"
  sql_string=sql_string+"floor_door = '"+str(floor_door)+"',"
  sql_string=sql_string+"glass_door1 = '"+str(glass_door1)+"',"
  sql_string=sql_string+"glass_door2 = '"+str(glass_door2)+"',"
  sql_string=sql_string+"glass_door3 = '"+str(glass_door3)+"',"
  sql_string=sql_string+"glass_door4 = '"+str(glass_door4)+"',"
  sql_string=sql_string+"rack_door = '"+str(rack_door)+"',"
  sql_string=sql_string+"f2_environment_des = '"+str(f2_environment_des)+"',"

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
  sql_string=sql_string+"b1_cabinet_des = '"+str(b1_cabinet_des)+"',"

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

  #将所有机房数据更新进表form_record的条目（已经创建的巡检表），该条目的formname值与cookie的formname的值一致
  ms.ExecNonQuery("UPDATE form_record SET "+sql_string+" WHERE formname = "+"'"+str(formname_value)+"'")

  print("Content-type:text/html;charset=gbk")
  print()
  print('<html xmlns="http://www.w3.org/1999/xhtml">')
  print('<head>')
  #此处应跳转到查询页面，检查之前的录入,功能：查询、修改、提交审核、审核通过
  print('<meta http-equiv="refresh" content="1;url=../form_query_export.html";charset=utf-8" >')
  print('<meta name="viewport" content="width=device-width, initial-scale=1" />')
  print('<title>提交确认</title>')
  print('</head>')
  print('<body>')
  print('<div align="center">')
  print('<tr>')
  print('<td colspan="11"><div align="center">巡检表'+formname_value+'保存修改完成，请确认巡检表无误后提交审核。</div></td>')
  print('<td colspan="11"><div align="center">1秒后自动跳转。</div></td>')
  print('</tr>')
  print('</body>')
  print('</html>')