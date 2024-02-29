import streamlit as st

st.set_page_config(page_title="ADM", page_icon=":bar_chart:", layout="wide")

st.title("ADM")

with st.form("my_form"):
    st.markdown("**Formulário testes**")
    st.radio("Qual seu tipo de escritório?", ['Salas separadas', 'Coworking', 'Home office'])
    st.slider("Quantas pessoas trabalham com você?", 1, 10)
    cep = st.text_input("Digite seu CEP")

    submitted = st.form_submit_button("Pressione")
    if submitted:
        st.title('Seu código é "12AB5D"')
        open('dados.txt', 'w').write(f'12AB5D/{cep}')

