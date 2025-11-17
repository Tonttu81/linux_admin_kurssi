import streamlit as st
import pandas as pd
import plotly.express as px

def retrieve_temperatures_from_db():
    conn = st.connection('mysql', type='sql')
    query = conn.query('SELECT * FROM temperature ORDER BY date ASC;')
    return query

def main():
    st.title("Päivittäinen keskilämpötila Oulussa marraskuun aikana")
    
    data = retrieve_temperatures_from_db()

    data_frame = pd.DataFrame(data, columns=["date", "temperature"])

    scatter = px.scatter(data_frame, x='date', y='temperature')
    st.plotly_chart(scatter, use_container_width=True)

    st.write('(ei päivity automaattisesti, päivitetty viimeksi 17.11.)')

if __name__ == "__main__":
    main()