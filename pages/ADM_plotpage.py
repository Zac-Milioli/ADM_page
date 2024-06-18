from utils.config import *

initialize_page()

st.title("ADM Plotter Page")
st.header("Ainda em desenvolvimento...")
st.title("")
st.title("")
st.subheader("Mentira, essa página ainda nem começou a ser desenvolvida")

st.title("")
st.title("")
col1, col2, col3 = st.columns(3)
if col2.button(label='Voltar à página inicial de ADM', use_container_width=True):
    switch_page('ADM_firstpage')