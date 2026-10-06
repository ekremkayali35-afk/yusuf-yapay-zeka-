import streamlit as st
import base64
from groq import Groq
from datetime import datetime, timedelta, timezone

# 1. SAYFA YAPILANDIRMASI
st.set_page_config(
    page_title="KuzvAi",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 2. MOBİL UYUMLU & GEMİNİ STİLİ SİBERPUNK CSS
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Mobil Ve Bütün Ekranlar İçin Temiz Karanlık Arka Plan */
    .stApp {
        background-color: #0D1117 !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        color: #E6EDF3 !important;
    }
    
    /* Mobil Yazı Görünürlüğü Fix: Tüm Metin Elemanlarını Açık Renk Yap */
    p, span, label, h1, h2, h3, h4, h5, h6, div, input, textarea, .stMarkdown {
        color: #E6EDF3 !important;
    }
    
    @keyframes rgbGlow {
        0% { color: #FF0055; text-shadow: 0 0 12px rgba(255, 0, 85, 0.8); }
        33% { color: #00E5FF; text-shadow: 0 0 12px rgba(0, 229, 255, 0.8); }
        66% { color: #00FF66; text-shadow: 0 0 12px rgba(0, 255, 102, 0.8); }
        100% { color: #FF0055; text-shadow: 0 0 12px rgba(255, 0, 85, 0.8); }
    }
    
    .header-box {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid rgba(0, 229, 255, 0.2);
        padding: 10px 5px 15px 5px;
        margin-bottom: 20px;
    }
    
    .kuzvai-title {
        font-size: 2.2rem;
        font-weight: 900;
        animation: rgbGlow 4s infinite linear;
        margin: 0;
        letter-spacing: 1px;
    }
    
    .best-ai-title {
        font-size: 0.9rem;
        font-weight: 600;
        color: #00E5FF !important;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1.2px;
    }
    
    section[data-testid="stSidebar"] {
        background-color: #161B22 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    }
    
    section[data-testid="stSidebar"] button {
        border-radius: 12px !important;
        border: 1px solid rgba(0, 229, 255, 0.3) !important;
        background-color: #21262D !important;
        color: #00E5FF !important;
        font-weight: 600 !important;
        transition: all 0.2s ease;
    }
    
    section[data-testid="stSidebar"] button:hover {
        background-color: #00E5FF !important;
        color: #0D1117 !important;
        border-color: #00E5FF !important;
    }

    .stChatMessage {
        border-radius: 18px !important;
        padding: 14px 18px !important;
        margin-bottom: 12px !important;
        background-color: #161B22 !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
    }
    
    .stChatInputContainer textarea {
        background-color: #16
