### Health Management APP
from dotenv import load_dotenv

load_dotenv() ## load all the environment variables

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
import pandas as pd
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load Google Gemini Pro Vision API And get response

def get_gemini_repsonse(input_prompt,image_data):
    model=genai.GenerativeModel('gemini-1.5-flash')
    response=model.generate_content([input_prompt,image_data[0]])
    return response.text

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

#Function to save feedback

def save_feedback(feedback_text):
    feedback_file= "feedback.csv"
    feedback_data = pd.DataFrame([[feedback_text]], columns=["feedback"])
    
    if os.path.exists(feedback_file):
        feedback_data.to_csv(feedback_file, mode = 'a', header=False, index=False)
    else:
        feedback_data.to_csv(feedback_file, mode='w', header=True, index=False)

#Function to load feedback
def load_feedback():
    feedback_file = "feedback.csv"
    if os.path.exists(feedback_file):
        feedback_data = pd.read_csv(feedback_file)
        return feedback_data
    else:
        return pd.DataFrame(columns=["feedback"])   
##initialize our streamlit app

st.set_page_config(page_title="Gemini Health App")

st.header("Gemini Health App")
user_prompt = st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)


default_input_prompt="""
You are a nutrition expert. Your task is to analyze the provided image of food items, identify each item, and calculate the total caloric intake. Additionally, provide a detailed breakdown of each food item along with its respective calorie content, determine whether the food is healthy or not and mention the percentage split of protein, fat, carbohydrates, and fiber in the diet. Finally, provide a conclusion summarizing the overall nutritional quality of the meal. Please present the information in the following format:
Item 1 - Number of calories
Health Status: Healthy/Unhealthy
Nutritional Breakdown:
Protein: X%
Fat: X%
Carbohydrates: X%
Fiber: X%
Item 2 - Number of calories
Health Status: Healthy/Unhealthy
Nutritional Breakdown:
Protein: X%
Fat: X%
Carbohydrates: X%
Fiber: X%
Item 3 - Number of calories
Health Status: Healthy/Unhealthy
Nutritional Breakdown:
Protein: X%
Fat: X%
Carbohydrates: X%
Fiber: X%

Total Calories: Number of calories

Conclusion: Summarize the overall nutritional quality of the meal, including the balance of macronutrients, the healthiness of the food items, and any recommendations for improvement.
"""

## If submit button is clicked

if st.button("Analyze Meal"): 
    if uploaded_file is not None:
        image_data = input_image_setup(uploaded_file) 
        input_prompt = user_prompt if user_prompt else default_input_prompt 
        response = get_gemini_repsonse(input_prompt, image_data) 
        st.subheader("FitGen-Ai Analysis")
        st.write(response)
    else:
        st.error("please upload image of your meal")