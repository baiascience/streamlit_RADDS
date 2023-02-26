#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st

import requests
from streamlit_lottie import st_lottie

from PIL import Image

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

#Use local CSS

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)




# In[4]:


st.set_page_config(page_title="My webpage", page_icon=":smile:", layout="wide")

local_css("style/style.css")


# In[7]:

#--- LOAD ASSETS

supplychain_image = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_quxomsbr.json")
dice_image=Image.open("images/dice.jpg")

#---- HEADER SECTION-----
with st.container():

    st.subheader("Hi, I am Mathew :smile:")
    st.title("A Data Analyst from Brazil")
    st.write("I am passionate about findyins ways to use Python")
    st.write("[Learn More Clicking Here >](https://medium.com/@baia-science)")

with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        st.write(
        """
        There's no need to spend days or weeks building a website anymore. In this video, 
        I'm going to show you how to build a website with a blog and a contact page in only 12 minutes using Python, 
        Streamlit and other open-source tools."""
        )

with right_column:
    st_lottie(supplychain_image, height =300, key="Supply chain")

# PROJECTS

with st.container():
    st.write("---")
    st.header("My Projects")
    st.write("##")
    image_column, text_column = st.columns((1,2))
    with image_column:
        st.image(dice_image,width=400)
    with text_column:
        st.subheader("Main Project")
        st.write(
            " Learn how to use lottie files in streamlit"
        )
        st.markdown("[Watch Video...](https://www.youtube.com/watch?v=VqgUkExPvLY)")

 
#---- CONTACT -----

with st.container():
    st.write("---")
    st.header("Get in Touch with me!")
    st.write("##")

    contact_form = """
    <form action="https://formsubmit.co/matheusblqueiroz@gmail.com" method="POST">    
        <input type="hidden" name ="_captcha" value ="false">
        <input type="text" name="name" placeholder="Your name" required>
        <input type="email" name="email" placeholder = "Your email" required>
        <textarea name="message" placeholder="Your message here" required></textarea>
        <button type="submit">Send</button>
    </form>
    
    """

    left_column , right_column = st.columns(2)
    with left_column:
        st.markdown(contact_form, unsafe_allow_html=True)
    with right_column:
        st.empty()

     
    




