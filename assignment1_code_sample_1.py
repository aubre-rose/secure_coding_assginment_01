import os
import re
import pymysql
from urllib.request import urlopen

# Fix 1
# Instead of hardcoded credentials, use environment variables
def get_db_config():
    """Get database configuration from environment variables"""
    return {
        'host': os.environ.get('DB_HOST', 'localhost'),
        'user': os.environ.get('DB_USER', 'app_user'),  # Use a limited privilege user
        'password': os.environ.get('DB_PASSWORD', ''),  # Get from secure source
        'database': os.environ.get('DB_NAME', 'mydb')
    }

def get_user_input():
 # Fix 2   
 # Basic validation - only allow alphanumeric and common punctuation
    if not re.match(r'^[a-zA-Z0-9\s.,!?-]{1,100}$', user_input):
        raise ValueError("Invalid input format")
    return user_input

def send_email(to, subject, body):
       """Send email securely without shell injection"""
    # Fix 3
    # Validate email format
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', to):
        raise ValueError("Invalid email address")

def get_data():
    url = 'https://secure-api.com/get-data'# Fix 4 - Use HTTPS instead of HTTP to encrypt data in transit
    data = urlopen(url).read().decode()
    return data

# Fix 5 - Use parameterized queries to prevent SQL injection
def save_to_db(data):
    """Save data to database securely using parameterized queries"""
    if data is None:
        return
    
    # Use parameterized query to prevent SQL injection
    query = "INSERT INTO mytable (column1, column2) VALUES (%s, %s)"
    
    # Clean the data before using it
    data = str(data)[:1000]  # Limit length
    
    try:
        connection = pymysql.connect(**get_db_config())
        cursor = connection.cursor()
        cursor.execute(query, (data, 'Another Value'))  # Parameterized query
        connection.commit()
    except pymysql.Error as e:
        print(f"Database error: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


if __name__ == '__main__':
    user_input = get_user_input()
    data = get_data()
    save_to_db(data)
    send_email('admin@example.com', 'User Input', user_input)
