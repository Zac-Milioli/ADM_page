from utils.config import *

initialize_page()

col1, col2, col3 = st.columns([1,1.5,1])
if col1.button('Voltar ao início'):
    switch_page("ADM_firstpage")


st.title("")
_, col, _ = st.columns(3)
data_review_c = col.container(border=True)
data_review_c.subheader("O ID do local de trabalho é único e refere-se aos seguintes dados informados:")
col1, col2 = data_review_c.columns(2)
parte1, parte2 = st.session_state.get('check_answers')[:7], st.session_state.get('check_answers')[8:]
for item in parte1:
    col1.markdown(f"- {item}")
for item in parte2:
    col2.markdown(f"- {item}")
data_review_c.subheader("Você pode usar este ID sempre que desejar avaliar o mesmo local de trabalho")
st.title("")
st.subheader('Este é o ID do seu local de trabalho:')
st.title(st.session_state.get("build_id"))
st.subheader("Informe o ID do local de trabalho para todos os participantes da pesquisa.")
st.subheader("Este código será necessário para acessar o questionário.")

st.title("")
st.title("")
participants = st_tags(label="Insira a lista de emails no campo abaixo para convidar os participantes da pesquisa automaticamente", text='Escreva o email e pressione ENTER para adicionar')
_, col = st.columns([4,1])
if col.button(label='Enviar emails', use_container_width=True):
    try:
        with st.spinner("Enviando emails..."):
            mailto(participants=participants, id_=st.session_state.get("build_id"))
        st.success("Emails enviados com sucesso!", icon="✅")
    except Exception as e:
        st.error('Houve um problema ao enviar os emails', icon="⚠️")

st.title("")
st.subheader("Se preferir, copie a mensagem abaixo no seu email:")
st.code(body=f"""Você foi convidado a avaliar o seu local de trabalho.
Clique aqui para acessar o questionário {quest_link} e informe o ID do seu local de trabalho:
{st.session_state.get('build_id')}""", line_numbers=True)