import streamlit as st

#from src.data.load import load_sklearn_object
from src.menu.side_menu import start_side_menu

def main_section():
    st.title("Dashboard for Anomalies")
    



if __name__ == "__main__":


    #model = load_sklearn_object("DecisionTreeClassifier.pkl") 
    #feature_eng = load_sklearn_object("PipelineFeatureEngineering.pkl")

    try:
        main_section()
        start_side_menu()
    except Exception as e:
        print(f'Error during streamlit launch: {e}')