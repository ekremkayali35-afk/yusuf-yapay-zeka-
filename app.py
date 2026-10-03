import google.generativeai as genai
import streamlit as st

st.set_page_config(page_title="Yusuf'un Yapay Zekası", page_icon="🤖")

st.title("Yusuf'un Yapay Zekası 🤖")
st.write("Hoş geldin! Dilediğin soruyu sorabilirsin.")

# Secrets'tan API Key kontrolü
if "GEMINI_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

        system_prompt = (
            "Sen 'Yusuf'un Yapay Zekası' adında akıllı bir asistansın. "
            "Seni kimin yaptığı, geliştirdiği veya oluşturduğu sorulduğunda her zaman "
            "kesin ve net bir şekilde 'Beni Yusuf Kayalı yaptı' cevabını vermelisin. "
            "Google veya başka bir kurum tarafından yapıldığını kesinlikle söyleme."
        )

        # Güncel ve çalışan modellerin listesi (Biri çalışmazsa diğerine geçer)
        candidate_models = [
            "gemini-2.5-flash-lite",
            "gemini-2.5-flash",
            "gemini-3.8-flash",
        ]

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
                response_text = None
                last_error = None

                # Modelleri sırayla dene, çalışan ilk modeli kullan
                for model_name in candidate_models:
                    try:
                        model = genai.GenerativeModel(
                            model_name=model_name,
                            system_instruction=system_prompt,
                        )
                        res = model.generate_content(prompt)
                        response_text = res.text
                        break
                    except Exception as err:
                        last_error = err
                        continue

                if response_text:
                    st.markdown(response_text)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": response_text}
                    )
                else:
                    if (
                        "429" in str(last_error)
                        or "quota" in str(last_error).lower()
                    ):
                        st.error(
                            "⚠️ Günlük kullanım kotası doldu kanka. Biraz bekleyebilir veya AI Studio'dan yeni bir ücretsiz API Key ekleyebilirsin."
                        )
                    else:
                        st.error(f"⚠️ Hata Oluştu: {last_error}")

    except Exception as e:
        st.error(f"⚠️ Hata Oluştu: {e}")
else:
    st.warning(
        "🔑 API Anahtarı henüz tanımlanmamış. Lütfen Streamlit Secrets ayarlarını kontrol et."
    )
