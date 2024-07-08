import streamlit as st
st.set_page_config(layout='wide',initial_sidebar_state='collapsed')
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
email = col1.text_input(label="Email").strip()
col2.subheader('')
if col2.button(label="Enviar código de verificação", use_container_width=True):
    try:
        st.session_state['auth_code'] = mail_auth_code(email)
    except:
        st.error('Um erro ocorreu ao tentar enviar o email de validação. Verifique se o email inserido está correto e tente novamente', icon="⚠️")
codigo = form_email.text_input(label="Código", max_chars=6)
col1, col2, col3 = form_email.columns(3)
if col2.button(label="Validar código", use_container_width=True):
    if st.session_state['auth_code'] == codigo:
        st.session_state['email'] = email
        switch_page("ADM_edificio")
    else:
        st.error('ERRO: O código inserido é diferente do código enviado', icon="⚠️")
