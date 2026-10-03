import streamlit as st
from google import genai
from google.genai import types

# ⚠️ Tırnakların içine kendi gerçek API anahtarını yapıştır
client = genai.Client(api_key="AQ.Ab8RN6JvQMrkR3gR3HaTd3MbFnwNJIjDLWpwcP9HvG-H07aMBQ")

st.set_page_config(page_title="Yusuf'un Yapay Zekası", page_icon="🤖")
st.title("🤖 Yusuf'un Akıllı Yapay Zekası")

# Sohbet geçmişi
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Selam kanka! Ben Yusuf Kayalı tarafından geliştirilmiş akıllı yapay zekanım. Bana dilediğin soruyu sorabilirsin!"}
    ]

# Eski mesajları ekrana yazdır
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Kullanıcı mesaj yazdığında
if prompt := st.chat_input("Yapay zekana bir şeyler sor..."):
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Düşünüyor..."):
            try:
                response = client.models.generate_content(
                    model='gemini-3.8-flash',
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction="Sen Yusuf Kayalı tarafından yapılmış ve kurulmuş özel bir yapay zeka asistansın. Sana seni kimin yaptığı, kurduğu veya geliştirdiği sorulursa her zaman Yusuf Kayalı tarafından geliştirildiğini söyle."
                    )
                )
                st.write(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error("⚠️ Google sunucularında anlık bir yoğunluk var kanka. Lütfen birkaç saniye bekleyip sorunu tekrar yaz!")