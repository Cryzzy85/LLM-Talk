import pymysql

filename = '/home/Cryzzy/temp_table.sql'

with open(filename, 'r') as myfile:
    sql = myfile.read()

# Connect to the database
db = pymysql.connect(host='Cryzzy.mysql.pythonanywhere-services.com',
                     user='Cryzzy',
                     password='Xisnix:87',
                     db='Cryzzy$default')

cursor = db.cursor()

# Execute the SQL commands
cursor.execute(sql)

# Commit your changes and close the connection
db.commit()
db.close()