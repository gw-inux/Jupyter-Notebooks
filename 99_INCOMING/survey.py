import streamlit as st
from streamlit_star_rating import st_star_rating
import pandas as pd
import os
import pycountry

# Save function
def save_response(data, file_path="responses.csv"):
    df = pd.DataFrame([data])
    if os.path.exists(file_path):
        df.to_csv(file_path, mode='a', header=False, index=False)
    else:
        df.to_csv(file_path, index=False)

# ---- Get country names from pycountry ----
countries = sorted([country.name for country in pycountry.countries])

default_country = countries.index('Sweden')

# ---- Profession ----
professions = [
    "Student",
    "Software Developer",
    "Data Scientist",
    "Engineer",
    "Researcher",
    "Teacher / Educator",
    "Academic / Professor",
    "Consultant",
    "Government / Public Sector",
    "Writer / Journalist",
    "Retired",
    "Other"
]

# ---- UI ----
st.title("User Feedback Survey")

with st.form("survey_form", clear_on_submit=True):
    # How satisfied are you?
    #satisfaction = st.radio(
    #    "How satisfied are you with this app?",
    #    ["Very satisfied", "Satisfied", "Neutral", "Unsatisfied", "Very unsatisfied"]
    #)
    stars = st_star_rating("Please rate you experience", maxValue=5, defaultValue=3, key="Rating")
    # Education
    # education = st.radio(
    #     "What is your academic education level?",
    #     ["No academic education", "Bachelor", "Masters", "PhD", "Other"]
    # )    

    # Time spent
    time = st.radio(
         "How much time did you spend?",
         ["Less than 10 min", "10-30 min", "30-60 min", "More than 60 min"]
    )

    profession = st.selectbox("What is your profession?", professions)    
    #age = st.slider("What is your age?", 18, 100, 25)
    country = st.selectbox("Which country are you from?", countries, index=default_country)
    comments = st.text_area("Any additional comments?")

    submitted = st.form_submit_button("Submit")

    if submitted:
        response = {
            #"satisfaction": satisfaction,
            "stars": stars,
            "time": time,
            # "education": education,
            "profession": profession,
            #"age": age,            
            "country": country,
            "comments": comments
        }
        save_response(response)
        st.success("Thank you for your feedback!")

df = pd.read_csv('responses.csv')

def convert_for_download(df):
    return df.to_csv(index=False).encode("utf-8")

csv = convert_for_download(df)

st.download_button(
    label="📥 Download responses as CSV",
    data=csv,
    file_name='survey_responses.csv',
    mime='text/csv'
)