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
  sql_string=sql_string+"f2_environment_des = '"+str(f2_environment_des)+"'" #根据SQL语句语法，最后一个值的末尾不要加逗号

  #将所有2楼机房数据更新进表form_record的条目（已经创建的巡检表），该条目的formname值与cookie的formname的值一致
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

  #打印上传的2楼温湿度数据
  for i in range(31):
  	print('<td colspan="11"><div>监控点%d 温度：%s 湿度：%s</div></td>' % (i+1,f2_tem[i],f2_hum[i]))
  print('<td colspan="11"><div>2楼温湿度监控备注信息：%s</div></td>' % f2_temandhum_des)

  #打印上传的2楼空调数据
  for i in range(13):
  	print('<td colspan="11"><div>AC%d的回风温度信息：%s</div></td>' % (i+1,ac_tem[i]))
  	print('<td colspan="11"><div>AC%d的回风湿度信息：%s</div></td>' % (i+1,ac_hum[i]))
  	print('<td colspan="11"><div>AC%d的开启状态信息：%s</div></td>' % (i+1,ac_open[i]))
  	print('<td colspan="11"><div>AC%d的空调状态信息：%s</div></td>' % (i+1,ac_state[i]))
  	print('<td colspan="11"><div>AC%d的异常噪音信息：%s</div></td>' % (i+1,ac_voice[i]))
  print('<td colspan="11"><div>备注信息：%s</div></td>' % f2_aircondition_des)

  #打印上传的2楼PMM精密配电柜数据
  print('<td colspan="11"><div>P1101A的运行状态：%s</div></td>' % Dic11A['state'])
  print('<td colspan="11"><div>P1101A的电压V：%s</div></td>' % Dic11A['voltage'])
  print('<td colspan="11"><div>P1101A的电流Ia：%s</div></td>' % Dic11A['ia'])
  print('<td colspan="11"><div>P1101A的电流Ib：%s</div></td>' % Dic11A['ib'])
  print('<td colspan="11"><div>P1101A的电流Ic：%s</div></td>' % Dic11A['ic'])

  print('<td colspan="11"><div>P1101B的运行状态：%s</div></td>' % Dic11B['state'])
  print('<td colspan="11"><div>P1101B的电压V：%s</div></td>' % Dic11B['voltage'])
  print('<td colspan="11"><div>P1101B的电流Ia：%s</div></td>' % Dic11B['ia'])
  print('<td colspan="11"><div>P1101B的电流Ib：%s</div></td>' % Dic11B['ib'])
  print('<td colspan="11"><div>P1101B的电流Ic：%s</div></td>' % Dic11B['ic'])

  print('<td colspan="11"><div>P1001A的运行状态：%s</div></td>' % Dic10A['state'])
  print('<td colspan="11"><div>P1001A的电压V：%s</div></td>' % Dic10A['voltage'])
  print('<td colspan="11"><div>P1001A的电流Ia：%s</div></td>' % Dic10A['ia'])
  print('<td colspan="11"><div>P1001A的电流Ib：%s</div></td>' % Dic10A['ib'])
  print('<td colspan="11"><div>P1001A的电流Ic：%s</div></td>' % Dic10A['ic'])

  print('<td colspan="11"><div>P1001B的运行状态：%s</div></td>' % Dic10B['state'])
  print('<td colspan="11"><div>P1001B的电压V：%s</div></td>' % Dic10B['voltage'])
  print('<td colspan="11"><div>P1001B的电流Ia：%s</div></td>' % Dic10B['ia'])
  print('<td colspan="11"><div>P1001B的电流Ib：%s</div></td>' % Dic10B['ib'])
  print('<td colspan="11"><div>P1001B的电流Ic：%s</div></td>' % Dic10B['ic'])

  print('<td colspan="11"><div>P0901A的运行状态：%s</div></td>' % Dic09A['state'])
  print('<td colspan="11"><div>P0901A的电压V：%s</div></td>' % Dic09A['voltage'])
  print('<td colspan="11"><div>P0901A的电流Ia：%s</div></td>' % Dic09A['ia'])
  print('<td colspan="11"><div>P0901A的电流Ib：%s</div></td>' % Dic09A['ib'])
  print('<td colspan="11"><div>P0901A的电流Ic：%s</div></td>' % Dic09A['ic'])

  print('<td colspan="11"><div>P0901B的运行状态：%s</div></td>' % Dic09B['state'])
  print('<td colspan="11"><div>P0901B的电压V：%s</div></td>' % Dic09B['voltage'])
  print('<td colspan="11"><div>P0901B的电流Ia：%s</div></td>' % Dic09B['ia'])
  print('<td colspan="11"><div>P0901B的电流Ib：%s</div></td>' % Dic09B['ib'])
  print('<td colspan="11"><div>P0901B的电流Ic：%s</div></td>' % Dic09B['ic'])

  print('<td colspan="11"><div>P0801A的运行状态：%s</div></td>' % Dic08A['state'])
  print('<td colspan="11"><div>P0801A的电压V：%s</div></td>' % Dic08A['voltage'])
  print('<td colspan="11"><div>P0801A的电流Ia：%s</div></td>' % Dic08A['ia'])
  print('<td colspan="11"><div>P0801A的电流Ib：%s</div></td>' % Dic08A['ib'])
  print('<td colspan="11"><div>P0801A的电流Ic：%s</div></td>' % Dic08A['ic'])

  print('<td colspan="11"><div>P0801B的运行状态：%s</div></td>' % Dic08B['state'])
  print('<td colspan="11"><div>P0801B的电压V：%s</div></td>' % Dic08B['voltage'])
  print('<td colspan="11"><div>P0801B的电流Ia：%s</div></td>' % Dic08B['ia'])
  print('<td colspan="11"><div>P0801B的电流Ib：%s</div></td>' % Dic08B['ib'])
  print('<td colspan="11"><div>P0801B的电流Ic：%s</div></td>' % Dic08B['ic'])

  print('<td colspan="11"><div>P0701A的运行状态：%s</div></td>' % Dic07A['state'])
  print('<td colspan="11"><div>P0701A的电压V：%s</div></td>' % Dic07A['voltage'])
  print('<td colspan="11"><div>P0701A的电流Ia：%s</div></td>' % Dic07A['ia'])
  print('<td colspan="11"><div>P0701A的电流Ib：%s</div></td>' % Dic07A['ib'])
  print('<td colspan="11"><div>P0701A的电流Ic：%s</div></td>' % Dic07A['ic'])

  print('<td colspan="11"><div>P0701B的运行状态：%s</div></td>' % Dic07B['state'])
  print('<td colspan="11"><div>P0701B的电压V：%s</div></td>' % Dic07B['voltage'])
  print('<td colspan="11"><div>P0701B的电流Ia：%s</div></td>' % Dic07B['ia'])
  print('<td colspan="11"><div>P0701B的电流Ib：%s</div></td>' % Dic07B['ib'])
  print('<td colspan="11"><div>P0701B的电流Ic：%s</div></td>' % Dic07B['ic'])

  print('<td colspan="11"><div>P0601A的运行状态：%s</div></td>' % Dic06A['state'])
  print('<td colspan="11"><div>P0601A的电压V：%s</div></td>' % Dic06A['voltage'])
  print('<td colspan="11"><div>P0601A的电流Ia：%s</div></td>' % Dic06A['ia'])
  print('<td colspan="11"><div>P0601A的电流Ib：%s</div></td>' % Dic06A['ib'])
  print('<td colspan="11"><div>P0601A的电流Ic：%s</div></td>' % Dic06A['ic'])

  print('<td colspan="11"><div>P0601B的运行状态：%s</div></td>' % Dic06B['state'])
  print('<td colspan="11"><div>P0601B的电压V：%s</div></td>' % Dic06B['voltage'])
  print('<td colspan="11"><div>P0601B的电流Ia：%s</div></td>' % Dic06B['ia'])
  print('<td colspan="11"><div>P0601B的电流Ib：%s</div></td>' % Dic06B['ib'])
  print('<td colspan="11"><div>P0601B的电流Ic：%s</div></td>' % Dic06B['ic'])

  print('<td colspan="11"><div>P0501A的运行状态：%s</div></td>' % Dic05A['state'])
  print('<td colspan="11"><div>P0501A的电压V：%s</div></td>' % Dic05A['voltage'])
  print('<td colspan="11"><div>P0501A的电流Ia：%s</div></td>' % Dic05A['ia'])
  print('<td colspan="11"><div>P0501A的电流Ib：%s</div></td>' % Dic05A['ib'])
  print('<td colspan="11"><div>P0501A的电流Ic：%s</div></td>' % Dic05A['ic'])

  print('<td colspan="11"><div>P0501B的运行状态：%s</div></td>' % Dic05B['state'])
  print('<td colspan="11"><div>P0501B的电压V：%s</div></td>' % Dic05B['voltage'])
  print('<td colspan="11"><div>P0501B的电流Ia：%s</div></td>' % Dic05B['ia'])
  print('<td colspan="11"><div>P0501B的电流Ib：%s</div></td>' % Dic05B['ib'])
  print('<td colspan="11"><div>P0501B的电流Ic：%s</div></td>' % Dic05B['ic'])

  print('<td colspan="11"><div>P0401A的运行状态：%s</div></td>' % Dic04A['state'])
  print('<td colspan="11"><div>P0401A的电压V：%s</div></td>' % Dic04A['voltage'])
  print('<td colspan="11"><div>P0401A的电流Ia：%s</div></td>' % Dic04A['ia'])
  print('<td colspan="11"><div>P0401A的电流Ib：%s</div></td>' % Dic04A['ib'])
  print('<td colspan="11"><div>P0401A的电流Ic：%s</div></td>' % Dic04A['ic'])

  print('<td colspan="11"><div>P0401B的运行状态：%s</div></td>' % Dic04B['state'])
  print('<td colspan="11"><div>P0401B的电压V：%s</div></td>' % Dic04B['voltage'])
  print('<td colspan="11"><div>P0401B的电流Ia：%s</div></td>' % Dic04B['ia'])
  print('<td colspan="11"><div>P0401B的电流Ib：%s</div></td>' % Dic04B['ib'])
  print('<td colspan="11"><div>P0401B的电流Ic：%s</div></td>' % Dic04B['ic'])

  print('<td colspan="11"><div>P0301A的运行状态：%s</div></td>' % Dic03A['state'])
  print('<td colspan="11"><div>P0301A的电压V：%s</div></td>' % Dic03A['voltage'])
  print('<td colspan="11"><div>P0301A的电流Ia：%s</div></td>' % Dic03A['ia'])
  print('<td colspan="11"><div>P0301A的电流Ib：%s</div></td>' % Dic03A['ib'])
  print('<td colspan="11"><div>P0301A的电流Ic：%s</div></td>' % Dic03A['ic'])

  print('<td colspan="11"><div>P0301B的运行状态：%s</div></td>' % Dic03B['state'])
  print('<td colspan="11"><div>P0301B的电压V：%s</div></td>' % Dic03B['voltage'])
  print('<td colspan="11"><div>P0301B的电流Ia：%s</div></td>' % Dic03B['ia'])
  print('<td colspan="11"><div>P0301B的电流Ib：%s</div></td>' % Dic03B['ib'])
  print('<td colspan="11"><div>P0301B的电流Ic：%s</div></td>' % Dic03B['ic'])

  print('<td colspan="11"><div>P0101A的运行状态：%s</div></td>' % Dic01A['state'])
  print('<td colspan="11"><div>P0101A的电压V：%s</div></td>' % Dic01A['voltage'])
  print('<td colspan="11"><div>P0101A的电流Ia：%s</div></td>' % Dic01A['ia'])
  print('<td colspan="11"><div>P0101A的电流Ib：%s</div></td>' % Dic01A['ib'])
  print('<td colspan="11"><div>P0101A的电流Ic：%s</div></td>' % Dic01A['ic'])

  print('<td colspan="11"><div>P0101B的运行状态：%s</div></td>' % Dic01B['state'])
  print('<td colspan="11"><div>P0101B的电压V：%s</div></td>' % Dic01B['voltage'])
  print('<td colspan="11"><div>P0101B的电流Ia：%s</div></td>' % Dic01B['ia'])
  print('<td colspan="11"><div>P0101B的电流Ib：%s</div></td>' % Dic01B['ib'])
  print('<td colspan="11"><div>P0101B的电流Ic：%s</div></td>' % Dic01B['ic'])

  print('<td colspan="11"><div>备注信息：%s</div></td>' % f2_pmm_des)

  #打印上传的2楼环境数据
  print('<td colspan="11"><div>2楼消防主机运行状态：%s</div></td>' % f2_fire_host)
  print('<td colspan="11"><div>2楼消防钢瓶：%s</div></td>' % f2_fire_bottle)
  print('<td colspan="11"><div>2楼温感烟感运行状态：%s</div></td>' % f2_fire_sensor)
  print('<td colspan="11"><div>2楼消防通道：%s</div></td>' % f2_fire_access)
  print('<td colspan="11"><div>2楼消防指示牌：%s</div></td>' % f2_fire_sign)
  print('<td colspan="11"><div>2楼声光报警：%s</div></td>' % f2_fire_alarm)
  print('<td colspan="11"><div>2楼新风机状态：%s</div></td>' % f2_jxc_state)
  print('<td colspan="11"><div>2楼新风机打开或关闭：%s</div></td>' % f2_jxc_open)
  print('<td colspan="11"><div>2楼空调漏水绳状态：%s</div></td>' % f2_leak_ac)
  print('<td colspan="11"><div>2楼空调漏水位置：%s</div></td>' % f2_leak_ac_spot)
  print('<td colspan="11"><div>2楼走廊漏水绳状态：%s</div></td>' % f2_leak_corridor)
  print('<td colspan="11"><div>2楼走廊漏水位置：%s</div></td>' % f2_leak_corridor_spot)
  print('<td colspan="11"><div>2楼大屏幕状态：%s</div></td>' % screen_state)
  print('<td colspan="11"><div>动环状态：%s</div></td>' % observer_state)
  print('<td colspan="11"><div>2楼入侵状态：%s</div></td>' % f2_defend_state)
  print('<td colspan="11"><div>2楼痕迹：%s</div></td>' % f2_trace_state)
  print('<td colspan="11"><div>2楼监控室门状态：%s</div></td>' % monitorroom_door)
  print('<td colspan="11"><div>2楼测试间门状态：%s</div></td>' % testroom_door)
  print('<td colspan="11"><div>2楼机房大门状态：%s</div></td>' % gate_door)
  print('<td colspan="11"><div>2楼钢瓶间门状态：%s</div></td>' % bottleroom_door)
  print('<td colspan="11"><div>2楼楼梯门口门状态：%s</div></td>' % floor_door)
  print('<td colspan="11"><div>2楼玻璃门1状态：%s</div></td>' % glass_door1)
  print('<td colspan="11"><div>2楼玻璃门2状态：%s</div></td>' % glass_door2)
  print('<td colspan="11"><div>2楼玻璃门3状态：%s</div></td>' % glass_door3)
  print('<td colspan="11"><div>2楼玻璃门4状态：%s</div></td>' % glass_door4)
  print('<td colspan="11"><div>机柜门锁门情况：%s</div></td>' % rack_door)
  print('<td colspan="11"><div>2楼机房环境备注：%s</div></td>' % f2_environment_des)

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
  print('<td colspan="11"><div align="center">2楼机房巡检数据保存成功。</div></td>')
  print('</tr>')
  #数据提交成功后仍然保持在该页面，并延迟600ms返回
  print('<script language="javascript">')
  print('setTimeout("window.history.go(-1)",600);')
  print('</script>')

  print('</body>')
  print('</html>')