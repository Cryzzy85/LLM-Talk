from flask import Flask
from flask_mysqldb import MySQL
import csv


# Create an instance of Flask and MySQL
app = Flask(__name__)
mysql = MySQL(app)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'Cryzzy.mysql.pythonanywhere-services.com'
app.config['MYSQL_USER'] = 'Cryzzy'
app.config['MYSQL_PASSWORD'] = 'Xisnix:87'
app.config['MYSQL_DB'] = 'Cryzzy$development'
app.config['MYSQL_PORT'] = 3306

# ... other route definitions and configurations

def export_data_to_csv():
    with mysql.connection.cursor() as cursor:
        describe_query = "DESCRIBE Cryzzy$development.ChatHistory"
        cursor.execute(describe_query)
        columns = [column[0] for column in cursor.fetchall()]

        select_query = "SELECT * FROM Cryzzy$development.ChatHistory"
        cursor.execute(select_query)
        data = cursor.fetchall()

    with open('/home/Cryzzy/my_flask_app/exported_data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(columns)  # Write column names as the header
        writer.writerows(data)

    print('Data exported successfully')

if __name__ == '__main__':
    app.run()
