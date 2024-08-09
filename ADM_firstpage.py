import streamlit as st
from utils.config import *

initialize_page()

col1, col2 = st.columns([5,1])
if col2.button(label="Ir para o dashboard", use_container_width=True):
    switch_page("ADM_plotpage")
if col2.button(label="Verificar meu local de trabalho", use_container_width=True):
    switch_page("ADM_searchpage")
col1, col2, col3 = st.columns([1.5,1,1.5])
col2.title("ADMINISTRADOR")
col1, col2, col3 = st.columns([1.9,1.7,2])
col2.subheader("Para conectar-se ao seu local de trabalho,")
col1, col2, col3 = st.columns([1.5,1,1.5])
col2.subheader("preencha os campos abaixo:")
st.title("")
form_email = st.container(border=True)
form_email.title("")
col1, col2 = form_email.columns([4,1])
email = col1.text_input(label="Email").strip()
col2.subheader('')
if col2.button(label="Enviar código de verificação", use_container_width=True):
    try:
        st.session_state['auth_code'] = mail_auth_code(email)
        st.session_state['email'] = email
    except:
        st.error('Um erro ocorreu ao tentar enviar o email de verificação. Verifique se o email inserido está correto e tente novamente', icon="⚠️")
codigo = form_email.text_input(label="Código", max_chars=6)
col1, col2, col3 = form_email.columns(3)
if col2.button(label="Validar código", use_container_width=True):
    if not st.session_state.get('auth_code'):
        st.error('ERRO: O código de verificação não foi gerado', icon="⚠️")
    elif st.session_state['auth_code'] == codigo:
        switch_page("ADM_edificio")
    else:
        st.error('ERRO: O código inserido é diferente do código enviado', icon="⚠️")
    
footer()