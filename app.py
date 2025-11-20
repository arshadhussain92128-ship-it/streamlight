import streamlit as st

st.title("BMI Calculator")

weight = st.number_input("Enter weight (kg)")
height = st.number_input("Enter height (m)")

if st.button("Calculate"):
    if height > 0:
        bmi = weight / (height ** 2)
        st.success(f"Your BMI is {bmi:.2f}")
