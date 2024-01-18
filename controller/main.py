import mysql.connector
import streamlit as st
import pandas as pd
import openai
# import os
# import excel_to_db as xlsxx
from dotenv import load_dotenv
# import generate_insights as Ins
# import visualization as visual
# Load environment variables
load_dotenv()

# Set OpenAI API key
# openai.api_key = os.getenv('openai_api_key')

openai.api_key = st.secrets["openai_api_key"]

def make_prompt(customer_query,schema):
    prompt = f"""You are a professional DataBase Adminstrator \
        You have to write the syntatically sementically correct sql query \
        the sql query should be transformed from the customer_query \
        Scrictly make sure the attributes and table names to be used for formulating the sql query should be same as the provided schema\
        schema is a dictionary with table names as keys and table columns as their respective values \
        schema can have a single table only or multiple relational tables\
        while formulating the sql query consider the principles of relational database concepts\
        append a semicolon (;)at the end of sql query.\
        if the customer_query doesn't sound like a query, say "Please enter the relevent query !".
        
        
        ```{customer_query}```        
        ```{schema}```
    """
    return prompt

def get_completion(messages, model="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message["content"]

def get_answer(user_query,schema):
    # print('schema:',schema)
    prompt = make_prompt(user_query,schema)
    messages = [
        {"role": "system", "content": prompt}
    ] 

    response = get_completion(messages)
    
    return response


# Function to establish a database connection
def database_connection(host, user, password, database):
    schema = {}
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        if connection.is_connected():
            with st.sidebar:
               st.success(f"Connection Successfull !")

            cursor = connection.cursor()

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
            #st.write(schema)
            return connection,schema

    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        return None

# Function to fetch data from the database
def fetch_data(connection,response):
    try:
        cursor = connection.cursor()
        query = response
        print('query: ',query)
        cursor.execute(query)
        rows = cursor.fetchall()
        # st.write('rows:',rows)    
        #st.subheader("Fetched data:")
        if rows:
            # st.write('rows is not empty data: ',rows)
            return rows
        else:
            st.error(f"Error: Invalid query! Please provide correct information.")

    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        
        
        
        
        
        
        
        
        
'''      
        
def make_prompt(customer_query,schema):
    prompt = f"""You are a professional DataBase Adminstrator \
        You have to write the syntatically sementically correct sql query \
        the sql query should be transformed from the customer_query \
        the attributes and table names to be used for formulating the sql query should be identical to the provided schema\
        schema is a dictionary with table names as keys and table columns as their respective values \
        schema can have a single table only or multiple relational tables\
        while formulating the sql query consider the principles of relational database concepts\
        append a semicolon (;)at the end of sql query.\
        if the customer_query doesn't sound like a query, say "Please enter the relevent query !".
        
        
        ```{customer_query}```        
        ```{schema}```
    """
    return prompt

def get_completion(messages, model="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message["content"]

def get_answer(user_query,schema):

    prompt = make_prompt(user_query,schema)
    messages = [
        {"role": "system", "content": prompt}
    ] 

    response = get_completion(messages)
    
    return response


# Function to establish a database connection
def database_connection(host, user, password, database):
    schema = {}
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        if connection.is_connected():
            with st.sidebar:
               st.success(f"Connection Successfull !")

            cursor = connection.cursor()

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
            #st.write(schema)
            return connection,schema

    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        return None

# Function to fetch data from the database
def fetch_data(connection,response):
    try:
        cursor = connection.cursor()
        query = response
        cursor.execute(query)
        rows = cursor.fetchall()
        #st.subheader("Fetched data:")
        if rows:
            return rows
        else:
            st.error(f"Error: Invalid query! Please provide correct information.")

    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        
        
        '''