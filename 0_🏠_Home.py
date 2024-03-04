import streamlit as st
import pandas as pd
import logging

logging.basicConfig(filename='server_requests.log', level=logging.INFO, format='%(asctime)s - %(message)s')

logging.info('Received request')
st.session_state['data'] = pd.DataFrame()

st.write('# **Welcome to Leetcode Data Fetcher!!**')
