from dotenv import load_dotenv
load_dotenv() ## load all the environemnt variables

import streamlit
import os
import sqlite3
import google.generativeai as genai
import streamlit as st

## configure our model
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## load gemini model and provide sql as response
def get_gemini_response (question, prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt[0],question])
    return response.text


## function to retrive from sqlite db
def read_sql_query(sql,db):
    conn=sqlite3.connect(db)
    cur=conn.cursor()
    cur.execute(sql)
    rows=cur.fetchall()
    conn.commit()
    conn.close()
    for row in rows:
        print(row)
    return rows


## define the prompt
prompt=[
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name STUDENT and has the following columns - NAME, CLASS, 
    SECTION \n\nFor example,\nExample 1 - How many entries of records are present?, 
    the SQL command will be something like this SELECT COUNT(*) FROM STUDENT ;
    \nExample 2 - Tell me all the students studying in Data Science class?, 
    the SQL command will be something like this SELECT * FROM STUDENT 
    where CLASS="Data Science"; 
    also the sql code should not have ``` in beginning or end and sql word in output

    """


]

## generate streamlit code
st.set_page_config(page_title="Run sql statement using vanilla English !!!")
st.header("Gemini app to convert sql to English")

question = st.text_input("Input:", key="input")
submit = st.button("Ask the Question ?")

## if submit was clicked
if submit:
    response = get_gemini_response(question=question, prompt=prompt)
    print (response)
    data = read_sql_query(response, "test.db")
    st.subheader("The response is ")
    for row in data:
        print (row)
        st.header(row)
