import os
import json
import redis
import pika
from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)

# --- Database (PostgreSQL) Connection ---
# We'll use environment variables to get the database connection details from Docker Compose.
DB_HOST = os.environ.get('DB_HOST')
DB_USER = os.environ.get('POSTGRES_USER')
DB_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
DB_NAME = os.environ.get('POSTGRES_DB')

def get_db_connection():
    conn = psycopg2.connect(host=DB_HOST,
                            database=DB_NAME,
                            user=DB_USER,
                            password=DB_PASSWORD)
    return conn

# --- Redis Connection ---
REDIS_HOST = os.environ.get('REDIS_HOST')
r = redis.Redis(host=REDIS_HOST, decode_responses=True)

# --- RabbitMQ Connection ---
MQ_HOST = os.environ.get('MQ_HOST')
connection = pika.BlockingConnection(pika.ConnectionParameters(host=MQ_HOST))
channel = connection.channel()
channel.queue_declare(queue='todo_events')


# --- API Routes ---

@app.route('/')
def home():
    return "Hello from the To-Do Backend!"

@app.route('/todos', methods=['GET'])
def get_todos():
    # Example: fetch from database
    # and maybe cache in Redis
    return jsonify({"message": "This will return to-do items from the database."})

@app.route('/todos', methods=['POST'])
def add_todo():
    data = request.json
    todo_item = data.get('item')
    
    # Example: Save to DB and publish to RabbitMQ
    # Here, we'll just publish a message for now.
    message = {'action': 'added_todo', 'item': todo_item}
    channel.basic_publish(exchange='',
                          routing_key='todo_events',
                          body=json.dumps(message))

    return jsonify({"message": f"To-do item '{todo_item}' added and a message was sent to the queue."}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)