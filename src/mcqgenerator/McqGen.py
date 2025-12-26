import os
import json 
import pandas as pd
import traceback
from src.mcqgenerator.logger import logging
from src.mcqgenerator.utils import read_file, get_table_data
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import JsonOutputParser


load_dotenv()

my_api = os.getenv("my_key")

#step 1: Initialize the model
llm = ChatGoogleGenerativeAI(model = "gemini-3-flash-preview",
                              google_api_key=my_api)


Template = '''
text : {text}
You are a expert at creating multiple choice questions (MCQs) for educational purposes.
Based on the above text, generate {number} multiple choice questions (MCQs) for {subject} students in {tone} tone.
Make shure each question has 4 options (A, B, C, D) and indicate the correct answer also make shure that questions are not repeated in the output.
make shure the format you responce like responce_json below and use it as a guide:
## Responce_json
{responce_json}
'''

prompt = PromptTemplate(input_variables=["text", "number", "tone", "responce_json"],
                        template=Template)


quiz_generation_chain = prompt|llm


Template2 = '''
Your are an expert english grammarian and writer . Give a multiple choice question quiz for {subject} student
you need to evluate the complexity of the questions and give the complete analysis of the quiz. onluy use at  max 50 words for complixty 
if the quiz is not at per the cognitive and analytical ablity of the student ,update the question of the quiz which need to be change and change the tone shuch that it prefectly fits the student ablity
Quize : {quiz}'''


prompt2 = PromptTemplate(input_variables=["subject", "quiz"],
                        template=Template2)

evaluation_chain = prompt2|llm|StrOutputParser()

# Define the parser
parser = JsonOutputParser()

final_chain = (
    
    
           # Run chain 1 to get the 'quiz' text
    RunnablePassthrough.assign(quiz=quiz_generation_chain)# Pass the 'subject' from the original input
    
    | evaluation_chain|parser
)

