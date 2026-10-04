import streamlit as st
from openai import OpenAI
from datetime import datetime, timedelta, timezone

# 1. MOBİL UYUMLU SAYFA
st.set_page_config(
    page_title="Yusuf'un Yapay Zekası",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. ARAYÜZ TASARIMI
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp {
        background-color: #0B0F19;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    
    .main-title {
        text-align: center;
        color: #00E676;
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: -10px;
        text-shadow: 0px 2px 4px rgba(0, 230, 118, 0.3);
    }
    
    .sub-title {
        text-align: center;
        color: #94A3B8;
        font-size: 1rem;
        margin-bottom: 30px;
    }
    
    .stChatMessage {
        border-radius: 18px;
        padding: 5px 15px;
        margin-bottom: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">Yusuf\'un Yapay Zekası 🤖</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Net Yanıtlar. Sınırsız Zeka.</div>', unsafe_allow_html=True)

# 3. ZAMAN BİLGİSİ
tz_tr = timezone(timedelta(hours=3))
now = datetime.now(tz_tr)
gunler = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
aylar = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
canli_tarih = f"{now.day} {aylar[now.month - 1]} {now.year}, {gunler[now.weekday()]}"
canli_saat = now.strftime("%H:%M")

with st.sidebar:
    st.header("⚙ Ayarlar")
    st.write("Geliştirici: **Yusuf Kayalı**")
    st.write("Altyapı: **ChatGPT (OpenAI)**")
    st.divider()
    if st.button("🧹 Yeni Sohbet Başlat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

if "OPENAI_API_KEY" in st.secrets:
    try:
        # OpenAI İstemcisini Başlatma
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            avatar_icon = "👤" if message["role"] == "user" else "🤖"
            with st.chat_message(message["role"], avatar=avatar_icon):
                st.markdown(message["content"])

        if prompt := st.chat_input("Mesajını buraya yaz..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user", avatar="👤"):
                st.markdown(prompt)

            with st.chat_message("assistant", avatar="🤖"):
                
                system_instruction = f"""
                Senin adın "Yusuf'un Yapay Zekası"sın. Seni kodlayan kişi "Yusuf Kayalı"dır.
                Sen Yusuf DEĞİLSİN, onun yarattığı asistansın.
                
                ZAMAN: {canli_tarih} - Saat: {canli_saat}
                
                KESİN KURALLAR:
                1. ASLA saçmalama, kelimeleri yarıda kesme. Kusursuz Türkçe kullan.
                2. SADECE 1 VEYA 2 CÜMLE YAZ. Uzun destanlar yazmak kesinlikle yasak.
                3. Ne sorulursa sorulsun sadede gel, lafı uzatma.
                """

                # OpenAI mesaj formatını hazırlıyoruz (Geçmiş sohbeti de dahil eder)
                openai_messages = [{"role": "system", "content": system_instruction}]
                for msg in st.session_state.messages:
                    openai_messages.append({"role": msg["role"], "content": msg["content"]})

                try:
                    # ChatGPT'nin en hızlı ve akıllı ekonomik modeli: gpt-4o-mini
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=openai_messages,
                        temperature=0.3,
                        max_tokens=300
                    )

                    bot_reply = response.choices[0].message.content

                    if bot_reply and str(bot_reply).strip():
                        st.markdown(bot_reply)
                        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
                    else:
                        st.error("⚠️ Model boş yanıt döndürdü.")

                except Exception as api_err:
                    st.error(f"⚠️ OpenAI API Hatası: {api_err}")

    except Exception as e:
        st.error(f"⚠️ Kritik Hata: {e}")
else:
    st.warning("🔑 OPENAI_API_KEY henüz tanımlanmamış. Lütfen Streamlit Secrets ayarlarına anahtarını ekle.")
