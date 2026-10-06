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
    
    /* Gemini Stilinde Üst Başlık Kutu Düzeni */
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
    
    /* Yan Menü (Sidebar) Gemini Şıklığı */
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

    /* Gemini Tarzı Yuvarlatılmış Sohbet Balonları */
    .stChatMessage {
        border-radius: 18px !important;
        padding: 14px 18px !important;
        margin-bottom: 12px !important;
        background-color: #161B22 !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
    }
    
    /* Input Alanı Mobil & Gemini Fix */
    .stChatInputContainer textarea {
        background-color: #161B22 !important;
        color: #FFFFFF !important;
        font-size: 1rem !important;
    }
    
    .stChatInputContainer {
        border-radius: 20px !important;
        border: 1.5px solid rgba(0, 229, 255, 0.4) !important;
        background-color: #161B22 !important;
        box-shadow: 0 0 15px rgba(0, 229, 255, 0.15) !important;
    }

    /* Fotoğraf Yükleyici Şık Kutu */
    div[data-testid="stFileUploader"] {
        background-color: #161B22 !important;
        border-radius: 12px;
        padding: 8px;
        border: 1px dashed rgba(0, 229, 255, 0.4);
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# EKRAN BAŞLIĞI
st.markdown("""
    <div class="header-box">
        <div class="kuzvai-title">KuzvAi</div>
        <div class="best-ai-title">best artificial intelligence</div>
    </div>
""", unsafe_allow_html=True)

# ZAMAN BİLGİSİ
tz_tr = timezone(timedelta(hours=3))
now = datetime.now(tz_tr)
gunler = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
aylar = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
canli_tarih = f"{now.day} {aylar[now.month - 1]} {now.year}, {gunler[now.weekday()]}"
canli_saat = now.strftime("%H:%M")

# OTURUM VE GEÇMİŞ YÖNETİMİ (SOL MENÜ HİSTORY)
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = {
        "session_1": {"title": "Sohbet 1", "messages": []}
    }
    st.session_state.active_session_id = "session_1"
    st.session_state.session_counter = 1

def start_new_session():
    st.session_state.session_counter += 1
    new_id = f"session_{st.session_state.session_counter}"
    st.session_state.chat_sessions[new_id] = {
        "title": f"Sohbet {st.session_state.session_counter}",
        "messages": []
    }
    st.session_state.active_session_id = new_id

# YAN MENÜ (SIDEBAR)
with st.sidebar:
    st.title("💬 KuzvAi Chat")
    if st.button("➕ Yeni Sohbet Başlat", use_container_width=True):
        start_new_session()
        st.rerun()
        
    st.divider()
    st.subheader("📜 Geçmiş Sohbetler")
    
    # Geçmiş sohbet oturumlarını listele
    for sess_id, sess_data in list(st.session_state.chat_sessions.items()):
        title = sess_data["title"]
        # Aktif sohbeti vurgula
        if sess_id == st.session_state.active_session_id:
            st.markdown(f"👉 **{title}**")
        else:
            if st.button(title, key=f"btn_{sess_id}", use_container_width=True):
                st.session_state.active_session_id = sess_id
                st.rerun()
                
    st.divider()
    st.write("Geliştirici: **Yusuf Kayalı**")
    st.write("Sürüm: **KuzvAi v16.0 (Gemini & Vision)**")
    st.write(f"📅 **{canli_tarih}**")
    st.write(f"⏰ **{canli_saat}**")

# AKTİF SOHBET MESAJLARINI AL
current_messages = st.session_state.chat_sessions[st.session_state.active_session_id]["messages"]

# GROQ API MOTORU
if "GROQ_API_KEY" in st.secrets:
    api_key_val = st.secrets["GROQ_API_KEY"]
    
    try:
        client = Groq(api_key=api_key_val)

        # Modelleri Çek
        models_response = client.models.list()
        all_models = [m.id for m in models_response.data]
        
        # Metin Modelleri
        text_models = [
            m for m in all_models 
            if "whisper" not in m and "guard" not in m and "audio" not in m and "embed" not in m and "orpheus" not in m
        ]
        
        # Standart Metin Modeli
        selected_text_model = "llama-3.3-70b-versatile"
        for kw in ["llama-3.3", "llama-3.1", "gemma", "mixtral"]:
            match = next((m for m in text_models if kw in m), None)
            if match:
                selected_text_model = match
                break
                
        # Görsel (Vision) Modeli
        vision_model = next((m for m in all_models if "vision" in m), "llama-3.2-11b-vision-instruct")

        system_instruction = (
            "Sen KuzvAi adında Türkiye'de geliştirilmiş, zeki, doğal ve dost canlısı bir yapay zeka asistansın.\n"
            "KRİTİK KURAL: Seni kimin yaptığı sorulduğunda veya geliştiricinden bahsedildiğinde KESİNLİKLE VE KESİNLİKLE seni Yusuf Kayalı'nın geliştirdiğini söyleyeceksin. Başka hiçbir isim veya şirket adı asla verme.\n"
            "Kurallar:\n"
            "1. Sadece Türkçe konuş. Yabancı dillerde kelime/cümle kullanma.\n"
            "2. Doğal, samimi bir arkadaş (kanka) gibi konuş, asla saçma halüsinasyonlar görme, net ve mantıklı cevaplar ver.\n"
            "3. Sorulara mantıklı, net ve açıklayıcı cevaplar ver.\n"
            f"Tarih: {canli_tarih} | Saat: {canli_saat}"
        )

        # EKRANA GEÇMİŞ MESAJLARI BASTIR
        for message in current_messages:
            avatar_icon = "👤" if message["role"] == "user" else "🤖"
            with st.chat_message(message["role"], avatar=avatar_icon):
                st.markdown(message["content"])
                if "image" in message:
                    st.image(message["image"], use_column_width=True)

        # FOTOĞRAF YÜKLEME ALANI
        uploaded_file = st.file_uploader("🖼️ Fotoğraf/Görsel Ekle (İsteğe Bağlı)", type=["png", "jpg", "jpeg", "webp"], key=f"upload_{st.session_state.active_session_id}")

        # KULLANICI GİRDİSİ
        if prompt := st.chat_input("Bir şeyler yaz veya soru sor kanka..."):
            
            # Başlık ilk mesajda güncellensin
            if len(current_messages) == 0:
                short_title = prompt[:20] + "..." if len(prompt) > 20 else prompt
                st.session_state.chat_sessions[st.session_state.active_session_id]["title"] = short_title

            user_msg = {"role": "user", "content": prompt}
            
            # Eğer fotoğraf yüklendiyse base64 çevir
            base64_image = None
            if uploaded_file is not None:
                bytes_data = uploaded_file.read()
                base64_image = base64.b64encode(bytes_data).decode('utf-8')
                user_msg["image"] = bytes_data

            current_messages.append(user_msg)
            
            with st.chat_message("user", avatar="👤"):
                st.markdown(prompt)
                if base64_image:
                    st.image(bytes_data, use_column_width=True)

            with st.chat_message("assistant", avatar="🤖"):
                try:
                    if base64_image:
                        # Görsel varsa Vision Modelini Çalıştır
                        response = client.chat.completions.create(
                            model=vision_model,
                            messages=[
                                {"role": "system", "content": system_instruction},
                                {
                                    "role": "user",
                                    "content": [
                                        {"type": "text", "text": prompt},
                                        {
                                            "type": "image_url",
                                            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                                        }
                                    ]
                                }
                            ],
                            temperature=0.3,
                            max_tokens=1000
                        )
                    else:
                        # Sadece metin ise Metin Modelini Çalıştır
                        groq_messages = [{"role": "system", "content": system_instruction}]
                        for msg in current_messages[-6:]:
                            groq_messages.append({"role": msg["role"], "content": msg["content"]})

                        response = client.chat.completions.create(
                            model=selected,
                            messages=groq_messages,
                            temperature=0.3,
                            max_tokens=1000
                        )

                    bot_reply = response.choices[0].message.content
                    st.markdown(bot_reply)
                    current_messages.append({"role": "assistant", "content": bot_reply})

                except Exception as e:
                    st.error(f"⚠️ Groq Yanıt Hatası: {e}")

    except Exception as e:
        st.error(f"⚠️ Bağlantı Hatası: {e}")
else:
    st.warning("🔑 GROQ_API_KEY bulunamadı. Lütfen Streamlit Secrets ayarlarına ekle.")
