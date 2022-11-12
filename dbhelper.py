import logging

import os

import mysql
import mysql.connector

logger = logging.getLogger(__name__)


def getDB():
    # Open database connection
    DB_HOST = os.environ.get('DB_HOST')
    DB_NAME = os.environ.get('DB_NAME')
    DB_USERNAME = os.environ.get('DB_USERNAME')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')

    return mysql.connector.connect(host=DB_HOST, user=DB_USERNAME, password=DB_PASSWORD, database=DB_NAME)


def get_model_chat_id(chat_id):
    global conn, cursor
    try:
        conn = getDB()

        # prepare a cursor object using cursor() method
        cursor = conn.cursor(dictionary=True)

        # execute SQL query using execute() method.
        query = 'SELECT * FROM messages WHERE chat_id = %s'
        cursor.execute(query, (chat_id,))
        result = cursor.fetchone()

        cursor.close()
        conn.close()
        return result
    except Exception as e:
        logger.info(f'Exception occurred for chat-id:{chat_id}')
        logger.info(f'{e}')

        # rollback if any exception occurred
        conn.rollback()
        cursor.close()
        conn.close()
        return False


def upsert_model_chat_id(chat_id, text, chain):
    global cursor, conn
    try:
        conn = getDB()
        # prepare a cursor object using cursor() method
        cursor = conn.cursor()
        # execute SQL query using execute() method.
        query = "INSERT into messages (chat_id, text, chain) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE text=VALUES(text), chain=VALUES(chain)"
        cursor.execute(query, (chat_id, text, chain,))

        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        logger.info(f'Exception occurred for chat-id:{chat_id}')
        logger.info(f'{e}')
        # rollback if any exception occurred
        conn.rollback()
        cursor.close()
        conn.close()
        return False


def delete_model(chat_id):
    global cursor, conn
    try:
        conn = getDB()

        # prepare a cursor object using cursor() method
        cursor = conn.cursor()

        # execute SQL query using execute() method.
        query = 'DELETE FROM messages WHERE chat_id = %s'
        cursor.execute(query, (chat_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        logger.info(f'Exception occurred for chat-id:{chat_id}')
        logger.info(f'{e}')
        # rollback if any exception occurred
        conn.rollback()
        cursor.close()
        conn.close()