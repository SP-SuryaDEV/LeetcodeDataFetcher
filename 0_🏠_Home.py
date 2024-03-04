import streamlit as st
import pandas as pd
import logging
from logging import getLogger

print("---------------------------")
app_logger = getLogger()
app_logger.addHandler(logging.StreamHandler())
app_logger.setLevel(logging.INFO)
app_logger.info("best")
print("---------------------------")


st.session_state['data'] = pd.DataFrame()

st.write('# **Welcome to Leetcode Data Fetcher!!**')
