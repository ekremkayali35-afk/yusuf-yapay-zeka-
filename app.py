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

        # Günlük 1500 mesaja kadar ücretsiz destekleyen model
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash", system_instruction=system_prompt
        )

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
        if "429" in str(e) or "quota" in str(e).lower():
            st.error(
                "⚠️ Günlük kullanım limitine ulaşıldı. Lütfen biraz sonra tekrar dene kanka."
            )
        else:
            st.error(f"⚠️ Hata Oluştu: {e}")
else:
    st.warning(
        "🔑 API Anahtarı henüz tanımlanmamış. Lütfen Streamlit Secrets ayarlarını kontrol et."
    )
