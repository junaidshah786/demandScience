from  controller.generate_insights  import get_insights
from controller.main import database_connection, fetch_data, get_answer
import controller.excel_to_db as xlsxx

import mysql.connector
import streamlit as st
import pandas as pd
import openai
import os
import excel_to_db as xlsxx
from dotenv import load_dotenv
import generate_insights as Ins
import visualization as visual
# Load environment variables
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv('openai_api_key')



    # finally:
    #     # Close the cursor and connection
    #     if cursor:
    #         cursor.close()
    #     if connection.is_connected():
    #         connection.close()
    #         st.success("Connection closed")
        

if 'db_connection' not in st.session_state:
    st.session_state['db_connection']=[]

if 'connect_db' not in st.session_state:
    st.session_state['connect_db']=[]

if 'schema' not in st.session_state:
    st.session_state['schema']=[]

if 'xls_connection' not in st.session_state:
        st.session_state['xls_connection']=[]
# Main function
def main():
    st.title("Data Craft")
    # Custom CSS styles for button and text box
    st.markdown(
        """
        <style>
            .stButton>button {
            background-color: #000000;
            color: #FFFFFF;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    uploaded_file = st.sidebar.file_uploader("Choose a file")
    if uploaded_file is not None:
        # st.sidebar.success('File uploaded Successully')
        db_name = st.sidebar.text_input("Database name: ")
        submit_button = st.sidebar.button("Submit", type="primary")
        if submit_button:
            st.sidebar.success("DB name submitted successfully")
            xls_connection = xlsxx.excel_to_mysql(uploaded_file,db_name)
            #st.session_state['excel_accepted']=excel_accepted
            st.session_state['xls_connection']=xls_connection
            if  st.session_state['xls_connection'] == "Database name already in use !":
                st.error(f"Database name already in use !")
                return
    # Sidebar for input fields
    with st.sidebar:
        st.subheader("Connection Settings")
        host = st.text_input("MySQL Host:")
        user = st.text_input("MySQL Username:")
        password = st.text_input("MySQL Password:", type="password")
        database = st.text_input("MySQL Database Name:")

    # Connect to the database when the "Connect" button is clicked
    check_connection=st.sidebar.button("Connect", key='check_connection')
    st.session_state['connect_db']=check_connection
    
    
    
    
    if st.session_state['connect_db'] is not None:
        #print(st.sidebar.button("Connect"))
        
        if host and user and database:
            
            db_connection,schema = database_connection(host, user, password, database)
            st.session_state['schema']=schema
            st.session_state['db_connection']=db_connection
            #st.write(st.session_state['db_connection'])
        if 'xls_connection' in st.session_state and st.session_state['xls_connection'] is not None:
            st.session_state['db_connection'] = st.session_state['xls_connection']
            # st.write("CONNECTION xls:   ",st.session_state['xls_connection'])
            # st.write("CONNECTION :   ",st.session_state['db_connection'])
        if st.session_state['db_connection'] is not None:
            
            st.markdown("---")
            with st.form(key='my_form', clear_on_submit=True):  
                user_query = st.text_area("Enter your query:", height=150, max_chars=1000)
                submit_button = st.form_submit_button(label='Draft Insights')
                #st.write(submit_button)
            if submit_button:
                
                if user_query:
                    sql_query = get_answer(user_query, st.session_state['schema'])

                    with st.expander("Generated SQL Query", expanded=True):
                        st.success(sql_query)
                    if sql_query != "Please enter the relevant query!":

                        # Perform database operations here
                        # st.write("CONNECTION before fetch data:  ",st.session_state['db_connection'])
                        data = fetch_data(st.session_state['db_connection'], sql_query)
                        print(f"==========DATA=============  {data}")
                        query_nature = visual.get_answer(sql_query)
                        if any(element is None for element in data[0]):
             
                             st.error(f"Error: Invalid query! Please provide correct information.")
                        else:
                            
                            print(f"USER QUERY : {sql_query} \nsql_query : {query_nature}")
                            if "Insight" in query_nature:
                                # for element in data:
                                #     st.success(element)
                                processed_data = get_insights(user_query,data)
                                st.success(processed_data)
                            else:
                                visual.visualization(data,query_nature)
                        
      
if __name__ == "__main__":
    main()
