#该模块用于作为新增巡检表保存和修改巡检表保存修改的函数中的ajax验证服务器连通性的目标模块
#解释：如果直接将目标模块设置为实际提交的模块，实际提交的模块将被加载并运行，form.getvalue将获取到传来的空数据，并将空数据写入数据库。

# CGI处理模块
import cgi, cgitb

#响应给前端ajax
print("Content-type: text/html")  #http 头信息必须
print() #这个空格一定要输入