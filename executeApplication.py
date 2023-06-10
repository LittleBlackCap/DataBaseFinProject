# coding=utf-8

import mariadb

def create_connection():
    try:
        user_setting={
            "user":"411077014",
            "password":"411077014",
            "host":"140.127.74.226",
            "database":"411077014"}
        
        connection = mariadb.connect(**user_setting)
        
        return connection

    except mariadb.Error as e:
        print(f"資料庫錯誤: {e}")
        return None

def close_connection(connection):
    connection.close()
    
def command(position):
    if(position==1):
        print("search something where 查詢本地或附近的商品庫存\n")
    elif(position==2):
        print("insert phonenumber 訪問顧客數據、輸入電話訂單\n")
    elif(position==3):
        print("record something where 記錄進貨和更新庫存\n")

def searchInventory(connection, sth, whe):
    try:
        cursor = connection.cursor()

        # query = f"SELECT amount FROM {where} WHERE name=='{sth}'"
        query = f"SELECT ID FROM {whe} WHERE ID=55"
        cursor.execute(query)
        result = cursor.fetchall()

        for row in result:
            print(row)

        cursor.close()

    except mariadb.Error as e:
        print(f"資料庫錯誤: {e}")


def insertOrder(connection, phoneNumber):
    try:
        cursor = connection.cursor()
        # insert 55
        # query = f"INSERT INTO order VALUES (SELECT name FROM customer WHERE phone={phoneNumber})"
        query = f"INSERT INTO test VALUES ((SELECT id FROM test2 WHERE habbit='我愛音樂'),'')"
        cursor.execute(query)
        connection.commit()
        print("資料上傳成功")

        cursor.close()

    except mariadb.Error as e:
        print(f"資料庫錯誤: {e}")

def recordInventory(connection, sth, where):
    try:
        cursor = connection.cursor()
        # record id test2
        query = f"INSERT INTO {where} VALUES (555, (SELECT id FROM test WHERE name='df'))"
        # query = f"INSERT INTO {where} VALUES ('SELECT amount FROM {where} WHERE {sth}==name',{where})"
        cursor.execute(query)
        connection.commit()
        print("資料上傳成功")

        cursor.close()

    except mariadb.Error as e:
        print(f"資料庫錯誤: {e}")
    

def main():
    print("請稍候")
    connection = create_connection()
    
    print("請輸入您的身份(數字): 1 Customer service/ 2 Call center staff/ 3 The stocking clerks")
    position=int(input())
    print("(若不知要查詢什麼可以按「？」、若要結束按「bye」)")
    while(1):
        print("要查詢:",end=" ")
        str=list(input().split())
        if(str[0]=='?'):
            command(position)
        elif(str[0]=='search'):
            searchInventory(connection, str[1], str[2])
        elif(str[0]=='insert'):
            insertOrder(connection, str[1])
        elif(str[0]=='record'):
            recordInventory(connection, str[1], str[2])
        elif(str[0]=='bye'):
            break;
        else:
            print("輸錯指令了請重來")
                
    #execute_select_query(connection, "test")
    #execute_insert_query(connection, "test2", "(4,'swim')")
    
    close_connection(connection)

if __name__ == "__main__":
    main()
