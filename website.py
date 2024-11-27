import google.generativeai as genai
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import streamlit as st
import pandas as pd
import requests
import os

load_dotenv()
BOT_TOKEN = '7956922025:AAFh9rz6T45IFdKTN-nQOUhtgrXTeueAAFw'
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"
API_KEY = os.getenv("API_KEY")
genai.configure(api_key=API_KEY)


def send_message(message):
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {
        "chat_id": '1317717099',
        "text": message
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print("Message sent successfully!")
    except requests.exceptions.RequestException as e:
        print(f"Error sending message: {e}")


def summarize_text(text):
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    prompt = "Summarize the given text in detail in para form"
    response = model.generate_content([prompt, text])
    return response.text

def main():
    st.title("Hello !!!")

    url1 = st.text_input("Enter url1")
    url2 = st.text_input("Enter url2")
    url3 = st.text_input("Enter url3")
    url4 = st.text_input("Enter url4")
    url5 = st.text_input("Enter url5")
    
    inputs = [url1, url2, url3, url4, url5]
    if(st.button("Submit")):
        for link in inputs: 
            req = requests.get(link)
            article = BeautifulSoup(req.content, "html.parser")
            page_text = article.get_text()
            clean_text = ' '.join(page_text.split())
            text = summarize_text(clean_text)
            st.write(text)
            send_message(text)
    
main()

# streamlit run .\website.py
# https://gov.optimism.io/t/how-to-stay-up-to-date/6124
# https://gov.optimism.io/t/how-to-navigate-the-forum/6120
# https://gov.optimism.io/t/about-the-optimism-collective/6118
# https://gov.optimism.io/t/working-constitution-of-the-optimism-collective/55
# https://gov.optimism.io/t/governance-season-guides/6122
