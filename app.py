import streamlit as st
from groq import Groq
from datetime import datetime, timedelta, timezone

st.set_page_config(
    page_title="Yusuf'un Yapay Zekası",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

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

                # Canlı tarama ve %100 sağlam Llama modeli garantisi
                try:
                    models_info = client.models.list().data
                    available_models = [m.id for m in models_info]
                    
                    candidate_models = []
                    for m in available_models:
                        name = m.lower()
                        # Sadece güncel Llama serisini al, çöpleri ve deaktifleri ele
                        if "llama-3.3" in name or "llama-3.1-70b" in name or "llama-3" in name:
                            if not any(bad in name for bad in ["guard", "whisper", "vision", "classify", "embed", "tool", "decommissioned"]):
                                candidate_models.append(m)
                    
                    # Eğer dinamik listede çıkmazsa direkt en sağlam güncel ID'yi daya
                    if not candidate_models:
                        candidate_models = ["llama-3.3-70b-versatile"]
                except Exception:
                    candidate_models = ["llama-3.3-70b-versatile"]

                bot_reply = None
                last_error = "Model yanıt üretemedi."

                for model_name in candidate_models:
                    try:
                        def generate_stream():
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

                        reply = st.write_stream(generate_stream())
                        
                        if reply and str(reply).strip():
                            bot_reply = reply
                            break
                    except Exception as err:
                        last_error = err
                        continue

                if bot_reply:
                    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
                else:
                    st.error(f"⚠️ Bağlantı Hatası: {last_error}")

    except Exception as e:
        st.error(f"⚠️ Kritik Hata: {e}")
else:
    st.warning("🔑 GROQ_API_KEY henüz tanımlanmamış. Lütfen Streamlit Secrets ayarlarını kontrol et.")
