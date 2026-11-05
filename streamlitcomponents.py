import streamlit as st
import requests

st.title("Calculator API Client")
st.write("This is a simple Streamlit app that interacts with the Calculator API.")
st.header("Enter two numbers and select an operation to perform.")
st.markdown("### Calculation")
st.subheader("Input Numbers")
a = st.number_input("Enter the first number (a):", value=0.0)
b = st.number_input("Enter the second number (b):", value=0.0)
st.subheader("Select Operation")
operation = st.selectbox("Choose an operation:", ["add", "subtract", "multiply", "divide", "power", "modulo"])  
name = st.text_input("Enter your name:", value="User")
age = st.number_input("Enter your age:", value=0, step=1)
department= st.text_input("Enter you dept:",value="Dept")
number = st.slider("pick a number",0,100)
agree = st.checkbox("i agree the terms")
st.info("info")
st.success("success")
st.warning("warning")
st.error("Error")
if st.button("Clck me"):
    st.write("you clicked me")


