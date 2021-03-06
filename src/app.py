from flask import Flask, render_template, request
import pymysql
import requests
import re
from flask import Markup

app = Flask(__name__)

# データベースコネクション情報
MYSQL_OPTIONS = {"host": 'db'
                ,"port": 3306
                ,"user": 'negaposi_user'
                ,"passwd": 'negaposi_pass_db'
                ,"db": 'negaposi'
                ,"charset": 'utf8'
                }

# ホーム
@app.route('/', methods=["GET", "POST"])
def index():
    return render_template("index.html"
                          ,labo_list=get_labo_list()
                          ,comment_list=None
                          ,year_list=get_year_list()
                          )

# 検索
@app.route('/search', methods=["GET", "POST"])
def search():
    comment_list = None
    select_labo_id = None
    select_year = None
    if request.method == 'POST':
        select_labo_id = request.form["labo"]
        select_year = request.form["year"]
        comment_list = get_student_comments(select_labo_id, select_year)
    
    return render_template("index.html"
                          ,labo_list=get_labo_list()
                          ,comment_list=comment_list
                          ,year_list=get_year_list()
                          ,select_labo_id=select_labo_id
                          ,select_year=select_year
                          )

# 研究室データ一覧を取得する。
def get_labo_list():
    conn = getConnection()
    try:
        with conn.cursor() as cursor:
            sql = """
                  SELECT LABO_ID
                        ,LABO_NAME
                    FROM TBL_LABO
                  ;
                  """
            cursor.execute(sql)
            result = cursor.fetchall()
    finally:
        conn.close()
    result_list = list()
    for row in result:
        result_list.append({"labo_id":row["LABO_ID"]
                           ,"labo_name":row["LABO_NAME"]
                           })
    return result_list

# 生徒の感想文データ一覧を取得する
def get_student_comments(lab_id, year):
    conn = getConnection()
    try:
        with conn.cursor() as cursor:
            sql = """
                  SELECT A.STUDENT_ID
                        ,A.LABO_ID
                        ,B.LABO_NAME
                        ,A.YEAR
                        ,A.COMMENTS AS COMMENTS
                    FROM TBL_STUDENT_COMMENTS A
                        ,TBL_LABO B
                  WHERE A.LABO_ID = B.LABO_ID
                    AND A.LABO_ID = %s
                    AND A.YEAR = %s
                  ;
                  """
            cursor.execute(sql, (lab_id, year))
            result = cursor.fetchall()
    finally:
        conn.close()
    result_list = list()
    for row in result:
        result_list.append({"student_id":row["STUDENT_ID"]
                           ,"labo_id":row["LABO_ID"]
                           ,"labo_name":row["LABO_NAME"]
                           ,"year":row["YEAR"]
                           ,"comments":Markup(row["COMMENTS"])
                           })
        print(row["COMMENTS"])
    return result_list

# 年度一覧を取得する。
def get_year_list():
    conn = getConnection()
    try:
        with conn.cursor() as cursor:
            sql = """
                  SELECT DISTINCT YEAR
                    FROM TBL_STUDENT_COMMENTS
                  ;
                  """
            cursor.execute(sql)
            result = cursor.fetchall()
    finally:
        conn.close()
    result_list = list()
    for row in result:
        result_list.append({"year":row["YEAR"]})
    return result_list

# データベースコネクション獲得
def getConnection():
    conn = pymysql.connect(host=MYSQL_OPTIONS['host']
                          ,port=MYSQL_OPTIONS['port']
                          ,user=MYSQL_OPTIONS['user']
                          ,passwd=MYSQL_OPTIONS['passwd']
                          ,db=MYSQL_OPTIONS['db']
                          ,charset=MYSQL_OPTIONS['charset']
                          ,cursorclass=pymysql.cursors.DictCursor
                          )
    return conn

@app.template_filter('cr')
def cr(arg):
    return Markup(arg.replace('\r\n', '<br>'))

# アプリ起動
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
