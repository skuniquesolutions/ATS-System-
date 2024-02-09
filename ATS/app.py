import re

from dotenv import load_dotenv
import streamlit as st
import os
import io
import base64

from PIL import Image
import pdf2image
import google.generativeai as genai


load_dotenv()


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_text, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_text, pdf_content[0], prompt])
    return response.text






def input_pdf_setup(uploaded_file):
    # Convert the PDF to Images
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        
        # Extract image data for the second page if available
        if len(images) >= 2:
            # Extract image data for the second page
            second_page_image = images[1]
            
            # Convert image to bytes
            img_byte_arr = io.BytesIO()
            second_page_image.save(img_byte_arr, format='JPEG')
            img_byte_arr = img_byte_arr.getvalue()
            
            # Encode image data to base64
            img_base64 = base64.b64encode(img_byte_arr).decode()
            
            # Create a dictionary containing image data for the second page
            pdf_part = {
                "mime_type": "image/jpeg",
                "data": img_base64
            }
            
            return [pdf_part]  # Return a list containing the image data for the second page
        else:
            raise ValueError("PDF must have at least two pages for scanning the second page")
    else:
        raise FileNotFoundError("No file uploaded")

 
# Streamlit App

st.set_page_config(page_title="ATS Resume Expert")
st.header('ATS Tracking System')
input_text = st.text_area("Job Description: ", key='input')
uploaded_file = st.file_uploader("Upload your resume(PDF)......", type=["pdf"])


if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")
    
    
submit1 = st.button("Tell Me About the Resume")
submit2 = st.button("How Can I Improvise my Skills")
submit3 = st.button("what are the keywords That are Missing")
submit4 = st.button("Percentage match")   
submit5 = st.button("Generate Skill Set")


input_prompt1 = """
You are an experienced HR with Tech Experience in the field of any of these Data Science, Big Data Engineering, 
Data Engineering, DEVOPS, Data Analyst, your task is to review the provided resume against the job description for 
these profiles.
Please share your professional evaluation on whether the candidate's profile aligns with the role.
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""    

input_prompt2 = """
As a skilled professional looking to improve your skills, you want to identify areas for growth based on your current resume.
Please provide a detailed analysis highlighting your strengths and areas for improvement.
Suggest specific skills or experiences that would enhance your qualifications for the desired role.
"""

input_prompt3 = """
You are an experienced ATS (Applicant Tracking System) scanner specializing in the field of any of these Data Science, Big Data Engineering, 
Data Engineering, DEVOPS, and Data Analysis.
Your task is to identify keywords that are essential for the specified job description but missing from the provided resume.
Please list the keywords that the candidate should include in their resume to better align with the job requirements.
"""


input_prompt4 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of any of these Data Science, Big Data Engineering, 
Data Engineering, DEVOPS, Data Analyst and deep ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First, the output should come as a percentage and then keywords missing and last final thoughts.
"""

input_prompt5 = """
You are an experienced ATS (Applicant Tracking System) scanner specializing in the field of Data Science, Big Data Engineering, 
Data Engineering, DEVOPS, and Data Analysis. Your task is to generate a skill set tailored to the job description provided by the user. 
Please provide the skill set according to the job description with formatting similar to the provided resume skill set example.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
        
    else:
        st.write("Please upload the resume") 
        
if submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt2, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
        
    else:
        st.write("Please upload the resume") 
          
if submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
        
    else:
        st.write("Please upload the resume") 
                              
           
if submit4:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt4, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
        
    else:
        st.write("Please upload the resume") 

if submit5:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt5, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
        
    else:
        st.write("Please upload the resume") 