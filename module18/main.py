import streamlit as st
import pandas as pd

st.header("Displaying dataframes")

data = pd.DataFrame({
    "Name" : ["Dreni" , "Gerti" , "Deon"],
    "Age" : ["17" , "12" , "15"],
    "City" : ["Prizren" , "Ferizaj" , "Klines"]
})

st.dataframe(data)