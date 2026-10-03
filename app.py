from groq import Groq
import streamlit as st

st.set_page_config(page_title="Yusuf'un Yapay Zekası", page_icon="🤖")

st.title("Yusuf'un Yapay Zekası 🤖")
st.write("Hoş geldin! Dilediğin soruyu sorabilirsin.")

if "GROQ_API_KEY" in st.secrets:
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])

        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Eski mesajları ekrana bas
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Bir şeyler yaz..."):
            st.session_state.messages.append(
                {"role": "user", "content": prompt}
            )
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                # Kimlik tanımı ve sohbet geçmişi
                chat_messages = [
                    {
                        "role": "system",
                        "content": (
                            "Sen 'Yusuf'un Yapay Zekası' adında akıllı bir asistansın. "
                            "Seni kimin yaptığı, geliştirdiği veya oluşturduğu sorulduğunda her zaman "
                            "kesin ve net bir şekilde 'Beni Yusuf Kayalı yaptı' cevabını vermelisin. "
                            "Google veya başka bir kurum tarafından yapıldığını kesinlikle söyleme."
                        ),
                    }
                ]

                for msg in st.session_state.messages:
                    chat_messages.append(
                        {"role": msg["role"], "content": msg["content"]}
                    )

                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=chat_messages,
                )

                bot_reply = response.choices[0].message.content
                st.markdown(bot_reply)
                st.session_state.messages.append(
                    {"role": "assistant", "content": bot_reply}
                )

    except Exception as e:
        st.error(f"⚠️ Hata Oluştu: {e}")
else:
    st.warning(
        "🔑 GROQ_API_KEY henüz tanımlanmamış. Lütfen Streamlit Secrets ayarlarını kontrol et."
    )
