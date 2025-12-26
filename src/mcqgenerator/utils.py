import os
from unittest import result
from PyPDF2 import PdfReader
import json




def read_file(file):
    if file.name.endswith('.pdf'):
       try:
           pdf_reader = PdfReader(file)
           text = ""
           for page in pdf_reader.pages:
               text += page.extract_text() + "\n"
           return text
       except Exception as e:
           raise Exception("Error reading PDF file") from e
    elif file.name.endswith('.txt'):
        text = file.read().decode('utf-8')
        return text
    else:
        raise ValueError("Unsupported file type")
    



def get_table_data(quize_str):

    #convert Quize from string to dictionary:
    try:
        quize_dict = json.loads(quize_str)
        # 1. Create an empty list to hold the cleaned rows
        table_data = []

        # 2. Loop through the dictionary to flatten the data
        # quiz_data is the dictionary you extracted: {"1": {...}, "2": {...}}
        for key, value in quize_dict.items():
            row = {
            "Question_ID": key,
            "Question": value.get("question"),
            "Option_A": value["options"].get("A"),
            "Option_B": value["options"].get("B"),
            "Option_C": value["options"].get("C"),
            "Option_D": value["options"].get("D"),
            "Correct_Answer": value.get("correct_answer")
        }
        table_data.append(row)

        return table_data
    except Exception as e:
        raise ValueError("Error processing quiz data") from e
