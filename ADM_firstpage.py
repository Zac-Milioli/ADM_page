from utils.config import *

initialize_page()

col1, col2 = st.columns([5,1])
if col2.button(label="Ir à página de gráficos"):
    switch_page("ADM_plotpage")
col1, col2, col3 = st.columns([1.5,1,1.5])
col2.title("tela do ADM")
col1, col2, col3 = st.columns([1,4,1])
col2.subheader("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do aimusmod tempor")
col1, col2, col3 = st.columns([1.5,1,1.5])
col2.subheader("incidinunt ut labore")
st.title("")
form_email = st.container(border=True)
form_email.title("")
col1, col2 = form_email.columns([4,1])
email = col1.text_input(label="Email")
col2.subheader('')
if col2.button(label="Enviar código de verificação", use_container_width=True):
    pass
codigo = form_email.text_input(label="Código", max_chars=6)
col1, col2, col3 = form_email.columns(3)
if col2.button(label="Validar código", use_container_width=True):
    switch_page("ADM_edificio")
