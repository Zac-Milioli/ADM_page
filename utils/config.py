import streamlit as st
import smtplib
import email.message
from random import randint
import json
import requests

# authorization_list = st.secrets["AUTH_LIST"]
# password = st.secrets['EMAIL_PASSWORD']
password = "sxux ztfv fsiw aqfp"
authorization_list = ["519249","215333","885531","618511","572447","869808","795177","371314","349847","725307","152101","687085","930430","862644","631116","202600","226685","675900","850068","502866","499124","119076","194394","850663","501970","343110","604899","873815","873732","332027","229599","195539","642693","113458","973402","798801","651854","588405","940423","774287","620429","797880","652906","713421","149751","419936","947997","372791","250261","469589","499024","854435","413249","856289","381478","617604","476102","738816","105552","961946","633041","305899","566873","299503","924671","502313","124981","563472","999154","314874","205129","685368","875393","430502","433164","209055","254352","479366","755502","800045","218490","280180","666648","651533","831232","711813","665228","484822","798532","145640","886177","791129","482785","486436","611493","464165","665697","786134","344894","828499"]


def initialize_page():
    st.set_page_config(layout='wide',initial_sidebar_state='collapsed')
    st.markdown(
        """
    <style>
        [data-testid="collapsedControl"] {
            display: none
        }
        [data-testid="stToolbarActions"] {
            display: none
        }
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True,)
    col1, col2, col3 = st.columns(3)
    col2.image(r'static/lab_banner.png', width=400)


def mail_me(mail_person:str, edificacao:dict):
    corpo_email = f'{edificacao}'
    msg = email.message.Message()
    msg['Subject'] = f'EDIFICACAO-{mail_person}'
    msg['From'] = 'escritorios.qai.bot@gmail.com'
    msg['To'] = 'escritorios.qai.bot@gmail.com'
    msg.set_payload(corpo_email)
    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))

def mail_auth_code(mail_person:str):
    auth_code = authorization_list[randint(0, len(authorization_list)-1)]
    corpo_email = f"""
    <p>Seu código de verificação para o registro de um edifício<p>
    <h1><strong>{auth_code}</strong></h1>
    <br>
    <hr>
    <p>Esta é uma mensagem automática, não é necessário respondê-la.</p><br><br>
    <a href="https://labeee.ufsc.br/pt-br/en-welcome"><img src="https://labeee.ufsc.br/sites/default/files/labeee_final_completo_maior.png" width="400" /></a>"""
    msg = email.message.Message()
    msg['Subject'] = f'CÓDIGO DE VERIFICAÇÃO - QAI em escritórios, LabEEE'
    msg['From'] = 'escritorios.qai.bot@gmail.com'
    msg['To'] = mail_person
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email)
    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
    return auth_code

def send_thanks_email(mail_person:str):
    corpo_email = f"""
    <h2>A equipe LabEEE agradece pela participação na pesquisa!</h2>
    <br>
    <hr>
    <p>Esta é uma mensagem automática, não é necessário respondê-la.</p><br><br>
    <a href="https://labeee.ufsc.br/pt-br/en-welcome"><img src="https://labeee.ufsc.br/sites/default/files/labeee_final_completo_maior.png" width="400" /></a>"""
    msg = email.message.Message()
    msg['Subject'] = f'CONFIRMAÇÃO DE PARTICIPAÇÃO - QAI em escritórios, LabEEE'
    msg['From'] = 'escritorios.qai.bot@gmail.com'
    msg['To'] = mail_person
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email)
    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))


## STREAMLIT_EXTRAS --> switch page button
def switch_page(page_name: str):
    """
    Switch page programmatically in a multipage app

    Args:
        page_name (str): Target page name
    """
    from streamlit.runtime.scriptrunner import RerunData, RerunException
    from streamlit.source_util import get_pages

    def standardize_name(name: str) -> str:
        return name.lower().replace("_", " ")

    page_name = standardize_name(page_name)

    pages = get_pages("streamlit_app.py")  # OR whatever your main page is called

    for page_hash, config in pages.items():
        if standardize_name(config["page_name"]) == page_name:
            raise RerunException(
                RerunData(
                    page_script_hash=page_hash,
                    page_name=page_name,
                )
            )

    page_names = [standardize_name(config["page_name"]) for config in pages.values()]

    raise ValueError(f"Could not find page {page_name}. Must be one of {page_names}")