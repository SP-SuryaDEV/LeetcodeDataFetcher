import streamlit as st
import time
import requests
import backoff
import json
import pandas as pd
import os
import logging

contestName = st.text_input("Enter the name of the contest:")
class ForbiddenError(Exception):
    pass
completeData = {}

with st.sidebar:
    uploader = st.file_uploader('Upload any custom files here.. Else All years (II and III) will be choosen by default')

    if uploader:
        with open('temp.csv', 'w') as file:
            file.write(uploader)
        st.session_state.data = pd.read_csv('temp.csv')
        os.remove('temp.csv')
    

if type(st.session_state.get('data')) != pd.DataFrame:
    st.session_state.data = pd.read_csv('./data.csv')

@backoff.on_exception(backoff.expo, ForbiddenError, max_tries=20)
def fetch(contestName,pageNumber):

    headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'cookies' : 'asdweaea',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }
    
    url = f"https://leetcode.com/contest/api/ranking/{contestName}/?pagination={pageNumber}&region=global"
    response = requests.get(url , headers=headers)

    if response.status_code == 200:
        return response
    elif response.status_code == 403:
        print('error raised')
        raise ForbiddenError('forbidden')
    else :
        return response
if contestName:

    if  st.button('fetch'):
    
        pageNumber = 1
        completeData = {}


        while(True):
            st.write(pageNumber)
            response = fetch(contestName,pageNumber)

            if response.status_code == 200:
                json_data = response.json()

                if len(json_data) == 0:
                    st.error("Contest Doesn't exist")
                    break
                
                submissions = json_data['submissions']
                total = json_data['total_rank']

               
                
                if(len(submissions) == 0):
                    break

            

                for i in range(len(submissions)):
                    
                    userName = total[i]['username'].lower()
                    rank = total[i]['rank']+1
                    score = total[i]['score']
                    problemsSolved = len(submissions[i])
                    completeData[userName] = {'rank':rank,"score":score, "problemsSolved" : problemsSolved}
                    st.write(f'Fetched **{userName}**')
                
                
                pageNumber += 1
            elif response.status_code == 404:
                st.error('Contest not found')
                successful = 0
                break
            else:

                print('There might be an error . Try again after some time')
                

        st.download_button(
            label="Download data as CSV",
            data=csv.to_csv().encode("utf-8"),
            file_name=f"{contestName}.csv",
            mime="text/csv",
        )

        st.success('Fetching complete')

        csv = st.session_state.data
        
        csv['Rank'] = ''
        csv['ProbCount'] = ''
        csv['Score'] = ''

        for ind , row in csv.iterrows():
            username = row['Username'].lower()

            if username in completeData:
                csv.loc[ind,'Rank'] = completeData[username]['rank']
                csv.loc[ind,'ProbCount'] = completeData[username]['problemsSolved']
                csv.loc[ind,'Score'] = completeData[username]['score']
            else:
                csv.loc[ind,'Rank'] = 0
                csv.loc[ind,'ProbCount'] = 0
                csv.loc[ind,'Score'] = 0

        filtered_data = csv.copy()
    
        departments = ["All"] + list(csv['Department'].unique())
        sections = ["All"] + list(csv['Section'].unique())
        years = ["All"] + list(csv['Year'].unique())
        domains = ["All"] + list(csv['Domain'].unique())
        
        department = st.selectbox('Department', departments, index=0)
        section = st.selectbox('Section' , sections, index=0)
        year = st.selectbox('Year', years, index=0)
        domain = st.selectbox('Domain', domains, index=0)

        if year:
            if year == 'All':
                filtered_data = csv.copy()
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
