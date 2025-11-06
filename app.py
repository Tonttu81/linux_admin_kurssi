from flask import Flask, render_template
import mysql.connector
import os

app = Flask(__name__)
@app.route('/')

def home():
    # Connect to MySQL/MariaDB
    conn = mysql.connector.connect(
        host=os.environ['sql_host'],
        user=os.environ['sql_user'],
        password=os.environ['sql_password'],
        database=os.environ['sql_db']
    )
    cursor = conn.cursor()
    cursor.execute("SELECT NOW()")
    result = cursor.fetchone()
    # Clean up
    cursor.close()
    conn.close()
    return render_template('index.html', server_time=str(result))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)