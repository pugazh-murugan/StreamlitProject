import streamlit as st

#title
st.title("BMI calculate")
st.write("Enter the calculate you BMI")

#input from the user
weight = st.number_input("Enter the weeight",min_value=1.0)
height = st.number_input("Enter the height",min_value=1.0)

#Button to calculate
if st.button("calculate BMI"):
    bmi = weight/(height*weight)
    st.write("your BMI is:",round(bmi,2))

    if bmi<10.5:
        st.warning("warning")
    elif bmi<25:
        st.success("success")
    else:
        st.error("error")
