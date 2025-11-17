import streamlit as st
import plotly.express as px

def main():
    st.title("Plot some data")
    
    ff = px.scatter(x=[], y=[])
    st.plotly_chart(ff, use_container_width=True)

if __name__ == "__main__":
    main()