import streamlit as st
from groq import Groq
from datetime import datetime, timedelta, timezone

# 1. SAYFA YAPILANDIRMASI (TAM EKRAN VE GENİŞ DÜZEN)
st.set_page_config(
    page_title="Yusuf AI",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. ÖZEL NEON, RGB VE SİBERPUNK CSS TASARIMI
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
        min-height: 90px !important;
        font-size: 1rem !important;
        color: #FFFFFF !important;
    }
    </style>
""", unsafe_allow_html=True)

# EKRAN BAŞLIĞI VE TASARIM
st.markdown("""
    <div class="header-box">
        <div class="yusuf-ai-title">Yusuf AI</div>
        <div class="naber-baby-title">naber baby</div>
    </div>
""", unsafe_allow_html=True)

# CANLI TARIH VE SAAT ENTEGRASYONU
tz_tr = timezone(timedelta(hours=3))
now = datetime.now(tz_tr)
gunler = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
aylar = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
canli_tarih = f"{now.day} {aylar[now.month - 1]} {now.year}, {gunler[now.weekday()]}"
canli_saat = now.strftime("%H:%M")

# YAN MENÜ VE KONTROLLER
with st.sidebar:
    st.header("⚙️ Sistem Paneli")
    st.write("Geliştirici: **Yusuf Kayalı**")
    st.write("Sürüm: **Yusuf AI v7.0 (Süper Zeka)**")
    st.write(f"📅 Tarih: **{canli_tarih}**")
    st.write(f"⏰ Saat: **{canli_saat}**")
    st.divider()
    if st.button("🧹 Sohbeti Sıfırla (Temizle)", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# CHAT VE YAPAY ZEKA MOTORU
if "GROQ_API_KEY" in st.secrets:
    api_key_val = st.secrets["GROQ_API_KEY"]
    
    if not api_key_val.startswith("gsk_"):
        st.error("🚨 **API Anahtarı Hatası:** Secrets içindeki anahtar `gsk_` ile başlamıyor!")
    else:
        try:
            client = Groq(api_key=api_key_val)

            if "messages" not in st.session_state:
                st.session_state.messages = []

            # DETAYLI VE ZENGİN KİŞİLİK / BİLGİ TALİMATI
            system_instruction = f"""
            Sen "Yusuf AI" adında son derece akıllı, geniş genel kültüre sahip, samimi, eğlenceli ve yardımsever bir yapay zeka asistansın.

            BİLGİ VE KİŞİLİK REHBERİ:
            1. YÜKSEK GENEL KÜLTÜR: OpenAI'ın ChatGPT'si, Anthropic'in Claude'u, Google Gemini, Groq altyapısı, yazılım dilleri (Python, JavaScript, HTML/CSS), bilgisayar donanımları, oyunlar (Valorant, Cyberpunk 2077 vb.), teknoloji ve günlük hayat hakkında eksiksiz bilgi sahibisin. Sana sorulan teknik veya genel sorulara doğru ve doyurucu cevaplar ver.
            2. SAMİMİ VE DOĞAL ÜSLUP: Kullanıcıya dostça, kanka üslubuyla hitap et. Ancak yapay ve abartılı sloganlar (her cümlenin başında 'naber baby', 'fişek gibiyiz' vb.) kullanma. Doğal bir arkadaş gibi konuş.
            3. DETAYLI VE AÇIKLAYICI YANITLAR: Sorulan soruları tek bir kelimeyle veya baştan savma geçiştirme. Adım adım, net, anlaşılır ve detaylı açıklamalar yap.
            4. BİLGİSAYAR VE DİL MANTIĞI: Kod örnekleri istendiğinde temiz ve doğru Python/Streamlit kodları sun.
            5. ZAMAN BİLGİSİ: Güncel tarih {canli_tarih}, saat {canli_saat}. Zamanla ilgili soruları buna göre yanıtla.

            Asla kendini tekrar etme, gereksiz saçmalama yapma. Her zaman kaliteli ve akıllı bir sohbet sun.
            """

            # GEÇMİŞ MESAJLARI EKRANA BASTIRMA
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
                        # Konuşma akışını korumak için son 6 mesajı hafızada tut
                        for msg in st.session_state.messages[-6:]:
                            groq_messages.append({"role": msg["role"], "content": msg["content"]})

                        # SADECE EN GÜÇLÜ SOHBET MODELLERİNİ DİNAMİK SEÇ
                        active_model = None
                        try:
                            raw_models = client.models.list().data
                            banned_keywords = ["guard", "whisper", "embed", "vision", "audio", "classify", "classifier", "orpheus"]
                            
                            valid_models = [
                                m.id for m in raw_models 
                                if "/" not in m.id and not any(b in m.id.lower() for b in banned_keywords)
                            ]
                            
                            # En akıllı modeller öncelikli
                            priority_list = [
                                "llama-3.3-70b-versatile",
                                "llama3-70b-8192",
                                "llama-3.1-8b-instant",
                                "gemma2-9b-it",
                                "mixtral-8x7b-32768"
                            ]
                            
                            for p in priority_list:
                                if p in valid_models:
                                    active_model = p
                                    break
                            
                            if not active_model and valid_models:
                                active_model = valid_models[0]
                        except Exception:
                            pass

                        if not active_model:
                            active_model = "llama-3.3-70b-versatile"

                        # YANIT LİMİTİNİ UZATTIK (max_tokens=1000)
                        stream = client.chat.completions.create(
                            model=active_model,
                            messages=groq_messages,
                            temperature=0.6,
                            frequency_penalty=0.4,
                            max_tokens=1000,
                            stream=True
                        )

                        def generate_reply():
                            full_response = ""
                            for chunk in stream:
                                if chunk.choices[0].delta.content:
                                    text_chunk = chunk.choices[0].delta.content
                                    full_response += text_chunk
                                    yield text_chunk
                            st.session_state.temp_full_reply = full_response

                        bot_reply = st.write_stream(generate_reply())
                        
                        if "temp_full_reply" in st.session_state:
                            st.session_state.messages.append({"role": "assistant", "content": st.session_state.temp_full_reply})
                            del st.session_state.temp_full_reply

                    except Exception as e:
                        st.error(f"⚠️ Yusuf AI Hatası: {e}")

        except Exception as e:
            st.error(f"⚠️ Bağlantı Hatası: {e}")
else:
    st.warning("🔑 GROQ_API_KEY bulunamadı. Lütfen Streamlit Secrets ayarlarına ekle.")
