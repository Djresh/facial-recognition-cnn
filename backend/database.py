import mysql.connector
import pandas as pd

DB_CONFIG = {
    "host":     "localhost",
    "user":     "root",
    "password": "your_password",
    "database": "facial_recognition_db"
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def create_tables():
    conn   = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recognition_logs (
            id           INT AUTO_INCREMENT PRIMARY KEY,
            person_name  VARCHAR(100) NOT NULL,
            confidence   DECIMAL(5,4),
            recognized_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            image_source VARCHAR(50)  DEFAULT 'webcam'
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registered_persons (
            id            INT AUTO_INCREMENT PRIMARY KEY,
            name          VARCHAR(100) UNIQUE NOT NULL,
            registered_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            sample_count  INT DEFAULT 0
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()
    print("Database tables ready.")

def log_recognition(person_name, confidence, source="webcam"):
    conn   = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO recognition_logs (person_name, confidence, image_source) VALUES (%s, %s, %s)",
        (person_name, confidence, source)
    )
    conn.commit()
    cursor.close()
    conn.close()

def get_recent_logs(limit=50):
    conn = get_connection()
    df   = pd.read_sql(
        "SELECT person_name, confidence, recognized_at, image_source "
        "FROM recognition_logs ORDER BY recognized_at DESC LIMIT %s",
        conn, params=(limit,)
    )
    conn.close()
    return df

def get_recognition_stats():
    conn = get_connection()
    df   = pd.read_sql("""
        SELECT person_name,
               COUNT(*)         AS total_recognitions,
               AVG(confidence)  AS avg_confidence,
               MAX(recognized_at) AS last_seen
        FROM recognition_logs
        WHERE person_name != 'Unknown'
        GROUP BY person_name
        ORDER BY total_recognitions DESC
    """, conn)
    conn.close()
    return df

if __name__ == "__main__":
    create_tables()
