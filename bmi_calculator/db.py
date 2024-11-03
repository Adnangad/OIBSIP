import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

class DB:
    """Connects to the db"""

    def __init__(self) -> None:
        """Initializes attributes"""
        # Connects to the db
        self.connect = psycopg2.connect(
            database=os.getenv("DATABASE"),
            host=os.getenv("HOST"),
            user=os.getenv("USERAUTH"),
            password=os.getenv("PASSWORD"),
            port="5432"
        )
        self.cursor = self.connect.cursor()

    def create_table(self):
        """Creates a users table to store the data"""
        query = '''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                age NUMERIC,
                weight NUMERIC,
                height NUMERIC,
                sex VARCHAR(100)
            );
        '''
        self.cursor.execute(query)
        self.connect.commit()

    def insert_data(self, name):
        """Inserts data to users table"""
        insert_query = '''
            INSERT INTO users (name, age, weight, height, sex)
            VALUES (%s, 0, 0, 0, 'no');
        '''
        self.cursor.execute(insert_query, (name,))
        self.connect.commit()

    def update_data(self, name, age, weight, height, sex):
        """Updates the users data based on the provided info"""
        update_query = '''
            UPDATE users
            SET age = %s, weight = %s, height = %s, sex = %s
            WHERE name = %s;
        '''
        self.cursor.execute(update_query, (age, weight, height, sex, name))
        self.connect.commit()

    def get_data(self, name):
        """Retrieves data from the table based on name"""
        get_query = '''
            SELECT name, age, weight, height, sex FROM users WHERE name = %s;
        '''
        self.cursor.execute(get_query, (name,))
        user = self.cursor.fetchone()
        return user

    def check_data(self, name):
        """Checks if user exists in the table"""
        check_query = '''
            SELECT EXISTS(SELECT 1 FROM users WHERE name = %s);
        '''
        self.cursor.execute(check_query, (name,))
        exists = self.cursor.fetchone()[0]
        return exists

    def close(self):
        """Closes the cursor and connection"""
        self.cursor.close()
        self.connect.close()

db_op = DB()
db_op.create_table()
db_op.close()