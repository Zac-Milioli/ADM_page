import streamlit as st
import smtplib
import email.message
from random import randint
import json
import requests
from streamlit_gsheets import GSheetsConnection
import gspread
from google.oauth2.service_account import Credentials
from time import sleep
from datetime import datetime
# import pandas as pd

# ---------------VARIÁVEIS---------------

project = "VOSS"

# ESTA VARIÁVEL É SENSÍVEL E NA APLICAÇÃO REAL DEVE SER ADICIONADA AO ENV DO STREAMLIT E ACESSADA ATRAVÉS DE st.secrets["CREDENTIALS"]
credentials = {"type": "service_account","project_id": "sheets-connection-api","private_key_id": "c693b8107c458cd42c7f0be9ffc706aa6eff4dbd","private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDDh3+tWRN886tG\nkrOEBRbMxvFAQITqV8FefzkoZVkTX31Gad+yTgd/T7phnU/mcUcm9vNRjbRfBXqU\nOC+Qle9kldqJGOzhA2IvwGLHnN5+jVUXAl9Nj6C8Fs3qdiZfwEXnC62APIo9QYrR\nH0/u+ixkPFzPEu/3Ny8ECagKSt8hIxCAHU1Fe383XfiWHRebu/wdxlvBNL/Erlnf\nTygY0Cdm3ntMJbAdXRDDtO1sbL8y2Y7dsJNh5yex7kOFF7CgGWoZoiXwx4ujikd+\n1l6QG+So8nxp7pf1e/T3RA2Tfby47MjON/MWEF4p4XqGLt7zt3bkZJQagwuAeAD2\nGsjFNwMLAgMBAAECggEAF4eCO0uJV1OBTGxR8vSj0j+sf3VkKUknKWZ4694KUpT+\nn88UzsGqEE15Wc7S8yG1lMBJ9ontZzPjFNwQCT+pv7pywmW/97HvCl0F5gyAD82V\nLEAqVMyQZKH/5JOUOZiLMOsMVW6zmfx9pn20okbzuZoz9u1J+D9pRnyc/qQU5sk5\nn0i/GbHUQUwfWo2RsJ0zjvOz5n5Xc0lawvUIa04ugQfz67leDQpAkjLdw/09C3d7\nEASfL7eYI7FsAjP5HtRbS5Yd6TO4OzOp8aGJTZn+PBhjgy8gidFHKGVycecB/B5L\nyFVsV+MUqFZfq+2Vt6iV/gQsEdaMf1uILkULKXBPRQKBgQD/DlxsKkYZSAUwVnrT\n86kWXQRPjSJ5U9yGvt1Skd/x/LtWWDdNB2FVSauSSJhK+LZHlCiWc7o0gqFvq2ok\nc3zmAEN3FBUGXJXcIECtaLGgcK1XeujcpqnAhKoAsl5Z4HTCN9U7G3/7jHgmF97k\nbhR3Eu2c0WVth/RyNRutU2QNhwKBgQDEQL4Gy3zgvsoxxaZQYAf8McbwEepAzfzZ\nfr/KxY0pWT4zptgkhW0+QwSaCXShISzBiJy9aQu7Mn7XuawkKTADO428FFSZJUOe\nToR1JWzmrpGJYWR+M+asCvfVfYkEL8MoqrMBCZAwYobq07X3AiU+BohH5qi3Povq\nO+75/p9fXQKBgQDkjZLmXm9YYkA8E5KXcaXYY1vkiV0WCb74g/pB7nQWHVomQoCz\npuRij9SODj1iGUMGG07Pmz6FpXVSYvGHXnHSjPPntfgtLjQgAErU2ZcqZS3/0STv\n7Oz6libc3vlLYqZeD7gk8jyaRkK4J/XVDouKNEz2lHFmWEkFOm/lvm9O6wKBgHFr\nBSdCJJpySMI4+uQKi7LZRaJqiBoJsa40jTzvrKQP2l3Zd6KrpbXM33TyMAAK/yWe\nAQ+KDOiTxzB/Mpf3YbMMkN34Vefn3Es6D1zwUx6CFsPxkDVLY21cLVypXy0XOU9g\nT3EzCKyd1GEUF154U/OjrND44dp9ADlPh83ctFhVAoGBAMv3ly9loXruAqF2DC+8\nQkyrCI5hsNz9H2uuMhYRaCA9iWGPGr8ISrrlgYnu//mIDQ9MDJiwDBCYTQi081XU\nEM/eANKnpvGzdfQ2+9tesYM7gFH58joeZNQaXbSGSusQol7m/4CqG7VbUz7mAxqq\n0TfslpSbMgx3BmKNqwpJue3Y\n-----END PRIVATE KEY-----\n","client_email": "sheet-bot-api@sheets-connection-api.iam.gserviceaccount.com","client_id": "103080225992158614942","auth_uri": "https://accounts.google.com/o/oauth2/auth","token_uri": "https://oauth2.googleapis.com/token","auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs","client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/sheet-bot-api%40sheets-connection-api.iam.gserviceaccount.com","universe_domain": "googleapis.com"}

with open("credentials.json", "w") as file:
    json.dump(credentials, file, indent=2)
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file(r"credentials.json", scopes=scopes)
client = gspread.authorize(creds)

# ESTA VARIÁVEL É SENSÍVEL E NA APLICAÇÃO REAL DEVE SER ADICIONADA AO ENV DO STREAMLIT E ACESSADA ATRAVÉS DE st.secrets["SHEET_ID"]
sheet_id = "1T3D_x6qr4OjXQ6qMXJR0ZCywifJaHP1ck-PbZ2vT_2I"

workbook = client.open_by_key(sheet_id)
worksheet_build = workbook.worksheet('build')

# ESTA VARIÁVEL É SENSÍVEL E NA APLICAÇÃO REAL DEVE SER ADICIONADA AO ENV DO STREAMLIT E ACESSADA ATRAVÉS DE st.secrets['EMAIL_PASSWORD']
password = "sxux ztfv fsiw aqfp"

# ESTA VARIÁVEL É SENSÍVEL E NA APLICAÇÃO REAL DEVE SER ADICIONADA AO ENV DO STREAMLIT E ACESSADA ATRAVÉS DE st.secrets["AUTH_LIST"]
authorization_list = ["519249","215333","885531","618511","572447","869808","795177","371314","349847","725307","152101","687085","930430","862644","631116","202600","226685","675900","850068","502866","499124","119076","194394","850663","501970","343110","604899","873815","873732","332027","229599","195539","642693","113458","973402","798801","651854","588405","940423","774287","620429","797880","652906","713421","149751","419936","947997","372791","250261","469589","499024","854435","413249","856289","381478","617604","476102","738816","105552","961946","633041","305899","566873","299503","924671","502313","124981","563472","999154","314874","205129","685368","875393","430502","433164","209055","254352","479366","755502","800045","218490","280180","666648","651533","831232","711813","665228","484822","798532","145640","886177","791129","482785","486436","611493","464165","665697","786134","344894","828499"]

cep_link = "https://viacep.com.br/ws/{}/json/"

quest_link = 'https://www.google.com'

support_mail = "escritorios.qai.bot@gmail.com"

# ESTA VARIÁVEL É SENSÍVEL E NA APLICAÇÃO REAL DEVE SER ADICIONADA AO ENV DO STREAMLIT E ACESSADA ATRAVÉS DE st.secrets["INJECTION"]
injection = ['insert', 'drop', 'create', 'select', '*', 'update', 'delete', 'alter', 'truncate', 'execute', 'union', '--', '#', ';', 'true', 'false']

# ---------------------------------------


def initialize_page():
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


def footer():
    st.title('')
    st.title('')
    st.title('')
    col1, _, col2 = st.columns([0.5,1.5,0.5])
    col1.image(r'static/lab_banner.png', width=300)
    col2.markdown("")
    col2.caption(f"Dúvidas e suporte: {support_mail}")


def register_building(values_list: list):
    worksheet_build.append_row(values_list)


def check_for_injection(items: list):
    for item in items:
        if item in injection:
            return "INJECTION"
    return "OK"


def get_build_info_by_id(id_: int, email: str):
    conn = st.connection("gsheets", type=GSheetsConnection, ttl=0)
    sql = f'SELECT * FROM build WHERE "id" = {id_} AND "email" = \'{email}\''
    response = conn.query(sql)
    if response.empty:
        return None, "ERROR"
    return response, "OK"


def verify_build_exists(cep, numero, complemento, ocupacao, ocupacao_desc, aplicada_toda_ocupacao):
    items = [cep, numero, complemento, ocupacao, ocupacao_desc, aplicada_toda_ocupacao]
    if check_for_injection(items) == "INJECTION":
        return False
    conn = st.connection("gsheets", type=GSheetsConnection, ttl=0)
    sql = f'SELECT * FROM build WHERE "cep" = {cep} AND "numero" = \'{numero}\' AND "complemento" = \'{complemento}\' AND "ocupacao" = \'{ocupacao}\' AND "ocupacao-desc" = \'{ocupacao_desc}\' AND "aplicada-toda-ocupacao" = \'{aplicada_toda_ocupacao}\''
    response = conn.query(sql)
    if response.empty:
        return "OK"
    return False


def mail_auth_code(mail_person:str):
    auth_code = authorization_list[randint(0, len(authorization_list)-1)]
    corpo_email = f"""
    <p>Este é o seu código de verificação para se cadastrar como administrador<p>
    <h1><strong>{auth_code}</strong></h1>
    <p>Insira este código na página do ADM e informe os dados necessários para criar o ID do local de trabalho.</p>
    <hr>
    <p>Esta é uma mensagem automática, não é necessário respondê-la.</p><br><br>
    <a href="https://labeee.ufsc.br/pt-br/en-welcome"><img src="https://labeee.ufsc.br/sites/default/files/labeee_final_completo_maior.png" width="400" /></a>"""
    msg = email.message.Message()
    msg['Subject'] = f'CÓDIGO DE VERIFICAÇÃO - {project}, LabEEE'
    msg['From'] = 'escritorios.qai.bot@gmail.com'
    msg['To'] = mail_person
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email)
    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
    return auth_code


def mail_auth_code_searchpage(mail_person:str):
    auth_code = authorization_list[randint(0, len(authorization_list)-1)]
    corpo_email = f"""
    <p>Este é o seu código de verificação para buscar seu local de trabalho<p>
    <h1><strong>{auth_code}</strong></h1>
    <p>Caso você não tenha solicitado este código, basta ignorar este email.</p>
    <hr>
    <p>Esta é uma mensagem automática, não é necessário respondê-la.</p><br><br>
    <a href="https://labeee.ufsc.br/pt-br/en-welcome"><img src="https://labeee.ufsc.br/sites/default/files/labeee_final_completo_maior.png" width="400" /></a>"""
    msg = email.message.Message()
    msg['Subject'] = f'CÓDIGO DE VERIFICAÇÃO - {project}, LabEEE'
    msg['From'] = 'escritorios.qai.bot@gmail.com'
    msg['To'] = mail_person
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email)
    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
    return auth_code


def confirmation_email(mail_person:str, id_: str, data: str):
    corpo_email = f"""
    <h2>Seu local de trabalho foi cadastrado com sucesso.</h2>
    <p>Este é o ID do seu local de trabalho:</p>
    <br>
    <h1><strong>{id_}</strong></h1>
    <br>
    <p><strong>Informe o ID do local de trabalho para todos os participantes da pesquisa. Este código será necessário para acessar o questionário.</strong></p>
    <p>O ID do local de trabalho é único e refere-se aos seguintes dados informados:</p>
    <li style="color: #b7b7b7;">{'</li><li style="color: #b7b7b7;">'.join(data)}</li>
    <p>Você pode usar este ID sempre que desejar avaliar o mesmo local de trabalho.</p>
    <br>
    <hr>
    <p>Esta é uma mensagem automática, não é necessário respondê-la.</p><br><br>
    <a href="https://labeee.ufsc.br/pt-br/en-welcome"><img src="https://labeee.ufsc.br/sites/default/files/labeee_final_completo_maior.png" width="400" /></a>"""
    msg = email.message.Message()
    msg['Subject'] = f'CONFIRMAÇÃO DE CADASTRO - {project}, LabEEE'
    msg['From'] = 'escritorios.qai.bot@gmail.com'
    msg['To'] = mail_person
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email)
    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))


def mailto(participants: list, id_: str):
    corpo_email = f"""
    <h1>Você foi convidado a avaliar o seu local de trabalho.</h1>
    <p><a href={quest_link}>Clique aqui para acessar o questionário</a> e informe o ID do seu local de trabalho:</p>
    <h2><strong>{id_}</strong></h2>
    <br>
    <hr>
    <p>Esta é uma mensagem automática, não é necessário respondê-la.</p><br><br>
    <a href="https://labeee.ufsc.br/pt-br/en-welcome"><img src="https://labeee.ufsc.br/sites/default/files/labeee_final_completo_maior.png" width="400" /></a>"""    
    participants = participants.split(",")
    for participant in participants:
        msg = email.message.Message()
        msg['Subject'] = f'CONVITE - {project}, LabEEE'
        msg['From'] = 'escritorios.qai.bot@gmail.com'
        msg.add_header('Content-Type', 'text/html')
        s = smtplib.SMTP('smtp.gmail.com: 587')
        msg.set_payload(corpo_email)
        s.starttls()
        s.login(msg['From'], password)
        msg['To'] = participant
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