import google.generativeai as genai
import streamlit as st

st.set_page_config(page_title="Yusuf'un Yapay Zekası", page_icon="🤖")

st.title("Yusuf'un Yapay Zekası 🤖")
st.write("Hoş geldin! Dilediğin soruyu sorabilirsin.")

# Secrets'tan API Key kontrolü
if "GEMINI_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel("gemini-1.5-flash")

        # Sohbet Geçmişi
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Eski Mesajları Göster
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Kullanıcı Mesajı
        if prompt := st.chat_input("Bir şeyler yaz..."):
            st.session_state.messages.append(
                {"role": "user", "content": prompt}
            )
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append(
                    {"role": "assistant", "content": response.text}
                )

    except Exception as e:
        st.error(f"⚠️ Hata Oluştu: {e}")
else:
    st.warning(
        "🔑 API Anahtarı henüz tanımlanmamış. Lütfen Streamlit Secrets ayarlarını kontrol et."
    )
