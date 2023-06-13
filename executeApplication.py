# coding=utf-8
import mariadb


def create_connection():
    try:
        user_setting = {
            "user": "411077014",
            "password": "411077014",
            "host": "140.127.74.226",
            "database": "411077014",
        }
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
    print("topTwoTotalPrice 查找過去一年中按銷售金額計算的前2個產品")
    print("notInKaohsiung 查找所有在高雄的商店都缺貨的產品")
    print("findDelay 查找未按照承諾的時間交付的包裹")
    print("findruined 查找在事故中損壞包裹的顧客聯繫信息。此外，查找該包裹的內容並創建替換商品的新包裹。")  # 還有問題
    print("search something(item_id) where(depot,Taipei,Kaohsiung) 查詢本地或附近的商品庫存")
    print("insert phonenumber 訪問顧客數據、輸入電話訂單")  # 還有問題
    print("record something where 記錄進貨和更新庫存")  # 還有問題
    print()


def maxCostCustomer(connection):
    try:
        cursor = connection.cursor()
        query = """
            SELECT cus_name 
            FROM customer 
            ORDER BY cumu_consump DESC
        """
        cursor.execute(query)
        result = cursor.fetchone()
        for row in result:
            print(row)
        print()
        cursor.close()
    except mariadb.Error as e:
        print(f"資料庫錯誤: {e}\n")


def topTwoTotalPrice(connection):
    try:
        cursor = connection.cursor()
        query = """
            SELECT item1_number, item2_number, item3_number, item4_number, item5_number, item6_number, item7_number, item8_number, item9_number, item10_number, item11_number, item12_number, item13_number, item14_number, item15_number, item16_number, item17_number, item18_number, item19_number, item20_number, item21_number, item22_number, item23_number, item24_number 
            FROM sale_data 
            WHERE whatTime='total_price'
        """
        cursor.execute(query)
        row = cursor.fetchall()
        data = list(row[0])
        maximum = max(data)
        maxIndex = data.index(maximum)
        data2 = data
        data2.remove(maximum)
        second = max(data2)
        secondIndex = data.index(second)

        query = """
            SELECT item_name
            FROM item 
            WHERE (item_id=(%s) OR item_id=(%s))
        """
        cursor.execute(query, (maxIndex + 1, secondIndex + 1))
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
        query = """
            SELECT order_id 
            FROM trans_info 
            WHERE delay=1
        """
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
        query = """
            SELECT DISTINCT customer.cus_id 
            FROM trans_info, customer 
            WHERE (trans_info.state = '物件毀損' AND trans_info.cus_id = customer.cus_id)
        """
        cursor.execute(query)
        cus1 = cursor.fetchall()
        print("costumer: ",end="")
        for row in cus1:
            print(row)

        query = """
            SELECT phone_num 
            FROM customer 
            WHERE cus_id= (%s)
        """
        cursor.execute(query, (cus1,))
        result = cursor.fetchall()
        print("此名顧客的聯絡方式為: ", end="")
        for row in result:
            print(row)

        # query = """
        #     SELECT SUM(item.item_price)
        #     FROM item,product,trans_info
        #     WHERE (trans_info.state='物件毀損' AND trans_info.order_id = product.order AND product.item_id = item.item_id)
        # """
        # query = """
        #     SELECT SUM(item_price)
        #     FROM item
        #     WHERE item.id IN %s
        # """
        # cursor.execute(query, (items))
        # items_sum = cursor.fetchall()


        query = """
            SELECT item_id 
            FROM product 
            WHERE state = '物件毀損'
        """
        cursor.execute(query)
        items = cursor.fetchall()
        for row in items:
            print(row)

        query = """
            SELECT SUM(item_price)
            FROM item
            WHERE item_id IN %s
        """
        cursor.execute(query, (items,))
        items_sum = cursor.fetchall()
        for row in items_sum:
            print(row)

        query = """
            SELECT order_id
            FROM orders
            ORDER BY order_id DESC
        """
        cursor.execute(query, (items,))
        lastOrder_id = cursor.fetchone()
        for row in lastOrder_id:
            print(row)

        query = "INSERT INTO orders VALUES ((%s[0]+(int(%s)[1:len(%s)])+1),%s,%s,CURDATE())"
        cursor.execute(query, (lastOrder_id, lastOrder_id, lastOrder_id, cus1, items_sum))
        connection.commit()
        print()
        cursor.close()
    except mariadb.Error as e:
        print(f"資料庫錯誤: {e}\n")


def searchInventory(connection, sth, whe):
    try:
        cursor = connection.cursor()
        if whe == "depot":
            query = f"SELECT store_num FROM depot WHERE item_id={sth}"
            cursor.execute(query)
            result = cursor.fetchall()
            for row in result:
                print(row)
        elif whe == "Taipei":
            query = f"SELECT Taipei_store FROM shop WHERE item_id={sth}"
            cursor.execute(query)
            result = cursor.fetchall()
            for row in result:
                print(row)
        else:
            query = f"SELECT Kaohsiung_store FROM shop WHERE item_id={sth}"
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
        # query = f"INSERT INTO orders VALUES (B131,(SELECT cus_id FROM customer WHERE phone={phoneNumber}),)"
        query = (
            f"INSERT INTO orders VALUES ((SELECT id FROM test2 WHERE habbit='我愛音樂'),'')"
        )
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
        query = (
            f"INSERT INTO {where} VALUES (555, (SELECT id FROM test WHERE name='df'))"
        )
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
    while 1:
        print("要查詢:", end=" ")
        str = list(input().split())
        if str[0] == "?":
            command()
        elif str[0] == "search":
            searchInventory(connection, str[1], str[2])
        elif str[0] == "insert":
            insertOrder(connection, str[1])
        elif str[0] == "record":
            recordInventory(connection, str[1], str[2])
        elif str[0] == "maxCostCustomer":
            maxCostCustomer(connection)
        elif str[0] == "topTwoTotalPrice":
            topTwoTotalPrice(connection)
        elif str[0] == "notInKaohsiung":
            notInKaohsiung(connection)
        elif str[0] == "findDelay":
            findDelay(connection)
        elif str[0] == "findruined":
            findruined(connection)
        elif str[0] == "bye":
            break
        else:
            print("輸錯指令了請重來")
    close_connection(connection)


if __name__ == "__main__":
    main()
