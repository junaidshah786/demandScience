from controller.generate_insights import get_insights
from controller.main import database_connection, fetch_data, get_answer
import controller.excel_to_db as xlsxx
from controller.visualization import visualization, get_answer_for_visualization
import streamlit as st
# from dotenv import load_dotenv
import openai
import time
# load_dotenv()

openai.api_key = st.secrets["openai_api_key"]

def initialize_session_state():
    session_state_vars = ['db_connection', 'connect_db', 'schema', 'xls_connection', 'host', 'user', 'database']

    for var in session_state_vars:
        if var not in st.session_state:
            st.session_state[var] = []

def upload_excel_file():
    if st.session_state['schema'] == []:
        uploaded_file = st.sidebar.file_uploader("Choose a file")
        if uploaded_file is not None:
            db_name = st.sidebar.text_input("Project name: ")
            submit_button = st.sidebar.button("Submit", type="primary")

            if submit_button:   
                success_message = st.sidebar.success("DB name submitted successfully")
                time.sleep(2)
                success_message.empty()
                xls_connection, schema = xlsxx.excel_to_mysql(uploaded_file, db_name)
                st.session_state['schema'] = schema
                # st.warning(xls_connection)
                st.session_state['xls_connection'] = xls_connection
                if st.session_state['xls_connection'] == "Database name already in use !":
                    st.error("Database name already in use !")
                    return

def connect_to_sql():
    if st.session_state['schema'] == []:
        with st.sidebar:
            st.subheader("Connection Settings")
            st.session_state['host'] = st.text_input("MySQL Host:", value="70.98.204.225")
            st.session_state['user'] = st.text_input("MySQL Username:", value="root")
            st.session_state['password'] = st.text_input("MySQL Password:", type="password", value="BJe11cybiR7WpXgfmQJs")
            st.session_state['database'] = st.text_input("MySQL Database Name:")
            # st.session_state['database'] = st.text_input("MySQL Database Name:", value="qwertyuiop")


        check_connection = st.sidebar.button("Connect", key='check_connection')
        st.session_state['connect_db'] = check_connection

def main():
    try:
        st.title("Data Craft")
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

        initialize_session_state()

        DB_option = st.sidebar.selectbox(
            "How would you like to be connected?",
            ("Upload Excel File", "Connect to SQL", "Connect to MongoDB"),
            index=None,
            placeholder="Select DB..."
        )   
        
        if DB_option is None:
            # st.sidebar.success(DB_option)
            session_state_vars = ['db_connection', 'connect_db', 'schema', 'xls_connection', 'host', 'user', 'database']

            for var in session_state_vars:
                # if var not in st.session_state:
                st.session_state[var] = []
            

        # show_sql_query=st.sidebar.toggle('Show SQL query')

        if DB_option == 'Upload Excel File':
            upload_excel_file()

        elif DB_option == 'Connect to SQL':
            connect_to_sql()

        elif DB_option == 'Connect to MongoDB':
            st.success('Connected to MongoDB')

        if st.session_state['host'] and st.session_state['user'] and st.session_state['database']:
            db_connection, schema = database_connection(
                st.session_state['host'],
                st.session_state['user'],
                st.session_state['password'],
                st.session_state['database']
            )
            # print('schema: ',schema)
            st.session_state['schema'] = schema
            st.session_state['db_connection'] = db_connection

        if st.session_state['xls_connection']:
            st.session_state['db_connection'] = st.session_state['xls_connection']
            

        if st.session_state['db_connection']:
            # st.write('schema: ',st.session_state['schema'])
            st.markdown("---")
            with st.form(key='my_form', clear_on_submit=True):  
                # user_query = st.text_area("Enter your query:", height=150, max_chars=1000)
                # Check if the user_query key exists in session_state, if not set to an empty string
                user_query = st.session_state.get('user_query', '')
                user_query = st.text_area("Enter your query:", value=user_query, height=70, max_chars=1000)

                submit_button = st.form_submit_button(label='Draft Insights')
                
                
                chart_type = st.selectbox("Select Chart Type", ["bar", "line", "scatter"])  # Add more chart types as needed

            if submit_button and user_query:
                sql_query = get_answer(user_query, st.session_state['schema'])
                # with st.expander("Generated SQL Query", expanded=False):
                #     st.success(sql_query)
                
                
                # if show_sql_query:
                with st.sidebar.expander("Generated SQL Query", expanded=False):
                    st.success(sql_query)
                        
                        
                        
                        

                if sql_query != "Please enter the relevant query!":
                    # st.write('db connection 112: ', st.session_state['db_connection'])
                    # it fetches the answer using the sql command geenrated
                    data = fetch_data(st.session_state['db_connection'], sql_query)
                    print('data:', data)
                    # gives an answer in user friendly format using LLM
                    query_nature = get_answer_for_visualization(sql_query)
                    
                    # st.write(query_nature)
                    if any(element is None for element in data[0]):
                        st.error("Error: Invalid query! Please provide correct information.")
                    else:
                        if "Insight" in query_nature:
                            # st.write('')
                            processed_data = get_insights(user_query, data)
                            st.success(processed_data)
                        else:
                            # print('data used for visualzation: ', data)
                            
                            visualization(data, query_nature,chart_type)

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        print(f'ERROR OCCURED: {str(e)}')   

if __name__ == "__main__":
    main()
