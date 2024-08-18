import streamlit as st
import pickle
import re
import numpy as np
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
port_stem = PorterStemmer()
import time
from pygoogletranslation import Translator
import nltk
import ssl
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
nltk.download('stopwords')

# from_email = "hamidrezabahrami455@gmail.com"
# to_email = "hamidr.bahraami@gmail.com"
# email_password = "htth eind kniy bgst"

# context = ssl.create_default_context()

st.set_page_config(page_title='جوانی جمعیت / تکریم سالمندان - RoboAi', layout='centered', page_icon='🩺')

vectory = pickle.load(open('vectory.pkl', 'rb'))
load_modely = pickle.load(open('modely.pkl', 'rb'))

translator = Translator()

def stemming(content):
  con = re.sub('[^a-zA-Z]', ' ', content)
  con = con.lower()
  con = con.split()
  con = [port_stem.stem(word) for word in con if not word in stopwords.words('english')]
  con = ' '.join(con)
  return con

def thoughty(text):
  text = stemming(text)
  input_text = [text]
  vector1 = vectory.transform(input_text)
  prediction = load_modely.predict(vector1)
  return prediction

def show_page():
    st.write("<h3 style='text-align: center; color: blue;'>سامانه تشخیص زوال عقل و آلزایمر سالمندان 🩺</h3>", unsafe_allow_html=True)
    st.write("<h5 style='text-align: center; color: gray;'>Robo-Ai.ir طراحی شده توسط</h5>", unsafe_allow_html=True)
    st.link_button("Robo-Ai بازگشت به", "https://robo-ai.ir")
    with st.sidebar:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(' ')
        with col2:
            st.image('img.png')
        with col3:
            st.write(' ')
        st.divider()
        st.write("<h4 style='text-align: center; color: black;'>تشخیص زوال عقل یا دمانس زودرس</h4>", unsafe_allow_html=True)
        st.write("<h4 style='text-align: center; color: gray;'>با تحلیل متن کاربر</h4>", unsafe_allow_html=True)
        st.divider()
        st.write("<h5 style='text-align: center; color: black;'>طراحی و توسعه</h5>", unsafe_allow_html=True)
        st.write("<h5 style='text-align: center; color: black;'>حمیدرضا بهرامی</h5>", unsafe_allow_html=True)


    container = st.container(border=True)
    container.write("<h6 style='text-align: right; color: gray;'>تشخیص آلزایمر و زوال عقل زودرس از متن 💬</h6>", unsafe_allow_html=True)
    container.write("<h6 style='text-align: right; color: gray;'>.برای افزایش دقت تحلیل سامانه ، توسط اطرافیان شخص سالمند پاسخ داده شود ⚠️</h6>", unsafe_allow_html=True)
    container.write("<h6 style='text-align: right; color: gray;'>.علائم شخص سالمند موردنظر را در یک پاراگراف توصیف کنید 🗨️</h6>", unsafe_allow_html=True)
    
    text_3 = st.text_area('شخص سالمند موردنظر اغلب چه رفتارهایی از خود بروز می دهد؟',height=None,max_chars=None,key=None)

    button_3 = st.button('ارزیابی علائم')
    if button_3:
        if text_3 == "":
            with st.chat_message("assistant"):
                with st.spinner('''درحال بررسی'''):
                    time.sleep(1)
                    st.success(u'\u2713''تحلیل انجام شد')
                    text1 = 'لطفا متن را وارد کنید'
                    def stream_data1():
                        for word in text1.split(" "):
                            yield word + " "
                            time.sleep(0.09)
                    st.write_stream(stream_data1)
    
        
        else:
            out = translator.translate(text_3)
            prediction_class = thoughty(out.text)
            if prediction_class == [1]:
                with st.chat_message("assistant"):
                    with st.spinner('''درحال بررسی'''):
                        time.sleep(1)
                        st.success(u'\u2713''تحلیل انجام شد')
                        text1 = 'بر اساس تحلیل من ، علائمی از آلزایمر و زوال عقل در شخص موردنظر دیده می شود'
                        text2 = 'برای بررسی دقیق تر و کنترل بهتر علائم پیش رونده ، به پزشک مراجعه کنید'
                        def stream_data1():
                            for word in text1.split(" "):
                                yield word + " "
                                time.sleep(0.09)
                        st.write_stream(stream_data1)
                        def stream_data2():
                            for word in text2.split(" "):
                                yield word + " "
                                time.sleep(0.09)
                        st.write_stream(stream_data2)

            else:
                with st.chat_message("assistant"):
                    with st.spinner('''درحال بررسی'''):
                        time.sleep(1)
                        st.success(u'\u2713''تحلیل انجام شد')
                        text3 = 'بر اساس تحلیل من ، علائمی از آلزایمر و زوال عقل در شخص موردنظر دیده نمی شود'
                        def stream_data3():
                            for word in text3.split(" "):
                                yield word + " "
                                time.sleep(0.09)
                        st.write_stream(stream_data3)

    else:
        pass

show_page()
