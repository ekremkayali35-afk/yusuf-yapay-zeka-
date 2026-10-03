import streamlit as st
from groq import Groq

st.set_page_config(page_title="Yusuf'un Yapay Zekası", page_icon="🤖")

st.title("Yusuf'un Yapay Zekası 🤖")
st.write("Hoş geldin! Dilediğin soruyu sorabilirsin.")

if "GROQ_API_KEY" in st.secrets:
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])

        # Groq sunucularındaki O AN AKTİF olan modelleri canlı olarak çekiyoruz
        try:
            models_list = client.models.list()
            # Sadece sohbet için uygun olan aktif modelleri filtreliyoruz
            active_models = [
                m.id for m in models_list.data 
                if "whisper" not in m.id and "guard" not in m.id and "safetensors" not in m.id
            ]
        except Exception:
            # Canlı liste çekilemezse varsayılan en güncel modeller
            active_models = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"]

        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Eski mesajları ekrana bas
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Bir şeyler yaz..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
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
                        )
                    }
                ]

                for msg in st.session_state.messages:
                    chat_messages.append({"role": msg["role"], "content": msg["content"]})

                bot_reply = None
                last_error = None

                # Canlı listeden bulduğu ilk çalışan aktif modeli kullanır
                for model_name in active_models:
                    try:
                        response = client.chat.completions.create(
                            model=model_name,
                            messages=chat_messages
                        )
                        bot_reply = response.choices[0].message.content
                        break
                    except Exception as err:
                        last_error = err
                        continue

                if bot_reply:
                    st.markdown(bot_reply)
                    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
                else:
                    st.error(f"⚠️ Hata Oluştu: {last_error}")

    except Exception as e:
        st.error(f"⚠️ Hata Oluştu: {e}")
else:
    st.warning("🔑 GROQ_API_KEY henüz tanımlanmamış. Lütfen Streamlit Secrets ayarlarını kontrol et.")
