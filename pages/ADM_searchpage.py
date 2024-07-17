from utils.config import *

initialize_page()

if st.button(label='Voltar'):
    switch_page("ADM_firstpage")
st.title("Buscar local de trabalho")
st.title("")
form_email = st.container(border=True)
col1, col2 = form_email.columns([4,1])
email = col1.text_input(label="Email").strip()
col2.subheader('')
if col2.button(label="Enviar código de verificação", use_container_width=True):
    try:
        st.session_state['auth_code'] = mail_auth_code_searchpage(email)
        st.session_state['email'] = email
    except:
        st.error('Um erro ocorreu ao tentar enviar o email de validação. Verifique se o email inserido está correto e tente novamente', icon="⚠️")
col1, col2 = form_email.columns(2)
codigo = col1.text_input(label="Código de validação", max_chars=6)
id_search = col2.text_input(label="Insira o ID do seu local de trabalho:", max_chars=8)
check_inputs = True if not (id_search and codigo) else False
col1, col2, col3 = form_email.columns(3)
if col2.button(label="Validar código e buscar local de trabalho", use_container_width=True, disabled=check_inputs):
    if not st.session_state.get('auth_code'):
        st.error('ERRO: O código de confirmação não foi gerado', icon="⚠️")
    elif st.session_state['auth_code'] == codigo:
        returned, status = get_build_info_by_id(id_=int(id_search), email=st.session_state['email'])
        if status == "OK":
            return_list = returned.iloc[0].tolist()
            st.session_state['build_id'] = int(return_list.pop(0))
            st.session_state['email'] = return_list.pop(0)
            st.session_state['check_answers'] = return_list
            switch_page("ADM_final")
        else:
            st.error("O ID do local de trabalho inserido não foi encontrado na base de dados", icon='⚠️')
    else:
        st.error('ERRO: O código inserido é diferente do código enviado', icon="⚠️")

footer()