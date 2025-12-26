import os 
import json 
import traceback
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from src.mcqgenerator.logger import logging
from src.mcqgenerator.McqGen import final_chain
from src.mcqgenerator.utils import read_file, get_table_data


with open(r"C:\Data Sceience\PROJECTS\mcqgen\Response.json", "r") as f:
    responce_json = json.load(f)



#creating the title for the app:

st.title("MCQ Generator Application")


#Create a form using st.form:

with st.form("user_input"):
    #file uploader:
    upload_file = st.file_uploader("Upload your file here", type=['pdf', 'txt'])


    #input field:
    mcq_count = st.number_input("Enter number of MCQs to generate", min_value=1, max_value=20, value=5, step=1)

    #subject input:
    subject = st.text_input("Enter the subject for the MCQs",max_chars=20)


    #Quize tone:
    tone = st.selectbox("Select the tone for the MCQs", options=["Formal", "Informal", "Humorous", "Serious", "Encouraging"])

    #add a submit button:
    submit_button = st.form_submit_button("Generate MCQs")



    #check if the submit button is clicked and all fields are filled:

if submit_button and upload_file is not None and mcq_count and subject and tone:
    with st.spinner("Generating MCQs..."):
        try:
            #read the uploaded file:
            file_content = read_file(upload_file)

            #Generate the MCQs using the final_chain from McqGen.py
            result = final_chain.invoke({
                "text": file_content,
                "number": mcq_count,
                "tone": tone,
                "responce_json": json.dumps(responce_json),
                "subject": subject
            })

            #Display the generated MCQs:
            st.success("MCQs Generated Successfully!")
            st.json(result)

            #Convert the result to table data:
            table_data = get_table_data(json.dumps(result))

            #Create a DataFrame:
            df = pd.DataFrame(table_data)

            #Display the DataFrame:
            st.dataframe(df)

            #Provide an option to download the DataFrame as CSV:
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download MCQs as CSV",
                data=csv,
                file_name='generated_mcqs.csv',
                mime='text/csv',
            )

        except Exception as e:
            st.error(f"An error occurred: {e}")