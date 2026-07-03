import streamlit as st
import requests
import json

st.set_page_config(page_title="My Creation", page_icon=":sparkles:", layout="wide")

st.title("My Creation")

number1 = st.number_input("Enter the first number:")
number2 = st.number_input("Enter the second number:")

operation = st.selectbox("Select an operation:", 
                         ["add", "subtract", "multiply", "divide"], help="Choose the arithmetic operation you want to perform"
                         )

payload = {
    "number1": number1,
    "number2": number2,
    "operation": operation
}

if st.button("Calculate"):
    try:
        response = requests.post(f"http://localhost:8000/{operation}", json=payload)
        result = response.json()
        st.success(f"The result is: {result['result']}")
    except Exception as e:
        st.error(f"An error occurred: {e}")

