import json
import os
import psycopg2
from psycopg2.extras import execute_values
from api_request import mock_fetch_data, fetch_data

def connect_to_db():
    host = os.getenv('DB_HOST', 'db')
    port = int(os.getenv('DB_PORT', 5432))

    print(f"Connecting to the PostgreSQL database at {host}:{port}...")
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            dbname='db',
            user='db_user',
            password='db_password'
        )

        return conn
    except psycopg2.Error as e:
        print(f"Database connection failed: {e}")
        raise

def create_table(conn):
    print("Creating table if not exist...")
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE SCHEMA IF NOT EXISTS dev;
            CREATE TABLE IF NOT EXISTS dev.raw_news (
                id SERIAL PRIMARY KEY,
                article_id TEXT UNIQUE,
                title TEXT,
                description TEXT,
                pub_date TIMESTAMP,
                source_id TEXT,
                category TEXT[],
                language TEXT,
                raw_json JSONB,  -- This is a pro-tip: store the whole thing just in case!
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        conn.commit()
        print('Table was created.')
    except psycopg2.Error as e:
        print(f"Failed to create table: {e}")
        raise

def insert_records(conn, data):
    print("Inserting records into the database...")
    cursor = conn.cursor()

    values = [
        (
            item.get('article_id'),
            item.get('title'),
            item.get('description'),
            item.get('pubDate'),
            item.get('source_id'),
            item.get('category'),
            item.get('language'),
            json.dumps(item)
        )
        for item in data
    ]

    insert_query = """
        INSERT INTO dev.raw_news (article_id, title, description, pub_date, source_id, category, language, raw_json)
        values %s
        ON CONFLICT (article_id) DO NOTHING;
    """
    try:
        execute_values(cursor, insert_query, values)
        conn.commit()
        print(f'Successfully inserted {len(values)} articles.')
    except Exception as e:
        print(f"Error during insertion: {e}")
        raise

def main():
    try:
        # data = mock_fetch_data()
        data = fetch_data()
        conn = connect_to_db()
        create_table(conn)
        insert_records(conn, data)
    except Exception as e:
        print(f'An error occured during execution: {e}')
    finally:
        if 'conn' in locals():
            conn.close()
            print("Database connection closed.")


if __name__ == '__main__':
    main()




