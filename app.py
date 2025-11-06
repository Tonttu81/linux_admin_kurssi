import os
import json
from datetime import datetime

import mysql.connector
from flask import Flask, render_template

app = Flask(__name__)

def get_server_time():
    conn = mysql.connector.connect(
        host=os.environ['sql_host'],
        user=os.environ['sql_user'],
        password=os.environ['sql_password'],
        database=os.environ['sql_db']
    )
    cursor = conn.cursor()
    cursor.execute("SELECT NOW()")
    result = cursor.fetchone()
    result = result[0].strftime("%Y-%m-%d %H:%M:%S")

    # Clean up
    cursor.close()
    conn.close()

    return(result)

@app.route('/')
def home():
    # Connect to MySQL/MariaDB
    time = get_server_time()
    return render_template('index.html', server_time=time)

@app.route('/time')
def time():
    time = get_server_time()
    time_json = json.dumps({'sql_server_time': time})
    return(time_json)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)