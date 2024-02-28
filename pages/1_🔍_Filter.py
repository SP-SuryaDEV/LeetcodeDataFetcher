import streamlit as st
import pandas as pd

data = st.session_state.get('data')

st.write('# **Filter Data**')

if type(data) != type(pd.DataFrame()):
    if data == None:
        data = pd.DataFrame()

if data.empty:
    file = st.file_uploader('Drop the Data here')

    if file:
        data = pd.read_csv(file)
    

if not data.empty:
    filtered_data = data.copy()
    
    departments = ["All"] + list(data['Department'].unique())
    sections = ["All"] + list(data['Section'].unique())
    years = ["All"] + list(data['Year'].unique())
    domains = ["All"] + list(data['Domain'].unique())
    
    department = st.selectbox('Department', departments, index=0)
    section = st.selectbox('Section' , sections, index=0)
    year = st.selectbox('Year', years, index=0)
    domain = st.selectbox('Domain', domains, index=0)

    if year:
        if year == 'All':
            filtered_data = data.copy()
        else:
            filtered_data = filtered_data[filtered_data['Year'] == year]
    
        if department:
            if department != 'All':
                filtered_data = filtered_data[filtered_data['Department'] == department]
        
            if section:
                if section != 'All':
                    filtered_data = filtered_data[filtered_data['Section'] == section]
                    
                if domain:
                    if domain != 'All':
                        filtered_data = filtered_data[filtered_data['Domain'] == domain]
    
    st.write(filtered_data)
    st.write(f'Number of students in Filtered Data: {len(filtered_data)}')
