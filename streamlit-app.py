import requests
import streamlit as st
import pandas as pd

@st.cache_data
def retrieve_commits():
        # retrieves amount of commits per week for the last 5 weeks from a github repository
        url = 'https://api.github.com/repos/Tonttu81/linux_admin_kurssi/stats/participation'
        api_token = st.secrets['github_token']
        headers = {
                'Authorization': 'Bearer ' + api_token,
                'Content-Type': 'application/json',
                'Accept': 'application/vnd.github+json'
        }

        response = requests.get(url, headers=headers)
        response_json = response.json()

        commit_counts = response_json['all']
        commit_counts.reverse()
        commit_counts = commit_counts[:5]

        return commit_counts

@st.cache_data
def retrieve_weather():
    conn = st.connection('mysql', type='sql')
    query = conn.query('SELECT * FROM weather_data ORDER BY timestamp DESC LIMIT 50;')


    return query

st.cache_data.clear()

weather_data = retrieve_weather()

st.title('Säädata Helsingistä')
st.dataframe(weather_data)

commit_data = retrieve_commits()
commit_df = pd.DataFrame({
        'Committien määrä': commit_data
})
commit_df.index = [f"{i+1}. viikkoa sitten" for i in range(len(commit_data))]

st.title('Committien määrä viimeiseltä viideltä viikolta tämän sivun repositorystä')
st.dataframe(commit_df)
st.write('Tiedot haetaan Github APIa käyttäen https://github.com/Tonttu81/linux_admin_kurssi repositorystä')