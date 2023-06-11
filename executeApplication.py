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
        print(f"資料庫錯誤: {e}\n")
        return None

def close_connection(connection):
    connection.close()
    
def command():
    # if(position==1):
        # print("search something where 查詢本地或附近的商品庫存\n")
    # elif(position==2):
        # print("insert phonenumber 訪問顧客數據、輸入電話訂單\n")
    # elif(position==3):
        # print("record something where 記錄進貨和更新庫存\n")
    print("maxCostCustomer 查找過去一年中累積金額最高的顧客")
    print("searchTopTwoTotalPrice 查找過去一年中按銷售金額計算的前2個產品")
    print("notInKaohsiung 查找所有在高雄的商店都缺貨的產品")
    print("findDelay 查找未按照承諾的時間交付的包裹")
    print("findruined 查找在事故中損壞包裹的顧客聯繫信息。此外，查找該包裹的內容並創建替換商品的新包裹。")
    print("search something where 查詢本地或附近的商品庫存")
    print("insert phonenumber 訪問顧客數據、輸入電話訂單")
    print("record something where 記錄進貨和更新庫存")
    print()

def maxCostCustomer(connection):
    try:
        cursor = connection.cursor()
        query = """
            SELECT cus_name
            FROM (
                SELECT customer.cus_name, SUM(sale_data.total_price) AS total_amount,
                ROW_NUMBER() OVER (ORDER BY SUM(sale_data.total_price) DESC) AS row_num
                FROM sale_data
                INNER JOIN customer ON sale_data.cus_id = customer.cus_id
                WHERE sale_data.sale_date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
                GROUP BY customer.cus_name
            ) AS subquery
            WHERE row_num = 1
        """
        cursor.execute(query)
        result = cursor.fetchall()
        for row in result:
            print(row)
        print()
        cursor.close()
    except mariadb.Error as e:
        print(f"資料庫錯誤: {e}\n")

def maxCostCustomer1(connection):
    try:
        cursor = connection.cursor()
        query = """
            SELECT cus_name 
            FROM customer 
            WHERE cus_id IN (
                SELECT cus_id
                FROM sale_data
                WHERE sale_date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
                GROUP BY cus_id
                ORDER BY SUM(total_price) DESC
                LIMIT 1
            )
        """
        cursor.execute(query)
        result = cursor.fetchall()
        for row in result:
            print(row)
        print()
        cursor.close()
    except mariadb.Error as e:
        print(f"資料庫錯誤: {e}\n")
        
def topTwoTotalPrice(connection):
    try:
        cursor = connection.cursor()
        # query = f"SELECT item_name FROM sale_data,item CROSS APPLY (VALUES (ca.C2),(ca.C3),(ca.C4)) AS T(C) roup by ca.C1,ca.C2,ca.c3,ca.c4"

        # SELECT item_name FROM sale_data,item  MAX(total_price)、max(total_price"
        cursor.execute(query)
        result = cursor.fetchall()
        for row in result:
            print(row)
        print()
        cursor.close()
    except mariadb.Error as e:
        print(f"資料庫錯誤: {e}\n")
        
def notInKaohsiung(connection):
    try:
        cursor = connection.cursor()
        query = """
            SELECT item.item_name
            FROM item
            INNER JOIN shop ON item.item_id = shop.item_id
            WHERE shop.Kaohsiung_store = 0
        """
        cursor.execute(query)
        result = cursor.fetchall()
        for row in result:
            print(row)
        print()
        cursor.close()
    except mariadb.Error as e:
        print(f"資料庫錯誤: {e}\n")
        
def findDelay(connection):
    try:
        cursor = connection.cursor()
        query = f"SELECT order_id FROM trans_info WHERE delay=1"
        cursor.execute(query)
        result = cursor.fetchall()
        for row in result:
            print(row)
        print()
        cursor.close()
    except mariadb.Error as e:
        print(f"資料庫錯誤: {e}\n")
        
def findruined(connection):
    try:
        cursor = connection.cursor()
        cus1 = f"select customer from trans_info,order,customer where (trans_info.state=”損壞” AND trans_info.order_id= order.order_id AND order.cus_id = customer.cus_id)"
        query1 = f"select customer.phone_num from trans_info,order,customer where (trans_info.state=”損壞” AND trans_info.order_id= order.order_id AND order.cus_id = customer.cus_id)"
        cursor.execute(query)
        result = cursor.fetchall()
        for row in result:
            print(row)
        id1 = f"SELECT order_id FROM order ORDER BY id DESC LIMIT 0 , 1"
        query2 = f"INSERT INTO order VALUES (id1[0]+(int(id[1:3])+1),(SELECT order.cus_id,order.price FROM order,trans_info WHERE (trans_info.state=”損壞” AND trans_info.order_id= order.order_id)),CURDATE())"
        cursor.execute(query)
        connection.commit()
        print()
        cursor.close()
    except mariadb.Error as e:
        print(f"資料庫錯誤: {e}\n")

def searchInventory(connection, sth, whe):
    try:
        cursor = connection.cursor()
        # query = f"SELECT amount FROM {where} WHERE name=='{sth}'"
        query = f"SELECT ID FROM {whe} WHERE ID=55"
        cursor.execute(query)
        result = cursor.fetchall()
        for row in result:
            print(row)
        print()
        cursor.close()
    except mariadb.Error as e:
        print(f"資料庫錯誤: {e}\n")


def insertOrder(connection, phoneNumber):
    try:
        cursor = connection.cursor()
        # insert 55
        # query = f"INSERT INTO order VALUES (SELECT name FROM customer WHERE phone={phoneNumber})"
        query = f"INSERT INTO test VALUES ((SELECT id FROM test2 WHERE habbit='我愛音樂'),'')"
        cursor.execute(query)
        connection.commit()
        print()
        cursor.close()
    except mariadb.Error as e:
        print(f"資料庫錯誤: {e}\n")

def recordInventory(connection, sth, where):
    try:
        cursor = connection.cursor()
        # record id test2
        query = f"INSERT INTO {where} VALUES (555, (SELECT id FROM test WHERE name='df'))"
        # query = f"INSERT INTO {where} VALUES ('SELECT amount FROM {where} WHERE {sth}==name',{where})"
        cursor.execute(query)
        connection.commit()
        print()
        cursor.close()
    except mariadb.Error as e:
        print(f"資料庫錯誤: {e}\n")
    

def main():
    print("請稍候......")
    connection = create_connection()
    # print("請輸入您的身份(數字): 1 Customer service/ 2 Call center staff/ 3 The stocking clerks")
    # position=int(input())
    print("(若不知要查詢什麼可以按「？」、若要結束按「bye」)")
    while(1):
        print("要查詢:",end=" ")
        str=list(input().split())
        if(str[0]=='?'):
            command()
        elif(str[0]=='search'):
            searchInventory(connection, str[1], str[2])
        elif(str[0]=='insert'):
            insertOrder(connection, str[1])
        elif(str[0]=='record'):
            recordInventory(connection, str[1], str[2])
        elif(str[0]=='maxCostCustomer'):
            maxCostCustomer(connection)
        elif(str[0]=='searchTopTwoTotalPrice'):
            searchTopTwoTotalPrice(connection)
        elif(str[0]=='notInKaohsiung'):
            notInKaohsiung(connection)
        elif(str[0]=='findDelay'):
            findDelay(connection)
        elif(str[0]=='findruined'):
            findruined(connection)
        elif(str[0]=='bye'):
            break;
        else:
            print("輸錯指令了請重來")
    close_connection(connection)

if __name__ == "__main__":
    main()