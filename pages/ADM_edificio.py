from utils.config import *

initialize_page()


col1, col2, col3 = st.columns([1,1.5,1])
if col1.button('Voltar'):
    switch_page("ADM_firstpage")
col2.title("")
col2.title("Cadastrar novo local de trabalho")
col1, col2, col3 = st.columns([1.15,2,1])
col2.markdown("Todos os dados informados são confidenciais e não serão divulgados aos participantes da pesquisa.")
col2.markdown("As informações abaixo são necessárias para garantir o tratamento adequado dos resultados.")
col2.markdown("Os dados tratados são automaticamente anonimizados.")

st.title("")
form_edificio = st.container(border=True)

form_edificio.header("Insira abaixo os dados do local de trabalho que você deseja avaliar:")

col1, col2 = form_edificio.columns([1,3])
cep = col1.text_input(label="CEP", max_chars=8)

endereco_c = form_edificio.container()
col1, col2, col3, col4, col5, col6 = endereco_c.columns([2,0.5,1.5, 1,1,0.5])

body = {'erro': True}
if cep:
    full_link = cep_link.format(cep)
    response = requests.get(full_link)
    body = response.json()
    if not body.get('erro'):    
        cep_worked = True
        endereco = col1.text_input(label="Endereço", disabled=True, value=f"{body['logradouro']}")
        numero = col2.text_input(label="Número")
        complemento = col3.text_input(label="Complemento")
        bairro = col4.text_input(label="Bairro", disabled=True, value=f"{body['bairro']}")
        cidade = col5.text_input(label="Cidade", disabled=True, value=f"{body['localidade']}")
        uf = col6.text_input(label="UF", disabled=True, value=f"{body['uf']}")
    else:
        st.error("ERRO: CEP não encontrado", icon="⚠️")


col1, col2, col3 = form_edificio.columns([1,1,3])

col1.title("")
col1.markdown("O seu local de trabalho corresponde a:")
col2.title("")
local_trabalho = col2.radio(label="none", label_visibility="collapsed", options=["Sede própria", "Locação"], horizontal=True, index=None)

col1.title("")
col1.markdown("O seu local de trabalho ocupa:")
col2.title("")
ocupa_trabalho = col2.radio(label="none", label_visibility="collapsed", options=["Edifício completo", "Pavimento(s) inteiro(s)", "Trecho de um pavimento"], horizontal=False, index=None)

n_pavimentos = 'Trecho'
col3.title('')
col3.title('')
col3.title('')
if ocupa_trabalho == "Edifício completo":
    col3.markdown("Quantos pavimentos o edifício possui?")
    n_pavimentos = col3.number_input(label="none", label_visibility="collapsed", min_value=0, max_value=163)
    n_pavimentos = None if n_pavimentos == 0 else n_pavimentos
elif ocupa_trabalho == "Pavimento(s) inteiro(s)":
    col3.markdown("Qual(is) pavimento(s) é(são) ocupado(s)?")
    n_pavimentos = col3.multiselect(label="none", label_visibility="collapsed", placeholder="pavimento", options=range(1,163))
    n_pavimentos = None if len(n_pavimentos) == 0 else n_pavimentos

form_edificio.title("")
col1, col2, col3 = form_edificio.columns([1,0.5,3])
col1.markdown("A pesquisa será aplicada em todos os locais de ocupação?")
aplicada_todos_locais = col2.radio(label='none', label_visibility="collapsed", options=["Sim", "Não"], horizontal=True, index=None)
if aplicada_todos_locais == "Não":
    aplicada_todos_locais_desc = col3.text_input(label='Informe o trecho')
else:
    aplicada_todos_locais_desc = "Completo"

if not st.session_state.get('not_all_answered'):
    st.session_state['not_all_answered'] = True    

if not body.get('erro'):
    check_answers = [cep, endereco, numero, complemento, bairro, cidade, uf, local_trabalho, ocupa_trabalho, f"{n_pavimentos}" if n_pavimentos is not None else None, aplicada_todos_locais, aplicada_todos_locais_desc]
    if None not in check_answers and "" not in check_answers:
        st.session_state['not_all_answered'] = False

col1, col2 = st.columns([4,1])
if col2.button(label='Gerar ID do local de trabalho', use_container_width=True, disabled=st.session_state['not_all_answered']):
    with st.spinner("Verificando base de dados..."):
        status = verify_build_exists(cep=cep, numero=numero, complemento=complemento, ocupacao=ocupa_trabalho, ocupacao_desc=f"{n_pavimentos}" if n_pavimentos is not None else None, aplicada_toda_ocupacao=aplicada_todos_locais_desc)
    if status == "OK":
        with st.spinner('Registrando local de trabalho na base de dados...'):
            codigo = randint(10000000, 99999999)
            answered = [codigo, st.session_state['email']] + check_answers
            register_building(answered)
            confirmation_email(st.session_state['email'], codigo, check_answers)
            st.session_state['id_generated'] = True
            st.session_state['build_id'] = codigo
            st.session_state['check_answers'] = check_answers
        st.success("Local de trabalho registrado com sucesso! Você será reencaminhado à página de compartilhamento", icon="✅")
        aguarde = st.progress(0)
        for percent_complete in range(100):
            sleep(0.03)
            aguarde.progress(percent_complete+1)
        switch_page("ADM_final")
    else:
        st.error("ERRO: Local de trabalho já existe na base de dados", icon='⚠️')


# VERSÃO ANTIGA (Página de emails e dados do local de trabalho embutidos na página de registro de local)
# if st.session_state.get("id_generated"):
#     st.title("")
#     _, col, _ = st.columns(3)
#     data_review_c = col.container(border=True)
#     data_review_c.subheader("O ID do local de trabalho é único e refere-se aos seguintes dados informados:")
#     col1, col2 = data_review_c.columns(2)
#     parte1, parte2 = check_answers[:7], check_answers[8:]
#     for item in parte1:
#         col1.markdown(f"- {item}")
#     for item in parte2:
#         col2.markdown(f"- {item}")
#     data_review_c.subheader("Você pode usar este ID sempre que desejar avaliar o mesmo local de trabalho")
#     col.title("")
#     _, col, _ = st.columns([1,3,1])
#     col.subheader('Este é o ID do seu local de trabalho:')
#     _, col, _ = st.columns([1.5,1,1.5])
#     col.title(st.session_state.get("build_id"))
#     _, col, _ = st.columns([1,3,1])
#     col.subheader("Informe o ID do local de trabalho para todos os participantes da pesquisa.")
#     col.subheader("Este código será necessário para acessar o questionário.")

#     st.title("")
#     st.title("")
#     participants = st_tags(label="Insira a lista de emails no campo abaixo para convidar os participantes da pesquisa automaticamente", text='Escreva o email e pressione ENTER para adicionar')
#     _, col = st.columns([4,1])
#     if col.button(label='Enviar emails', use_container_width=True):
#         try:
#             with st.spinner("Enviando emails..."):
#                 mailto(participants=participants, id_=st.session_state.get("build_id"))
#             st.success("Emails enviados com sucesso!", icon="✅")
#         except Exception as e:
#             st.error('Houve um problema ao enviar os emails', icon="⚠️")

#     st.title("")
#     st.subheader("Se preferir, copie a mensagem abaixo no seu email:")
#     st.code(body=f"""Você foi convidado a avaliar o seu local de trabalho.
# Clique aqui para acessar o questionário {quest_link} e informe o ID do seu local de trabalho:
# {st.session_state.get('build_id')}""", line_numbers=True)