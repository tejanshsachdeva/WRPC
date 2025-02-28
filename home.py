import streamlit as st
import DSM.comb_dsm as dsm_app
import REA.comb_rea as rea_app

# Define the homepage
def home():
    st.title("Welcome to the WRPC Data Extractor Tool")
    st.write("Choose the functionality you want to use:")

    if st.button("DSM Functionality"):
        st.session_state.app_choice = "DSM"
        st.rerun()

    if st.button("REA Functionality"):
        st.session_state.app_choice = "REA"
        st.rerun()

# Initialize session state
if 'app_choice' not in st.session_state:
    st.session_state.app_choice = None

# Route based on the user's choice
if st.session_state.app_choice == "DSM":
    dsm_app.main()
elif st.session_state.app_choice == "REA":
    rea_app.main()
else:
    home()
