import pymysql

connection = pymysql.connect(
    host="sql6.freesqldatabase.com",
    user="sql6635197",
    password="QK5b9RZy6E",
    db="sql6635197",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)

if connection.open:
    print("the connection to db is opened!")

