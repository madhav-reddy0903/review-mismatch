# -*- coding: utf-8 -*-
"""
Created on Fri May 13 18:23:44 2022

@author: madha
"""

import pandas as pd
import streamlit as st
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import streamlit_authenticator as stauth

def identifier(df):
    sentiments = SentimentIntensityAnalyzer()
    data=df[['ID', 'Text', 'Star', 'User Name']]
    data=data[data['Text'].notna()]
    data["Positive"] = [sentiments.polarity_scores(i)["pos"] for i in data["Text"]]
    #data["Negative"] = [sentiments.polarity_scores(i)["neg"] for i in data["Text"]]
    #data["Neutral"] = [sentiments.polarity_scores(i)["neu"] for i in data["Text"]]
    red_data=data.loc[(data["Positive"]>0.5) & (data["Star"]<3)]
    output=red_data[['Text', 'Star', 'User Name']]
    return output
   
names = ['Madhav Reddy','Next Labs']
usernames = ['madhav','nlabs']
passwords = ['123456','456789']
hashed_passwords = stauth.Hasher(passwords).generate()
authenticator = stauth.Authenticate(names,usernames,hashed_passwords,
'some_cookie_name','some_signature_key',cookie_expiry_days=30)
name, authentication_status, username = authenticator.login('Login','main')
if authentication_status:
    authenticator.logout('Logout', 'main')
    st.write('Welcome *%s*' % (name))
    html_temp = """
    <div>
    <h1 style ="color:white;text-align:center;"> Incorrect ratings identifier </h1>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html = True)
    uploaded_file = st.file_uploader("Upload the csv file", type='csv')
    if uploaded_file is not None:
        df1=pd.read_csv(uploaded_file)
        st.write("The following is the list of users whose reviews mismatch with the ratings")
        st.dataframe(identifier(df1))
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
    
