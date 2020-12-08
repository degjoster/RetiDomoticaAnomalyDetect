import streamlit as st

from src.menu.side_menu import start_side_menu

def main_section():
    st.title("Dashboard for Anomaly Detection")
    
if __name__ == "__main__":

    try:
        main_section()
        start_side_menu()
    except Exception as e:
        print(f'Error during streamlit launch: {e}')