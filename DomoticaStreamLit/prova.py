import os
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

def main_menu():
    
    st.title("AnomalyDetection Domotica Reti")
    st.write("Si mostrano un po di elementi per creare una dashboard")
    st.markdown('Possiamo *anche* aggiungere un **po\'** di markdown')
    df_expander = st.beta_expander("Dataframe")
    df_expander.write('Stampiamo anche un Dataframe di Pandas')
    df = pd.DataFrame({'first column':[1, 2, 3, 4],'second column':[10, 20, 30, 40]})
    df_expander.write(df)
    df_expander.write('Possiamo anche colorare delle celle')
    df = pd.DataFrame(np.random.randn(10,20),columns=('col %d' %i for i in range(20)))
    df_expander.write(df)
    df_expander.dataframe(df.style.highlight_max(axis=0))
    chart_expander = st.beta_expander("Chart")
    chart_expander.header('Adesso passiamo ai grafici')
    chart_expander.write('streamlit supporta diverse lirerie per i grafici tipo **matplotlib**')
    chart_expander.write('I primi 2 sono nativi')
    chart_data = pd.DataFrame(np.random.randn(20,3),columns=['a', 'b', 'c'])
    chart_expander.line_chart(chart_data)
    chart_expander.bar_chart(chart_data)
    chart_expander.write('Esempio con matplotlib')
    arr = np.random.normal(1,1,size=100)
    fig, ax = plt.subplots()
    ax.hist(arr,bins=20)
    chart_expander.pyplot(fig)
    chart_expander.write('Esempio mappa con streamLit')
    df = pd.DataFrame(np.random.randn(1000, 2) / [50,50] + [37.76, -122.4], columns = ['lat', 'lon'])
    chart_expander.map(df)
    image_expander = st.beta_expander("Images")
    image_expander.write('E\' possibile scrivere immagini')
    pathImage = os.path.join(os.path.abspath('..'),'Image','610uFnTVcVL.png')
    image = Image.open(pathImage)
 #   image = Image.open("..\\Image\\610uFnTVcVL.png")
    image_expander.image(image,use_column_width=True)


if __name__ == "__main__":
    main_menu()