# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 15:08:43 2023

@author: harivars
"""

import pickle
import numpy as np
import pandas as pd
import streamlit as st
from streamlit_card import card

popular_df = pickle.load(open('popular.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))


st.title('Get Your Favorite Book Recommendations')

st.subheader('Get Your Recommendations Here')
predict_option = st.radio('Select One Option:', ('Most Popular Books', 'Personalized Recommendations'))

data = []
for i in range(0,50):
    x = {'Image': popular_df['Image-URL-M'].values[i],
         'Title': popular_df['Book-Title'].values[i],
            'Author':popular_df['Book-Author'].values[i],
            'Ratings':popular_df['Number-of-Ratings'].values[i],
            'Average Rating': (popular_df['Average-Rating'].values[i]).round(1)}
    data.append(x)
## Most Popular Books
if predict_option == 'Most Popular Books':
    st.subheader('Top 50 Books:')
    col1, col2, col3 = st.columns(3)
    
    with col1:
        for i in range(0, 48, 3):
            st.markdown(i+1)
            st.image(data[i]['Image'])
            st.write(data[i]['Title'])
            st.write('Author: ', data[i]['Author'])
            st.write('Number of Ratings:', data[i]['Ratings'])
            st.write('Average Rating:', data[i]['Average Rating'])
            st.write('--------------------------------------------------')
    
    with col2:
        for i in range(1, 49, 3):
            st.markdown(i+1)
            st.image(data[i]['Image'])
            st.write(data[i]['Title'])
            st.write('Author:', data[i]['Author'])
            st.write('Number of Ratings:', data[i]['Ratings'])
            st.write('Average Rating:', data[i]['Average Rating'])
            st.write('--------------------------------------------------')
    
    with col3:
        for i in range(2, 50, 3):
            st.markdown(i+1)
            st.image(data[i]['Image'])
            st.write(data[i]['Title'])
            st.write('Author: ', data[i]['Author'])
            st.write('Number of Ratings:', data[i]['Ratings'])
            st.write('Average Rating:', data[i]['Average Rating'])
            st.write('--------------------------------------------------')
    

elif predict_option == 'Personalized Recommendations':
    st.subheader('Get Your Personal Book Recommendations Here:')
    book_name = st.text_input('Enter a Book Name: ')
    if book_name:
        index = int(np.where(pt.index == book_name)[0][0])
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:6]
    
        data = []
        for i in similar_items:
            item = []
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
    
            data.append(item)
        
        if st.button('Get Suggestions'):
            if len(data) >= 1:
                for i in range(len(data)):
                    st.image(data[i][2])
                    st.write(data[i][0])
                    st.write('Author: ', data[i][1])
                    st.write('--------------------------------------------------')
            else:
                st.markdown('No Suitable Recommendations for this book')
    