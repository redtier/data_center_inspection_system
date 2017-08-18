// JS对SQL SERVER数据库进行操作

var conn;
var rs;

/*获取数据库连接*/
function getConnection() {
    conn = new ActiveXObject("ADODB.Connection");
    // 1.JavaScript操作数据库JS操作Access数据库
    // 在F盘有文件abc.mdf，表名为user，一共2个字段，id数字类型主键，name文本类型
    // conn.Open("DBQ=f://abc.mdb;DRIVER={Microsoft Access Driver (*.mdb)};");

    // 2.JavaScript操作数据库JS操作SQL Server数据库
    // 数据库名为：test，表名为user，id为int类型，自增列，name为用户名，为varchar类型；数据库用户名为sa，密码是sasa。
    conn.Open("Driver={SQL Server};Server=192.168.18.185;DataBase=data_center_inspection_system;UID=sa;PWD=111");       //打开数据库
    return conn;
}

/*执行增删改的方法*/
function executeUpdate(sql) {
    getConnection();
    try {
        conn.execute(sql);
        return true;
    } catch (e) {
        alert(e.description);
    } finally {
        closeAll();
    }
    return false;
}

/*执行查询的方法*/
function executeQuery(sql) {
    getConnection();
    try {
        rs = new ActiveXObject("ADODB.Recordset");
        rs.open(sql, conn);
        var html = "";
        while(!rs.EOF) {
            html = html + rs.Fields("username") + "    " + rs.Fields("truthname")+"<br/>";
            rs.moveNext();
        }
        return html;
    } catch (e) {
        alert(e.description);
    } finally {
        closeAll();
    }
}

/*关闭所有资源*/
function closeAll() {
    if(rs != null) {
        rs.close();
        rs = null;
    }
    if(conn != null) {
        conn.close();
        conn = null;
    }
}

// 增
// executeUpdate("INSERT INTO [user](create_date, edit_date, is_delete, [name], sex, age) VALUES ('2013-10-17 12:00:00', '2013-10-17 12:00:00', 0, '空', '男', 20)");
// 删
// executeUpdate("DELETE FROM [user] WHERE id = 1009");
// 改
// executeUpdate("UPDATE [user] SET sex = '女', age = 18 WHERE id = 1009");
// 查
//executeQuery("select * from [user]"); 