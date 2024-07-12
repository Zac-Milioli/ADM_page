from utils.config import *

initialize_page()

st.title("Busca de local de trabalho")
id_search = st.text_input(label="Insira o ID do seu local de trabalho", max_chars=8)
_, col, _ = st.columns([3,1,3])
if col.button(label='Buscar', use_container_width=True):
    returned, status = get_build_info_by_id(id_=int(id_search))
    if status == "OK":
        return_list = returned.iloc[0].tolist()
        st.session_state['build_id'] = int(return_list.pop(0))
        st.session_state['email'] = return_list.pop(0)
        st.session_state['check_answers'] = return_list
        switch_page("ADM_final")
    else:
        st.error("O ID do local de trabalho inserido não foi encontrado na base de dados", icon='⚠️')
