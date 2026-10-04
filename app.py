import streamlit as st
from groq import Groq
from datetime import datetime, timedelta, timezone

# 1. PLAY STORE İÇİN MOBİL UYUMLU SAYFA YAPILANDIRMASI
st.set_page_config(
    page_title="Yusuf'un Yapay Zekası",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. PROFESYONEL UYGULAMA ARAYÜZÜ (CSS - Özel Tasarım)
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

# 3. CANLI TARİH VE SAAT (Türkiye)
tz_tr = timezone(timedelta(hours=3))
now = datetime.now(tz_tr)
gunler = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
aylar = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
canli_tarih = f"{now.day} {aylar[now.month - 1]} {now.year}, {gunler[now.weekday()]}"
canli_saat = now.strftime("%H:%M")

with st.sidebar:
    st.header("⚙️ Ayarlar")
    st.write("Geliştirici: **Yusuf Kayalı**")
    st.divider()
    if st.button("🧹 Yeni Sohbet Başlat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

if "GROQ_API_KEY" in st.secrets:
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])

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
                
                # SIKI YÖNETİM TALİMATLARI
                system_prompt = f"""
                Senin adın "Yusuf'un Yapay Zekası"sın. Seni kodlayan kişi "Yusuf Kayalı"dır.
                Sen Yusuf DEĞİLSİN, onun yarattığı asistansın.
                
                ZAMAN: {canli_tarih} - Saat: {canli_saat}
                
                KESİN KURALLAR:
                1. ASLA saçmalama, anlamsız kelime üretme. Kusursuz Türkçe kullan.
                2. SADECE 1 VEYA 2 CÜMLE YAZ. Uzun destanlar yazmak kesinlikle yasak.
                3. Ne sorulursa sorulsun sadede gel, lafı uzatma.
                """

                chat_messages = [{"role": "system", "content": system_prompt}]
                for msg in st.session_state.messages:
                    chat_messages.append({"role": msg["role"], "content": msg["content"]})

                # SADECE EN SAĞLAM VE ZEKİ MODELLER (Saçmalama İhtimali %0)
                try:
                    live_models = [m.id for m in client.models.list().data]
                    guvenli_modeller = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "gemma2-9b-it"]
                    candidate_models = [m for m in guvenli_modeller if m in live_models]
                    
                    if not candidate_models: # Eğer 3'ü de yoksa en güvenli yedeğe geç
                        candidate_models = ["llama-3.1-8b-instant"]
                except Exception:
                    candidate_models = ["llama-3.3-70b-versatile"]

                bot_reply = None
                last_error = None

                for model_name in candidate_models:
                    try:
                        def generate_stream():
                            # temperature=0.3 -> Ciddiyet ayarı (halüsinasyonu önler)
                            # max_tokens=150 -> Uzun yazmasını fiziksel olarak engeller
                            response = client.chat.completions.create(
                                model=model_name,
                                messages=chat_messages,
                                stream=True,
                                temperature=0.3,
                                max_tokens=150
                            )
                            for chunk in response:
                                if chunk.choices and len(chunk.choices) > 0:
                                    content = chunk.choices[0].delta.content
                                    if content:
                                        yield content

                        bot_reply = st.write_stream(generate_stream())
                        if bot_reply:
                            break
                    except Exception as err:
                        last_error = err
                        continue

                if bot_reply:
                    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
                else:
                    st.error(f"⚠️ Hata Oluştu: Lütfen sayfayı yenileyin. Detay: {last_error}")

    except Exception as e:
        st.error(f"⚠️ Kritik Hata: {e}")
else:
    st.warning("🔑 GROQ_API_KEY henüz tanımlanmamış. Lütfen Streamlit Secrets ayarlarını kontrol et.")
