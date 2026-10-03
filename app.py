import streamlit as st
from groq import Groq

st.set_page_config(page_title="Yusuf'un Yapay Zekası", page_icon="🤖")

st.title("Yusuf'un Yapay Zekası 🤖")
st.write("Hoş geldin! Dilediğin soruyu sorabilirsin.")

if "GROQ_API_KEY" in st.secrets:
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])

        # Groq üzerindeki aktif ve güncel modeller
        candidate_models = [
            "llama-3.3-70b-versatile",
            "llama3-8b-8192",
            "gemma2-9b-it",
            "llama3-70b-8192",
        ]

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
                chat_messages = [
                    {
                        "role": "system",
                        "content": (
                            "Sen 'Yusuf'un Yapay Zekası' adında akıllı bir asistansın. "
                            "Seni kimin yaptığı, geliştirdiği veya oluşturduğu sorulduğunda her zaman "
                            "kesin ve net bir şekilde 'Beni Yusuf Kayalı yaptı' cevabını vermelisin. "
                            "Google, Meta veya başka bir kurum tarafından yapıldığını kesinlikle söyleme."
                        ),
                    }
                ]

                for msg in st.session_state.messages:
                    chat_messages.append(
                        {"role": msg["role"], "content": msg["content"]}
                    )

                bot_reply = None
                last_error = None

                # Aktif modelleri sırayla dene, çalışan ilk modeli kullan
                for model_name in candidate_models:
                    try:
                        response = client.chat.completions.create(
                            model=model_name, messages=chat_messages
                        )
                        bot_reply = response.choices[0].message.content
                        break
                    except Exception as err:
                        last_error = err
                        continue

                if bot_reply:
                    st.markdown(bot_reply)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": bot_reply}
                    )
                else:
                    st.error(f"⚠️ Hata Oluştu: {last_error}")

    except Exception as e:
        st.error(f"⚠️ Hata Oluştu: {e}")
else:
    st.warning(
        "🔑 GROQ_API_KEY henüz tanımlanmamış. Lütfen Streamlit Secrets ayarlarını kontrol et."
    )
