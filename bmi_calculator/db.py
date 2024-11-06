"""Contains code that operates the database"""

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
                age INTEGER,
                weight DECIMAL,
                height DECIMAL,
                sex VARCHAR(100)
            );
            CREATE TABLE IF NOT EXISTS bmi_history (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                user_id INTEGER REFERENCES users (id),
                bmi DECIMAL,
                date DATE
            );
        '''
        self.cursor.execute(query)
        self.connect.commit()

    def insert_data(self, name, age, weight, height, sex):
        """Adds a user to users table"""
        insert_query = '''
            INSERT INTO users (name, age, weight, height, sex)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id;
        '''
        self.cursor.execute(insert_query, (name, age, weight, height, sex))
        user_id = self.cursor.fetchone()[0]
        self.connect.commit()
        return user_id

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
    
    def get_user_id(self, name):
        """Gets the users id"""
        get_query = '''
            SELECT id FROM users WHERE name = %s;
        '''
        self.cursor.execute(get_query, (name,))
        user_id = self.cursor.fetchone()
        return user_id
    
    def check_data(self, name):
        """Checks if user exists in the table"""
        check_query = '''
            SELECT EXISTS(SELECT 1 FROM users WHERE name = %s);
        '''
        self.cursor.execute(check_query, (name,))
        exists = self.cursor.fetchone()[0]
        return exists
    
    def insert_bmi_date(self, user_id, bmi, date):
        """Adds a BMI and date values to the database."""
        # Check if a record with the given user_id and date already exists
        check_query = '''
            SELECT 1 FROM bmi_history WHERE user_id = %s AND date = %s;
        '''
        self.cursor.execute(check_query, (user_id, date))
        record_exists = self.cursor.fetchone() is not None

        if record_exists:
            # Update the existing record
            query = '''
                UPDATE bmi_history SET bmi = %s WHERE user_id = %s AND date = %s;
            '''
            self.cursor.execute(query, (bmi, user_id, date))
        else:
            # Insert a new record
            query = '''
                INSERT INTO bmi_history (user_id, bmi, date)
                VALUES (%s, %s, %s);
            '''
            self.cursor.execute(query, (user_id, bmi, date))

        # Commit the transaction
        self.connect.commit()
    
    def get_bmi_date(self, user_id):
        """Retreives the bmi and date values of a user"""
        get_query = '''
            SELECT bmi, date FROM  bmi_history WHERE user_id=%s;
        '''
        self.cursor.execute(get_query, (user_id,))
        data = self.cursor.fetchall()
        return data
    
    def delete_all(self):
        """Deletes all users from table users"""
        del_query = '''
            DROP TABLE users CASCADE;
            DROP TABLE bmi_history;
        '''
        self.cursor.execute(del_query)
        self.connect.commit()       
    
    def get_all_users(self):
        """Gets all users"""
        query = '''
            SELECT ALL FROM users;
        '''
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        return data
        
        
    def close(self):
        """Closes the cursor and connection"""
        self.cursor.close()
        self.connect.close()

