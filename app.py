import streamlit as st
from groq import Groq

# Sayfa Yapılandırması
st.set_page_config(
    page_title="Yusuf'un Yapay Zekası",
    page_icon="🤖",
    layout="wide"
)

# Özel Arayüz Tasarımı (CSS)
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stChatMessage {
        border-radius: 12px;
        padding: 10px;
        margin-bottom: 10px;
    }
    .stTitle {
        color: #4CAF50;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 Yusuf'un Yapay Zekası")
st.write("Süper hızlı ve akıllı yapay zeka asistanı. Dilediğin soruyu veya bilmeceyi sorabilirsin!")

if "GROQ_API_KEY" in st.secrets:
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])

        # Yan Menü (Sidebar)
        with st.sidebar:
            st.header("⚙️ Kontrol Paneli")
            st.write("Geliştirici: **Yusuf Kayalı**")
            st.write("Altyapı: **Groq Ultra-Fast AI**")
            st.divider()
            if st.button("🗑️ Sohbeti Sıfırla", use_container_width=True):
                st.session_state.messages = []
                st.rerun()

        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Eski mesajları ekrana bas
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Bir şeyler yaz veya bir bilmece sor..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                # Güçlendirilmiş Zeka ve Kültür Talimatı
                chat_messages = [
                    {
                        "role": "system",
                        "content": (
                            "Sen 'Yusuf'un Yapay Zekası' adında son derece akıllı, mantıklı ve kıvrak zekalı bir asistansın. "
                            "Türk kültürüne, bilmecelere (örneğin 'Pazardan aldım 1 tane, eve geldim 1000 tane' sorusunun cevabının 'Nar' olduğunu bilirsin), esprilere ve deyimlere tam hakimsin. "
                            "Bilmeceleri doğrudan mantığınla doğru cevaplarsın, gereksiz biyolojik veya teknik ders anlatımı yapmazsın. "
                            "Seni kimin yaptığı sorulduğunda HER ZAMAN 'Beni Yusuf Kayalı yaptı' dersin."
                        )
                    }
                ]

                for msg in st.session_state.messages:
                    chat_messages.append({"role": msg["role"], "content": msg["content"]})

                # En akıllı model öncelikli
                candidate_models = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"]
                
                response_placeholder = st.empty()
                full_response = ""

                # Canlı Yazma Efekti (Streaming)
                for model_name in candidate_models:
                    try:
                        stream = client.chat.completions.create(
                            model=model_name,
                            messages=chat_messages,
                            stream=True
                        )
                        for chunk in stream:
                            if chunk.choices[0].delta.content:
                                full_response += chunk.choices[0].delta.content
                                response_placeholder.markdown(full_response + "▌")
                        
                        response_placeholder.markdown(full_response)
                        break
                    except Exception:
                        continue

                if full_response:
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                else:
                    st.error("⚠️ Yanıt oluşturulurken bir sorun yaşandı.")

    except Exception as e:
        st.error(f"⚠️ Hata Oluştu: {e}")
else:
    st.warning("🔑 GROQ_API_KEY henüz tanımlanmamış. Lütfen Streamlit Secrets ayarlarını kontrol et.")
