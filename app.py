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
    /* Streamlit'in varsayılan menülerini ve yazılarını gizle (Gerçek uygulama hissi) */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Arka plan ve genel font ayarları */
    .stApp {
        background-color: #0B0F19;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Başlık stili */
    .main-title {
        text-align: center;
        color: #00E676;
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: -10px;
        text-shadow: 0px 2px 4px rgba(0, 230, 118, 0.3);
    }
    
    /* Alt başlık stili */
    .sub-title {
        text-align: center;
        color: #94A3B8;
        font-size: 1rem;
        margin-bottom: 30px;
    }
    
    /* Chat balonları genel tasarımı */
    .stChatMessage {
        border-radius: 18px;
        padding: 5px 15px;
        margin-bottom: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# Başlık Kısmı
st.markdown('<div class="main-title">Yusuf\'un Yapay Zekası 🤖</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Sınırsız Zeka. Net Yanıtlar. Her Şeyi Bilir.</div>', unsafe_allow_html=True)

# 3. CANLI TARİH VE SAAT HESAPLAMA (Türkiye Saat Dilimi)
tz_tr = timezone(timedelta(hours=3))
now = datetime.now(tz_tr)

gunler = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
aylar = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
bugun_gun = gunler[now.weekday()]
bugun_ay = aylar[now.month - 1]
canli_tarih = f"{now.day} {bugun_ay} {now.year}, {bugun_gun}"
canli_saat = now.strftime("%H:%M")

# 4. YAN MENÜ (Sohbeti Temizleme)
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

        # Eski mesajları ekrana bas
        for message in st.session_state.messages:
            avatar_icon = "👤" if message["role"] == "user" else "🤖"
            with st.chat_message(message["role"], avatar=avatar_icon):
                st.markdown(message["content"])

        if prompt := st.chat_input("Mesajını veya sorunu buraya yaz..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user", avatar="👤"):
                st.markdown(prompt)

            with st.chat_message("assistant", avatar="🤖"):
                
                # 5. GÜNCELLENMİŞ ULTRA ZEKA TALİMATI (Kısa Yanıt Odaklı)
                system_prompt = f"""
                Senin adın "Yusuf'un Yapay Zekası". Sen dünyanın en gelişmiş ve akıllı asistanısın. 
                Seni yaratan kişi "Yusuf Kayalı"dır. Başka kurumları (Google, OpenAI, Meta vb.) asla anma.
                
                ZAMAN BİLGİSİ:
                Şu anki tarih: {canli_tarih}
                Şu anki saat: {canli_saat}
                
                YANIT TARZI VE UZUNLUĞU (ÇOK ÖNEMLİ):
                Yanıtlarını HER ZAMAN KISA, ÖZ VE NET tut. Kullanıcı özellikle "bana uzun uzun anlat" demedikçe asla uzun paragraflar yazma.
                Destan yazmaktan kaçın, lafı dolandırma, direkt sadede gel. Bir insanla mesajlaşıyormuş gibi doğal ve pratik ol.
                
                GENEL KÜLTÜR VE MANTIK:
                Türk kültürüne, bilmecelere hakimsin ("Pazardan aldım 1 tane eve geldim 1000 tane" -> "Nar" gibi).
                Ansiklopedik, sıkıcı ve robotik dersler verme. Her soruyu zekice ve en kestirme yoldan çöz.
                """

                chat_messages = [{"role": "system", "content": system_prompt}]

                for msg in st.session_state.messages:
                    chat_messages.append({"role": msg["role"], "content": msg["content"]})

                # 6. DİNAMİK MODEL ÇEKİCİ
                try:
                    models_list = client.models.list()
                    candidate_models = [
                        m.id for m in models_list.data 
                        if "whisper" not in m.id and "guard" not in m.id and "safetensors" not in m.id and "llava" not in m.id
                    ]
                except Exception:
                    candidate_models = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"]

                bot_reply = None
                last_error = None

                for model_name in candidate_models:
                    try:
                        # 7. CANLI YAZMA EFEKTİ
                        def generate_stream():
                            response = client.chat.completions.create(
                                model=model_name,
                                messages=chat_messages,
                                stream=True
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
