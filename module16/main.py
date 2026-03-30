import streamlit as st

# def main():
#     st.title("Hello World")
#
#     st.button("Click me")
#
# if __name__ = "__main__":
#     main()

if st.button("Click me"):
    st.write("Damn")

st.checkbox("Rsrsrsrs")

if st.checkbox("dneS seduN"):
    st.write("seduN tneS")

user_input = st.text_input("Enter Text" , "Sample text")

st.write("You entered: ", user_input)

age = st.number_input("Enter Age: ", min_value = 0, max_value = 101)

st.write(f"You is {age} older than zero")

message = st.text_area("Enter a message")

st.write(f"Your message {message}")

choice = st.radio("Pick one", ["1"], ["2"], ["3"])

st.write(f"Your choice is : {choice}")

if st.button('Success'):
    st.success("Operation was successful")


try:
    1 / 0
except Exception as e:
    st.exception(e)