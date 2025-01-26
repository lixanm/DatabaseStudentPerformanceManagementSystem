import pymysql

user_name = ''#全局变量，用于存储登录的用户名


#打开数据库
def open():
    # 尝试连接数据库
    db = pymysql.connect(host='localhost',user='root',password='thoth',db='tb_student')
    #print(db)
    return db#返回连接对象


#执行向数据库中，增，删，改操作
def exec(sql,values):
    db=open()#获取连接对象
    cursor=db.cursor()#获取cursor对象
    try:
        cursor.execute(sql,values)
        db.commit()#事物的提交
        return 1
    except Exception as e:
        print(e)
        db.rollback()#事物的回滚
        return 0
    finally:
        cursor.close()
        db.close()

#查询操作  ，模糊查询
def query(sql,*keys):#*key个数可变的位置参数
    db=open()#获取连接对象
    cursor=db.cursor()#获取currsor对象
    cursor.execute(sql,keys)
    result=cursor.fetchall()#查询全部
    cursor.close()
    db.close()
    return result

def query2(sql):
    db=open()
    cursor = db.cursor()  # 获取currsor对象
    cursor.execute(sql)
    result = cursor.fetchall()  # 查询全部
    cursor.close()
    db.close()
    return result

if __name__ == '__main__':
    #sql='insert into tb_user values (%s,%s)'
    #exec(sql,['fjc','123456'])
    #sql='select * from tb_user where userName=%s and userPwd=%s'
    #print(query(sql,'fjc','123456'))
    sql='select * from tb_user'
    print(query2(sql))







