from utils.config import *

initialize_page()


col1, col2, col3 = st.columns([1.3,1,1.3])
if col1.button('Voltar'):
    switch_page("ADM_firstpage")
col2.title("")
col2.title("Dados do edifício")
col1, col2, col3 = st.columns([1,4,1])
col2.subheader("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do aimusmod tempor")
col1, col2, col3 = st.columns([1.5,1,1.5])
col2.subheader("incidinunt ut labore")

st.title("")
form_edificio = st.container(border=True)

form_edificio.title("")

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


col1, col2 = form_edificio.columns([1,3])

col1.title("")
col1.markdown("O seu local de trabalho corresponde a:")
col2.title("")
local_trabalho = col2.radio(label="none", label_visibility="collapsed", options=["Sede própria", "Locação"], horizontal=True, index=None)

col1.title("")
col1.markdown("O seu local de trabalho ocupa:")
col2.title("")
ocupa_trabalho = col2.radio(label="none", label_visibility="collapsed", options=["Edifício completo", "Pavimento(s) inteiro(s)", "Trecho de um pavimento"], horizontal=True, index=None)

n_pavimentos = 'Trecho'
form_edificio.title("")
if ocupa_trabalho == "Edifício completo":
    form_edificio.markdown("Quantos pavimentos o edifício possui?")
    n_pavimentos = form_edificio.number_input(label="none", label_visibility="collapsed", min_value=0, max_value=163)
    n_pavimentos = None if n_pavimentos == 0 else n_pavimentos
elif ocupa_trabalho == "Pavimento(s) inteiro(s)":
    form_edificio.markdown("Qual(is) pavimento(s) é(são) ocupado(s)?")
    n_pavimentos = form_edificio.multiselect(label="none", label_visibility="collapsed", placeholder="pavimento", options=range(1,163))
    n_pavimentos = None if len(n_pavimentos) == 0 else n_pavimentos

form_edificio.title("")
col1, col2, col3 = form_edificio.columns([1,0.5,3])
col1.markdown("A pesquisa será aplicada em todos os locais de ocupação?")
aplicada_todos_locais = col2.radio(label='none', label_visibility="collapsed", options=["Sim", "Não"], horizontal=True, index=None)
aplicada_todos_locais_desc = col3.text_input(label='Informe o trecho')

not_all_answered = True
if not body.get('erro'):
    aplicada_todos_locais_desc = 'Sem trecho informado' if aplicada_todos_locais_desc == '' else aplicada_todos_locais_desc
    check_answers = [cep, endereco, numero, complemento, bairro, cidade, uf, local_trabalho, ocupa_trabalho, f"{n_pavimentos}" if n_pavimentos is not None else None, aplicada_todos_locais, aplicada_todos_locais_desc]
    if None not in check_answers:
        not_all_answered = False

col1, col2 = st.columns([4,1])
if col2.button(label='Gerar código da pesquisa', use_container_width=True, disabled=not_all_answered):
    codigo = randint(10000000, 99999999)
    answered = [codigo, st.session_state['email']] + check_answers
    register_building(answered)
    col1, col2, col3 = st.columns([0.6,1,0.6])
    col2.title("")
    col2.title(f"O código da sua pesquisa é {codigo}")
    col2.subheader("Este dado deverá ser inserido na tela inicial da pesquisa junto")
    col1, col2, col3 = st.columns([0.8,1,0.5])
    col2.subheader("com o código de verificação pessoal")
    col1, col2, col3 = st.columns([0.85,1,0.8])
    col2.markdown("Acesse o link https://www.google.com (placeholder) para responder ao questionário")
