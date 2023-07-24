import pymysql

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    db="network_analysis",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)
if connection.open:
    print("the connection to db is opened!")