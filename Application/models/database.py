"""
Handle database connection
"""

import psycopg2
import psycopg2.extras



class Database():
    
    def __init__(self):
        """
        initialise database connection
        """
        credentials= """
        user='senditdb'
        dbname='senditdb'
        password='sendit123'
        port=5432
        host='localhost'
        """

        connection = psycopg2.connect(credentials)
        connection.autocommit = True
        self.cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        
    
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
                contact VARCHAR (250) NOT NULL UNIQUE,
                password VARCHAR (250),
                date_created TIMESTAMP,
                admin BOOLEAN NOT NULL DEFAULT FALSE
            );
            CREATE TABLE IF NOT EXISTS parcels(
                parcel_id SERIAL PRIMARY KEY,
                user_id INT NOT NULL,
                parcel_description VARCHAR (50) NOT NULL,
                weight_kgs INT NULL,
                price INT NULL,
                pickup_location VARCHAR (250) NOT NULL,
                current_location VARCHAR (250) NULL,
                destination VARCHAR (250) NOT NULL,
                status varchar(25) check (status in ('pending', 'delivered', 'in transit', 'canceled')) DEFAULT 'pending',
                date_created TIMESTAMP,
                date_to_be_delivered TIME
            );
		"""
        self.cursor.execute(sql_command)
        rows = self.cursor.fetchall()
        return rows
    
    def add_parcel(self):
        """
        Add parcel to database
        params:n/a
        returns:n/a
        """
        sql_command = """
        INSERT INTO parcels 
        (user_id, parcel_description, pickup_location, current_location,destination,date_created,date_to_be_delivered) 
        values (now(),now()+);
        """
        self.cursor.execute(sql_command)
    
    
    def add_user(self):
        """
        Add user to database
        params:n/a
        returns:n/a
        """
        sql_command = """
        INSERT INTO users (username,email,contact,password) 
        values ();
        """
        self.cursor.execute(sql_command)
        rows = self.cursor.fetchall()
        return rows
    
    def change_status(self,status,parcel_id):
        """
        change status of parcel delivery order
        params: status and parcel id
        returns: n/a
        """
        sql_command = """
        
        """

    