import streamlit as st
import google.generativeai as genai
from datetime import datetime, timedelta, timezone

# 1. SAYFA YAPILANDIRMASI
st.set_page_config(
    page_title="Yusuf AI - Gemini",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. NEON VE SİBERPUNK CSS TASARIMI
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp {
        background-color: #0B0F19;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    
    @keyframes rgbGlow {
        0% { color: #FF0055; text-shadow: 0 0 15px rgba(255, 0, 85, 0.9); }
        25% { color: #00E5FF; text-shadow: 0 0 15px rgba(0, 229, 255, 0.9); }
        50% { color: #00FF66; text-shadow: 0 0 15px rgba(0, 255, 102, 0.9); }
        75% { color: #FFBB00; text-shadow: 0 0 15px rgba(255, 187, 0, 0.9); }
        100% { color: #FF0055; text-shadow: 0 0 15px rgba(255, 0, 85, 0.9); }
    }
    
    .header-box {
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
        border-bottom: 2px solid #00E5FF;
        padding-bottom: 14px;
        margin-bottom: 25px;
        box-shadow: 0px 8px 20px rgba(0, 229, 255, 0.3);
    }
    
    .yusuf-ai-title {
        font-size: 3rem;
        font-weight: 900;
        animation: rgbGlow 3s infinite linear;
        margin: 0;
        line-height: 1;
        letter-spacing: 1.5px;
    }
    
    .naber-baby-title {
        font-size: 1.5rem;
        font-weight: 800;
        color: #FF007F;
        text-shadow: 0 0 10px rgba(255, 0, 127, 0.7);
        margin: 0;
        letter-spacing: 0.5px;
    }
    
    .stChatMessage {
        border-radius: 18px;
        padding: 12px 18px;
        margin-bottom: 14px;
        background-color: #161F30;
        border: 1px solid #2A364F;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        color: #E2E8F0;
        font-size: 1.05rem;
        line-height: 1.6;
    }
    
    .stChatInputContainer {
        border-radius: 20px !important;
        border: 2px solid #00E5FF !important;
        box-shadow: 0 0 15px rgba(0, 229, 255, 0.4) !important;
        background-color: #111827 !important;
    }
    
    .stChatInputContainer textarea {
        min-height: 80px !important;
        font-size: 1rem !important;
        color: #FFFFFF !important;
    }
    </style>
""", unsafe_allow_html=True)

# EKRAN BAŞLIĞI
st.markdown("""
    <div class="header-box">
        <div class="yusuf-ai-title">Yusuf AI</div>
        <div class="naber-baby-title">naber baby</div>
    </div>
""", unsafe_allow_html=True)

# ZAMAN BİLGİSİ
tz_tr = timezone(timedelta(hours=3))
now = datetime.now(tz_tr)
gunler = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
aylar = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
canli_tarih = f"{now.day} {aylar[now.month - 1]} {now.year}, {gunler[now.weekday()]}"
canli_saat = now.strftime("%H:%M")

# YAN MENÜ
with st.sidebar:
    st.header("⚙ Sistem Paneli")
    st.write("Geliştirici: **Yusuf Kayalı**")
    st.write("Sürüm: **Yusuf AI v10.1 (Gemini Güncel)**")
    st.write(f"📅 Tarih: **{canli_tarih}**")
    st.write(f"⏰ Saat: **{canli_saat}**")
    st.divider()
    if st.button("🧹 Sohbeti Sıfırla (Temizle)", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# GEMINI API MOTORU
if "GEMINI_API_KEY" in st.secrets:
    api_key_val = st.secrets["GEMINI_API_KEY"]
    
    try:
        genai.configure(api_key=api_key_val)
        
        # En güncel ve stabil çalışan Gemini flash modeli
        model = genai.GenerativeModel('gemini-2.5-flash')

        if "messages" not in st.session_state:
            st.session_state.messages = []

        system_instruction_text = f"""
        Sen Yusuf AI adında Türkiye'de geliştirilmiş, zeki, doğal ve dost canlısı bir yapay zeka asistansın.
        Kurallar:
        1. Sadece Türkçe konuş.
        2. Samimi, doğal bir arkadaş gibi konuş, saçma döngülere asla girme.
        3. Sorulara net, mantıklı ve açıklayıcı yanıtlar ver.
        Tarih: {canli_tarih} | Saat: {canli_saat}
        """

        # GEÇMİŞ MESAJLARI EKRANA BASTIR
        for message in st.session_state.messages:
            avatar_icon = "👤" if message["role"] == "user" else "🤖"
            with st.chat_message(message["role"], avatar=avatar_icon):
                st.markdown(message["content"])

        # KULLANICI GİRDİSİ
        if prompt := st.chat_input("İstediğin konuyu sor kanka..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user", avatar="👤"):
                st.markdown(prompt)

            with st.chat_message("assistant", avatar="🤖"):
                try:
                    gemini_history = []
                    for msg in st.session_state.messages[:-1]:
                        role_mapping = "user" if msg["role"] == "user" else "model"
                        gemini_history.append({"role": role_mapping, "parts": [msg["content"]]})

                    chat = model.start_chat(history=gemini_history)
                    
                    full_prompt = f"{system_instruction_text}\n\nKullanıcı: {prompt}"
                    
                    response = chat.send_message(full_prompt)
                    bot_reply = response.text

                    st.markdown(bot_reply)
                    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

                except Exception as e:
                    st.error(f"⚠️ Gemini Yanıt Hatası: {e}")

    except Exception as e:
        st.error(f"⚠️ Gemini Bağlantı Hatası: {e}")
else:
    st.warning("🔑 GEMINI_API_KEY bulunamadı. Lütfen Streamlit Secrets ayarlarına ekle.")
