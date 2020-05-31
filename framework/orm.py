import pymysql.cursors

# 连接数据库
# connection = pymysql.connect(host='localhost',user='root',password='root',db='chatroom',cursorclass=pymysql.cursors.DictCursor)



class DB():

    def __init__(self,host,user,password,db):
        self.connection = pymysql.connect(host=host,
                 user=user,
                 password=password,
                 db=db,
                 cursorclass=pymysql.cursors.DictCursor)

    def query(self, tableName, args=None, pageNo=None, pageSize=None):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            sql = "SELECT * FROM " + tableName
            if args != None:
                sql += " WHERE "
                for key in args:
                    value = args[key]
                    if(type(value)==str):
                        sql += key + "="+'"' + value+'"' + " "
                    else:
                        sql += key + "=" + str(value) + " "
                # {pageNo:1,pagesize:10}
            if pageNo != None:
                sql += " limit " + str((pageNo - 1) * pageSize) + ", " + str(pageSize)
            print(sql)
            cursor.execute(sql)
            result = cursor.fetchall()
            self.connection.close()
        return result

    def updata(self, tableName, args,where):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            sql = "UPDATE "+tableName+ " SET "
            for key in args:
                value = args[key]
                if (type(value) == str):
                    sql += key + "=" + '"' + value + '"' + " "
                else:
                    sql += key + "=" + str(value) + " "
            sql +=" WHERE "
            for key in where:
                value = where[key]
                if (type(value) == str):
                    sql += key + "=" + '"' + value + '"' + " "
                else:
                    sql += key + "=" + str(value) + " "
            print(sql)
            result = cursor.execute(sql)
            self.connection.commit()
            print(result)
            self.connection.close()
            return result

    # INSERT INTO table_name (列1, 列2,...) VALUES (值1, 值2,....)
    def insert(self, tabelName, args):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            sql ="INSERT INTO "+tabelName+" ("
            for key in args:
                sql += key+","
            sql = "I"+sql[0:-1]+") VALUES ("
            for key in args:
                value = args[key]
                if (type(value) == str):
                    sql += '"' + value + '"' + " "
                else:
                    sql += str(value) + " "
                sql+=','
            sql = sql[1:-1]+")"
            print(sql)
            result = cursor.execute(sql)
            self.connection.commit()
            return result
            self.connection.close()

    # DELETE FROM Person WHERE LastName = 'Wilson'
    def delete(self, tableName, where):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            sql = "DELETE FROM " + tableName + " "
            sql += " WHERE "
            for key in where:
                value = where[key]
                if (type(value) == str):
                    sql += key + "=" + '"' + value + '"' + " "
                else:
                    sql += key + "=" + str(value) + " "
            print(sql)
            result = cursor.execute(sql)
            self.connection.commit()
            print(result)
            self.connection.close()
            return result


db = DB(host="localhost",user="root",password="root",db="m_blog")
ans = db.query("user", {"name":"hby"},pageNo=1,pageSize=1)
print(ans)
