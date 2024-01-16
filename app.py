# connection.cursor?
# what happens when we connect the excel file, no response?
    # if DB_option=='Connect to SQL' and st.session_state['schema']==[]: (validate this line)

from  controller.generate_insights  import get_insights
from controller.main import database_connection, fetch_data, get_answer
import controller.excel_to_db as xlsxx
from controller.visualization import visualization, get_answer_for_visualization
# import mysql.connector
import streamlit as st
import pandas as pd
import openai
import os
# import excel_to_db as xlsxx
from dotenv import load_dotenv
# import generate_insights as Ins
# import visualization as visual
# Load environment variables
load_dotenv()   

# Set OpenAI API key
# openai.api_key = os.getenv('openai_api_key')

openai.api_key = st.secrets["openai_api_key"]


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
        
        
        
if 'host' not in st.session_state:
        st.session_state['host']=[]
        
if 'user' not in st.session_state:
        st.session_state['user']=[]

if 'database' not in st.session_state:
        st.session_state['database']=[]
        

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
    
    DB_option = st.sidebar.selectbox(
    "How would you like to be connected?",
    ("Upload Excel File", "Connect to SQL","Connect to MongoDB"),
    index=None,
    placeholder="Select DB...")
    
    if DB_option=='Upload Excel File' and st.session_state['schema']==[] :
    
        uploaded_file = st.sidebar.file_uploader("Choose a file")
        if uploaded_file is not None:
            # st.sidebar.success('File uploaded Successully')
            db_name = st.sidebar.text_input("Database name: ")
            submit_button = st.sidebar.button("Submit", type="primary")
            if submit_button:
                st.sidebar.success("DB name submitted successfully")
                xls_connection = xlsxx.excel_to_mysql(uploaded_file,db_name)
                st.warning(xls_connection)
                #st.session_state['excel_accepted']=excel_accepted
                st.session_state['xls_connection']=xls_connection
                if  st.session_state['xls_connection'] == "Database name already in use !":
                    st.error(f"Database name already in use !")
                    return
                
    # Sidebar for input fields
    # with st.sidebar:
    #     st.subheader("Connection Settings")
    #     host = st.text_input("MySQL Host:")
    #     user = st.text_input("MySQL Username:")
    #     password = st.text_input("MySQL Password:", type="password")
    #     database = st.text_input("MySQL Database Name:")
        
    if DB_option=='Connect to SQL' and st.session_state['schema']==[]:
        with st.sidebar:    
            st.subheader("Connection Settings")
            st.session_state['host'] = st.text_input("MySQL Host:", value="70.98.204.225")
            st.session_state['user'] = st.text_input("MySQL Username:", value="root")
            st.session_state['password']= st.text_input("MySQL Password:", type="password", value="BJe11cybiR7WpXgfmQJs")
            st.session_state['database']= st.text_input("MySQL Database Name:", value="sales")


        # Connect to the database when the "Connect" button is clicked
        check_connection=st.sidebar.button("Connect", key='check_connection')
        st.session_state['connect_db']=check_connection
        
    
    if DB_option=='Connect to MongoDB' and st.session_state['schema']==[]:
        st.success('Connected to MongoDB')
    
    
    
    # if st.session_state['connect_db']:
        # st.warning('')
        #print(st.sidebar.button("Connect"))
        
    if st.session_state['connect_db'] is not None:
        #print(st.sidebar.button("Connect"))
        if st.session_state['host'] !=[] and st.session_state['user'] !=[] and st.session_state['database'] !=[]:  
            
            db_connection,schema = database_connection(st.session_state['host'], st.session_state['user'] , st.session_state['password'], st.session_state['database'])
            st.session_state['schema']=schema   
            st.write('schema:',schema)

            st.session_state['db_connection']=db_connection
            #st.write(st.session_state['db_connection'])
        if  st.session_state['xls_connection'] != []:
        # if 'xls_connection' in st.session_state and st.session_state['xls_connection'] is not None:
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
                    st.write('user query:',user_query)
                    st.write('schema:',st.session_state['schema'])

# why is schema empltyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy
                    sql_query = get_answer(user_query, st.session_state['schema'])
                    st.write('sql query:',sql_query)
                    with st.expander("Generated SQL Query", expanded=True):
                        st.success(sql_query)
                    if sql_query != "Please enter the relevant query!":

                        # Perform database operations here
                        # st.write("CONNECTION before fetch data:  ",st.session_state['db_connection'])
                        data = fetch_data(st.session_state['db_connection'], sql_query)
                        print(f"==========DATA=============  {data}")
                        query_nature = get_answer_for_visualization(sql_query)
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
                                visualization(data,query_nature)
                        
      
if __name__ == "__main__":
    main()
    