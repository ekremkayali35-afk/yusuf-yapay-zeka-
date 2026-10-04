import streamlit as st
from groq import Groq
from datetime import datetime, timedelta, timezone

# 1. SAYFA YAPILANDIRMASI
st.set_page_config(
    page_title="Yusuf AI - Groq",
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
    st.write("Sürüm: **Yusuf AI v14.0 (Dinamik Model Bulucu)**")
    st.write(f"📅 Tarih: **{canli_tarih}**")
    st.write(f"⏰ Saat: **{canli_saat}**")
    st.divider()
    if st.button("🧹 Sohbeti Sıfırla (Temizle)", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# GROQ API MOTORU VE DİNAMİK MODEL BULUCU
if "GROQ_API_KEY" in st.secrets:
    api_key_val = st.secrets["GROQ_API_KEY"]
    
    try:
        client = Groq(api_key=api_key_val)

        # Groq'un o an hesabına verdiği TÜM modelleri çek ve text dışı olanları ele
        models_response = client.models.list()
        all_models = [m.id for m in models_response.data]
        
        # Sadece metin tabanlı ve temiz modelleri filtrele
        valid_models = [
            m for m in all_models 
            if "whisper" not in m 
            and "guard" not in m 
            and "audio" not in m 
            and "embed" not in m
            and "orpheus" not in m
        ]
        
        # Öncelikli olarak llama veya gemma içerenleri seç
        selected_model = None
        for keyword in ["llama", "gemma", "mixtral"]:
            match = next((m for m in valid_models if keyword in m), None)
            if match:
                selected_model = match
                break
                
        # Hiçbiri bulunamazsa listedeki ilk modeli al
        if not selected_model and valid_models:
            selected_model = valid_models[0]
        elif not selected_model:
            selected_model = "llama-3.3-70b-versatile" # Son yedek

        if "messages" not in st.session_state:
            st.session_state.messages = []

        system_instruction = f"""
        Sen Yusuf AI adında Türkiye'de geliştirilmiş, zeki, doğal ve dost canlısı bir yapay zeka asistansın.
        KRİTİK KURAL: Seni kimin yaptığı sorulduğunda veya geliştiricinden bahsedildiğinde KESİNLİKLE VE KESİNLİKLE seni **Yusuf Kayalı**'nın geliştirdiğini söyleyeceksin. Başka hiçbir isim veya şirket adı asla verme.
        Kurallar:
        1. Sadece Türkçe konuş. Yabancı dillerde kelime/cümle kullanma.
        2. Doğal, samimi bir arkadaş (kanka) gibi konuş, asla saçma halüsinasyonlar görme, net ve mantıklı cevaplar ver.
        3. Sorulara mantıklı, net ve açıklayıcı cevaplar ver.
        Tarih: {canli_tarih} | Saat: {canli_saat}
        """
        Kurallar:
        1. Sadece Türkçe konuş. Yabancı dillerde kelime/cümle kullanma.
        2. Doğal, samimi bir arkadaş (kanka) gibi konuş, asla saçma halüsinasyonlar görme, net ve mantıklı cevaplar ver.
        3. Sorulara mantıklı, net ve açıklayıcı cevaplar ver.
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
                    groq_messages = [{"role": "system", "content": system_instruction}]
                    for msg in st.session_state.messages[-6:]:
                        groq_messages.append({"role": msg["role"], "content": msg["content"]})

                    response = client.chat.completions.create(
                        model=selected_model,
                        messages=groq_messages,
                        temperature=0.3,
                        max_tokens=1000
                    )

                    bot_reply = response.choices[0].message.content
                    st.markdown(bot_reply)
                    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

                except Exception as e:
                    st.error(f"⚠️ Groq Yanıt Hatası: {e}")

    except Exception as e:
        st.error(f"⚠️ Bağlantı Hatası: {e}")
else:
    st.warning("🔑 GROQ_API_KEY bulunamadı. Lütfen Streamlit Secrets ayarlarına ekle.")
