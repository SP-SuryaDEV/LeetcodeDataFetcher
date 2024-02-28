import streamlit as st
import pandas as pd
import os

st.write('# **Edit Data**')

file = st.file_uploader('Edited Data here')


if file:
    
        file_path = '.\data\All Year.csv'

        
        if os.path.exists(file_path):
            os.remove(file_path)
            st.success('Old CSV file deleted successfully!')

        with open(file_path, "wb") as f:
            f.write(file.getbuffer())
            st.success('New CSV file uploaded and replaced successfully!')