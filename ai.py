import os, streamlit as st, requests
from dotenv import load_dotenv

load_dotenv()


HF_MODEL      = "meta-llama/Llama-3.1-8B-Instruct"
APP_TITLE     = "Health Assistant"
SYSTEM_PROMPT = "You are a health assistant. Never diagnose. Suggest next steps based on user details."

API_KEY = os.getenv("API_KEY")

st.title(APP_TITLE)

age     = st.number_input("Age",            min_value=1,  max_value=120)
gender  = st.selectbox(   "Gender",         ["Male", "Female", "Other"])
weight  = st.number_input("Weight (kg)",    min_value=1,  max_value=300)
chronic = st.text_input(  "Chronic issues", placeholder="e.g. diabetes, asthma or none")


user_input = st.text_area("Describe your symptoms")

if st.button("Run"):
    details = f"Age: {age}, Gender: {gender}, Weight: {weight}kg, Chronic conditions: {chronic}"
    prompt  = f"Patient details: {details}\n\nSymptoms: {user_input}"

    r = requests.post(
        "https://router.huggingface.co/v1/chat/completions",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={"model": HF_MODEL, "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": prompt}
        ], "max_tokens": 512},
        timeout=60
    )
    st.write(r.json()["choices"][0]["message"]["content"].strip())