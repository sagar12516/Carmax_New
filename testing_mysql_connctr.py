import mysql.connector

mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password="3295",
  database="carmax"
)
mycursor = mydb.cursor()
mycursor.execute("drop table customers")
mycursor.execute("CREATE TABLE TESTING_CARMAX(one int, two varchar(255))")
mydb.commit()
mycursor.close()
mydb.close()

