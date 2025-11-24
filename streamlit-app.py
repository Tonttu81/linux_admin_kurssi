import streamlit as st
import pandas as pd

def retrieve_weather():
    conn = st.connection('mysql', type='sql')
    query = conn.query('SELECT * FROM weather_data ORDER BY timestamp DESC LIMIT 50;')
    return query

data = retrieve_weather()
data_frame = pd.DataFrame(data)

st.title('Säädata Helsingistä')
st.dataframe(data_frame)