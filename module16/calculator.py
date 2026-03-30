import streamlit as st

st.write("For Adults (18+) calculate here : ")

weight = st.number_input("Enter weight (kilograms) : ")
height = st.number_input("Enter height (meters) : ")

st.write(f"Your BMI is : ")
try :
    weight / (height * height)
except Exception as e:
    st.exception(e)

st.write("For Kids (17-) calculate here : ")

kid_weight = st.number_input("Enter kids weight (in kilograms) : ")
kid_height = st.number_input("Enter kids height (in meters) : ")

st.write(f"Your kids BMI is : ")
try :
    (kid_weight / (kid_height * kid_height)) * 1.3
except Exception as a:
    st.exception(a)