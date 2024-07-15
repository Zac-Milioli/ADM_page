import streamlit as st

link = "nada"

st.set_page_config(page_title='Conexão Tableau', layout='wide')

st.title("Teste 03 conexão com Tableau")

html = f'''<iframe 
            width=100%
            height=850px
            src="{link}">
        </iframe>
'''

st.markdown(html, unsafe_allow_html=True)
