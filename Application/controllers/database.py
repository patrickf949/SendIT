"""
Handle database connection
"""

import psycopg2
import psycopg2.extras
from flask import jsonify


class Database():
    """
    Handle database connections
    """
    
    def __init__(self, dbname='senditdb'):
        """
        initialise database connection
        """
        credentials = """
        user='senditdb'
        dbname={}
        password='s3ndIt2m3'
        port=5432
        host='localhost'
        """.format(dbname)

        connection = psycopg2.connect(credentials)
        connection.autocommit = True
        self.cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        self.create_tables()


    def create_tables(self):
        """
        Create necessary tables in database
        params:n/a
        returns:n/a
        """
        sql_command = """
            CREATE TABLE IF NOT EXISTS users(
                user_id SERIAL PRIMARY KEY,
                username VARCHAR (250) NOT NULL UNIQUE,
                email VARCHAR (250) NOT NULL UNIQUE,
                contact VARCHAR (250) NOT NULL,
                password VARCHAR (250) NOT NULL,
                date_created TIMESTAMP NOT NULL,
                admin BOOLEAN NOT NULL DEFAULT FALSE
            );
            CREATE TABLE IF NOT EXISTS parcels(
                parcel_id SERIAL PRIMARY KEY,
                user_id INT NOT NULL,
                parcel_description VARCHAR (50) NOT NULL,
                weight_kgs INT NULL,
                price INT NULL,
                recipient VARCHAR (250) NOT NULL,
                recipient_contact VARCHAR (250) NOT NULL,
                pickup_location VARCHAR (250) NOT NULL,
                current_location VARCHAR (250) NULL,
                destination VARCHAR (250) NOT NULL,
                status varchar(25) check (status in ('pending', 'delivered', 'in transit', 'canceled')) DEFAULT 'pending',
                date_created TIMESTAMP,
                date_to_be_delivered TIME
            );
            CREATE TABLE IF NOT EXISTS weight_categories(
                weight_id SERIAL PRIMARY KEY,
                weight_kgs NUMRANGE NOT NULL UNIQUE,
                price INT NOT NULL UNIQUE
            );
		"""
        self.cursor.execute(sql_command)
        self.insert_into_weight_categories()


    def insert_into_weight_categories(self):
        """
        insert default values into weight categories
        params:n/a
        returns:n/a
        """
        sql_command="""
        INSERT INTO weight_categories (price, weight_kgs)
        VALUES (2000,'[0, 0.1)'),
               (3000,'[0.1, 0.5)'),
               (6000,'[0.5, 1)'),
               (10000,'[1, 2)'),
               (15000,'[2, 5)'),
               (20000,'[5, 10)'),
               (25000,'[10, 20)'),
               (30000,'[20, 30)'),
               (40000,'[30, 50)'),
               (70000,'[50, 100)'),
               (100000,'[100, 200)'),
               (200000,'[200, 500)'),
               (700000,'[500, 1000)');
        """
        sql_command1="""
        SELECT EXISTS(SELECT TRUE FROM weight_categories WHERE price=3000)
        """
        table_empty = self.execute_query(sql_command1)
        if not table_empty:
            self.cursor.execute(sql_command)



    def add_parcel(self, parcel):
        """
        Add parcel to database
        params:n/a
        returns:n/a
        """
        sql_command = """
        INSERT INTO parcels 
        (user_id, parcel_description, recipient, recipient_contact,
        pickup_location, current_location, destination, date_created,date_to_be_delivered)
        values ({user_id},'{recipient}','{contact}','{parcel_description}','{pickup_location}',
        '{current_location}','{destination}', now(), now()+'2 days 2 hours');
        """.format(
            user_id=parcel['user_id'],
            parcel_description=parcel['parcel_description'],
            recipient=parcel['recipient'],
            contact=parcel['contact'],
            pickup_location=parcel['pickup_location'],
            current_location=parcel['pickup_location'],
            destination=['destination']
        )
        rows = self.cursor.execute(sql_command)
        add_parcel = self.execute_query
        return rows


    def add_user(self, user):
        """
        Add user to database
        params: user information in dictionary
        returns:n/a
        """
        sql_command = """
        INSERT INTO users (username,email,contact,password,date_created,admin) 
        values ('{username}','{email}','{contact}','{password}',now(),'{admin}');
        """.format(
            username=user['username'],
            email=user['email'],
            contact=user['contact'],
            password=user['password'],
            admin=user['admin']
        )

        self.cursor.execute(sql_command)

        user_added = self.check_availability_of_userdetails('username',user['username'])
        print(user_added[0]['exists'])
        return user_added[0]['exists']


    def change_status(self, column, value, parcel_id):
        """
        change status of parcel delivery order
        params: status and parcel id
        returns: n/a
        """
        sql_command = """
        UPDATE parcels
            SET {column} = '{value}'
            WHERE 
            parcel_id={parcel_id};
        """.format(column=column, value=value, parcel_id=parcel_id)
        rows = self.execute_query(sql_command)
        return rows


    def check_availability_of_userdetails(self, column, value):
        """
        Check if user exists during login or signup
        params: column name, value
        returns: n/a
        """
        sql_command="""
        SELECT EXISTS(SELECT 1 FROM users where {column}='{value}');
        """.format(value=value, column=column)
        exists = self.execute_query(sql_command)
        return exists


    def get_from_users(self, column, username):
        """
        Get column from users table
        params:column name, username
        returns:password
        """
        sql_command="""
        SELECT {column} FROM users where username='{username}';
        """.format(username=username, column=column)
        db_password = self.execute_query(sql_command)

        return db_password[0][column]

    def validate_password(self,username,password):
        """
        Check if password password is equal to password in database
        """
        db_password = self.get_from_users('password',username)
        if password != db_password:
            return jsonify({'message':'invalid username or password'}), 400

        return True


    def check_availability_of_anyuser(self):
        """
        Check if user exists during login or signup
        params: username
        returns: n/a
        """
        sql_command="""
        SELECT EXISTS(SELECT TRUE FROM users where user_id=1)
        """
        exists = self.execute_query(sql_command)
        return exists

    def check_availability_of_anyparcel(self, username):
        """
        Check if user exists during login or signup
        params: username
        returns: n/a
        """
        sql_command="""
        SELECT EXISTS(SELECT TRUE FROM parcels)
        """
        exists = self.execute_query(sql_command)
        return exists[0]['exists']


    def execute_query(self, sql_command):
        """
        Execute query
        params: sql query statement
        returns: result
        """
        self.cursor.execute(sql_command)
        rows_returned = self.cursor.fetchall()

        return rows_returned

    
    def drop_all_tables(self):
        self.cursor.execute("Drop table users,parcels,weight_categories")
