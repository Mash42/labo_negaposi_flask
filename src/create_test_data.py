import pymysql

# データベースコネクション情報
MYSQL_OPTIONS = {"host": 'db'
                ,"port": 3306
                ,"user": 'negaposi_user'
                ,"passwd": 'negaposi_pass_db'
                ,"db": 'negaposi'
                ,"charset": 'utf8'
                }

def insert_labo_testdata():
    # Insert処理
    conn = pymysql.connect(host=MYSQL_OPTIONS['host'],
                           port=MYSQL_OPTIONS['port'],
                           user=MYSQL_OPTIONS['user'],
                           passwd=MYSQL_OPTIONS['passwd'],
                           db=MYSQL_OPTIONS['db'],
                           charset=MYSQL_OPTIONS['charset'],
                           cursorclass=pymysql.cursors.DictCursor
                           )
    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO TBL_LABO (LABO_ID, LABO_NAME) VALUES (%s, %s)"
            for i in range(10):
                r = cursor.execute(sql, (i+1, "研究室" + str(i+1)))
            print(r)  # -> 1
            # autocommitではないので、明示的にコミットする
            conn.commit()
    finally:
        conn.close()


def insert_labo_comments_testdata():
    # Insert処理
    conn = pymysql.connect(host=MYSQL_OPTIONS['host'],
                           port=MYSQL_OPTIONS['port'],
                           user=MYSQL_OPTIONS['user'],
                           passwd=MYSQL_OPTIONS['passwd'],
                           db=MYSQL_OPTIONS['db'],
                           charset=MYSQL_OPTIONS['charset'],
                           cursorclass=pymysql.cursors.DictCursor
                           )
    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO TBL_STUDENT_COMMENTS (STUDENT_ID, LABO_ID, YEAR, COMMENTS) VALUES (%s, %s, %s, %s)"
            for i in range(30):
                r = cursor.execute(
                    sql, (i+100, 1, 2019, '2019年大量データンゴ' + str(i+1)))
            print(r)  # -> 1
            # autocommitではないので、明示的にコミットする
            conn.commit()
    finally:
        conn.close()

#insert_labo_testdata()
insert_labo_comments_testdata()
