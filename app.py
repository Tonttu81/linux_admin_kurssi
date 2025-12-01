import os
import json
from datetime import datetime

import mysql.connector
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DB_CONFIG = {
    "host": os.environ['sql_host'],
    "user": os.environ['mqtt_user'],
    "password": os.environ['sql_password'],
    "database": os.environ['mqtt_db']
}

@app.route('/api/messages', methods=['GET'])
def get_messages():
    """Hae viestit tietokannasta."""
    limit = request.args.get('limit', 50, type=int)
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT id, nickname, message, client_id, created_at
        FROM messages ORDER BY created_at DESC LIMIT %s
    ''', (limit,))
    messages = cursor.fetchall()
    for msg in messages:
        msg['created_at'] = msg['created_at'].isoformat()
    cursor.close()
    conn.close()
    return jsonify(messages[::-1])

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
    return render_template('index.html', sql_server_time=time)

@app.route('/time')
def time():
    time = get_server_time()
    time_json = json.dumps({'sql_server_time': time})
    return(time_json)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)