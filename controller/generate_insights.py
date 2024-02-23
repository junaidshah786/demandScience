import openai
import os
import pandas as pd
from dotenv import load_dotenv
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# Load environment variables
load_dotenv()
# Set OpenAI API key
openai.api_key = os.getenv('openai_api_key')

def make_prompt(user_query,data):
    prompt = f"""
                Your role is to interpret and analyze the data in alignment with the requirements specified in the user query.\
                The response should not hold any specification of query and structure of data just the conclusion from the data\
                Provide a precise response.\      

        ```{sql_query}``` 
        ```{data}```       
        
    """
    return prompt

def get_completion(messages, model="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message["content"]

def get_insights(sql_query,data):

    prompt = make_prompt(sql_query,data)
    # messages = [
      
    #     {"role": "system", "content": prompt}
    # ] 
    messages = [
        {"role": "system", "content": "You are an expert Data Analyst."},
        {"role": "user", "content": prompt}
    ] 

    response = get_completion(messages)
    
    return response



