import pandas as pd
import mysql.connector
from mysql.connector import Error

# Function to create a MySQL connection
    
def create_connection(database, user, password, host='localhost'):    
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        if connection.is_connected():
            print(f"The name {database} is already in use !")
            return "Database name already in use !"
    except Error as e:
        # Check if the error is related to the database not existing
        if "Unknown database" in str(e):
            try:
                # If the database doesn't exist, create a new one
                connection = mysql.connector.connect(
                    host=host,
                    user=user,
                    password=password
                )
                cursor = connection.cursor()
                cursor.execute(f"CREATE DATABASE {database}")
                print(f"Database '{database}' created successfully.")
                connection.close()

                # Now, attempt to connect to the newly created database
                connection = mysql.connector.connect(
                    host=host,
                    user=user,
                    password=password,
                    database=database
                )

                if connection.is_connected():
                    print(f"Connected to the database: {database}")
                   
                    return connection

            except Error as e:
                print(f"Error creating or connecting to the database: {e}")
                return None

        else:
            print(f"Error: {e}")
            return None

# Function to create tables and insert data
def excel_to_mysql(excel_file, database):
    # user = 'root'
    # password = 'BJe11cybiR7WpXgfmQJs'
    # host = '70.98.204.225'
    
    # user = 'root'
    # password = 'atm8019atM@'
    # host = 'localhost'
    user = 'root'
    password = 'BJe11cybiR7WpXgfmQJs'
    host = '70.98.204.225'
    schema = {}
    # Read Excel file into a dictionary of DataFrames
    xls_data = pd.read_excel(excel_file, sheet_name=None)

    # Create a MySQL connection
    connection = create_connection(database, user, password, host)
    if connection is None :
        return

    elif connection == "Database name already in use !":
        return "Database name already in use !"
    
    else:
        try:
            cursor = connection.cursor()

            # Iterate through sheets and create tables
            for sheet_name, sheet_data in xls_data.items():
                # Use sheet name as table name (you may need to sanitize the sheet names)
                table_name = sheet_name.lower().replace(" ", "_")
                print(f"Creating table '{table_name}'")

                # Create table with MySQL-specific syntax
                create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join([f'{col} VARCHAR(255)' for col in sheet_data.columns])})"
                print("create_table_query: ",create_table_query)
                cursor.execute(create_table_query)
                print(f"Table '{table_name}' created")

                # Insert data into table
                for _, row in sheet_data.iterrows():
                    insert_query = f"INSERT INTO {table_name} VALUES ({', '.join(['%s']*len(row))})"
                    cursor.execute(insert_query, tuple(row))

                print(f"Data inserted into '{table_name}' table")



            # Define your SQL query
            schema_query = f""" SELECT table_name, column_name
                            FROM INFORMATION_SCHEMA.COLUMNS
                            WHERE table_schema = '{database}';"""

            # Execute the query
            cursor.execute(schema_query)

            # Fetch all rows
            rows = cursor.fetchall()

            # Display the fetched data using st.write
            # with st.sidebar:
            #     st.subheader("Schema:")
            for row in rows:
                table_name, column_name = row
                if table_name not in schema:
                    schema[table_name] = []
                schema[table_name].append(column_name)

            # connection.commit()
            print("Data successfully imported into the MySQL database.")
            #excel_accepted = True
            return connection
        except Error as e:
            print(f"Error: {e}")

        # finally:
        #     if connection.is_connected():
        #         cursor.close()
        #         connection.close()
        #         print("Connection closed.")

# Replace the placeholders with your MySQL details
#excel_file_path = 'd:\OFFICE\AI\DemandScience\DummyData.xlsx'
#database_name = 'sales_v1'
  # Use 'localhost' if MySQL is on the same machine, otherwise provide the IP address

#excel_to_mysql(excel_file_path, database_name)
