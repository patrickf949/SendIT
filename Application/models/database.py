"""
Handle database connection
"""

import psycopg2
import psycopg2.extras



class Database():
    """
    Handle database connections
    """
    def __init__(self):
        """
        initialise database connection
        """
        credentials = """
        user='senditdb'
        dbname='senditdb'
        password='sendit123'
        port=5432
        host='localhost'
        """

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
                contact VARCHAR (250) NOT NULL UNIQUE,
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
                weight_kgs INT NOT NULL,
                price INT NULL,
            );            
		"""
        rows = self.execute_query(sql_command)
        return rows


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
        rows = self.execute_query(sql_command)
        return rows


    def add_user(self, user):
        """
        Add user to database
        params:n/a
        returns:n/a
        """
        sql_command = """
        INSERT INTO users (username,email,contact,password,date_created,admin) 
        values ('{username}','{email}','{contact}','{password}',now(),'{admin}');
        """.format(
            username=['username'],
            email=['email'],
            contact=['contact'],
            password=user['password'],
            admin=user['admin']
        )

        rows = self.execute_query(sql_command)
        return rows


    def change_status(self, status, parcel_id):
        """
        change status of parcel delivery order
        params: status and parcel id
        returns: n/a
        """
        sql_command = """
        UPDATE parcels
            SET status = '{status}'
            WHERE 
            parcel_id={parcel_id};
        """.format(status=status, parcel_id=parcel_id)
        rows = self.execute_query(sql_command)
        return rows


    def execute_query(self, sql_command):
        """
        Execute query
        params: sql query statement
        returns: result
        """
        self.cursor.execute(sql_command)
        rows_returned = self.cursor.fetchall()
        rowcount = self.cursor.rowcount()

        return rows_returned
