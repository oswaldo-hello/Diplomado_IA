
from streamlit_mic_recorder import speech_to_text
from config import llm
import streamlit as st

st.set_page_config(page_title="Asistente de Voz", layout="centered")

# Encabezado con botón de limpieza alineado a la derecha
col1, col2 = st.columns([5, 1])
with col1:
    st.image("https://i.postimg.cc/qvrfhFXr/parrot.png", width=80)
    st.markdown("### Tu Asistente de Voz: **Lorito GPT**")
    st.write("Aplicación de chat habilitada por voz (GPT-4o + Micrófono)")
with col2:
    if st.button("🗑️ Limpiar", help="Borrar toda la conversación"):
        st.session_state.messages = []
        st.session_state.record_count = 0
        st.rerun()

# Inicializar estados
if "messages" not in st.session_state:
    st.session_state.messages = []
if "record_count" not in st.session_state:
    st.session_state.record_count = 0

# Mostrar historial de conversación
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Procesar nuevo mensaje si lo hay
if "new_text" in st.session_state:
    text = st.session_state.pop("new_text")

    st.chat_message("user").markdown(text)
    st.session_state.messages.append({"role": "user", "content": text})

    with st.spinner("Pensando..."):
        try:
            response = llm.invoke(st.session_state.messages)
            assistant_response = response.content
            st.chat_message("assistant").markdown(assistant_response)
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        except Exception as e:
            st.error("Ocurrió un error al obtener la respuesta del modelo.")
            st.exception(e)

    st.session_state.record_count += 1

# 👉 Captura de voz al final del chat
text = speech_to_text(
    language="es",
    use_container_width=True,
    just_once=True,
    key=f"STT_{st.session_state.record_count}"
)

if text:
    st.session_state.new_text = text
    st.rerun()
