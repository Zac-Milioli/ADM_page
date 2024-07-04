import streamlit as st
from streamlit_gsheets import GSheetsConnection
import gspread
from google.oauth2.service_account import Credentials
import json

# ESTA VARIÁVEL É SENSÍVEL E NA APLICAÇÃO REAL DEVE SER ADICIONADA AO ENV DO STREAMLIT E ACESSADA ATRAVÉS DE st.secrets["credentials"]
credentials = {"type": "service_account","project_id": "sheets-connection-api","private_key_id": "c693b8107c458cd42c7f0be9ffc706aa6eff4dbd","private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDDh3+tWRN886tG\nkrOEBRbMxvFAQITqV8FefzkoZVkTX31Gad+yTgd/T7phnU/mcUcm9vNRjbRfBXqU\nOC+Qle9kldqJGOzhA2IvwGLHnN5+jVUXAl9Nj6C8Fs3qdiZfwEXnC62APIo9QYrR\nH0/u+ixkPFzPEu/3Ny8ECagKSt8hIxCAHU1Fe383XfiWHRebu/wdxlvBNL/Erlnf\nTygY0Cdm3ntMJbAdXRDDtO1sbL8y2Y7dsJNh5yex7kOFF7CgGWoZoiXwx4ujikd+\n1l6QG+So8nxp7pf1e/T3RA2Tfby47MjON/MWEF4p4XqGLt7zt3bkZJQagwuAeAD2\nGsjFNwMLAgMBAAECggEAF4eCO0uJV1OBTGxR8vSj0j+sf3VkKUknKWZ4694KUpT+\nn88UzsGqEE15Wc7S8yG1lMBJ9ontZzPjFNwQCT+pv7pywmW/97HvCl0F5gyAD82V\nLEAqVMyQZKH/5JOUOZiLMOsMVW6zmfx9pn20okbzuZoz9u1J+D9pRnyc/qQU5sk5\nn0i/GbHUQUwfWo2RsJ0zjvOz5n5Xc0lawvUIa04ugQfz67leDQpAkjLdw/09C3d7\nEASfL7eYI7FsAjP5HtRbS5Yd6TO4OzOp8aGJTZn+PBhjgy8gidFHKGVycecB/B5L\nyFVsV+MUqFZfq+2Vt6iV/gQsEdaMf1uILkULKXBPRQKBgQD/DlxsKkYZSAUwVnrT\n86kWXQRPjSJ5U9yGvt1Skd/x/LtWWDdNB2FVSauSSJhK+LZHlCiWc7o0gqFvq2ok\nc3zmAEN3FBUGXJXcIECtaLGgcK1XeujcpqnAhKoAsl5Z4HTCN9U7G3/7jHgmF97k\nbhR3Eu2c0WVth/RyNRutU2QNhwKBgQDEQL4Gy3zgvsoxxaZQYAf8McbwEepAzfzZ\nfr/KxY0pWT4zptgkhW0+QwSaCXShISzBiJy9aQu7Mn7XuawkKTADO428FFSZJUOe\nToR1JWzmrpGJYWR+M+asCvfVfYkEL8MoqrMBCZAwYobq07X3AiU+BohH5qi3Povq\nO+75/p9fXQKBgQDkjZLmXm9YYkA8E5KXcaXYY1vkiV0WCb74g/pB7nQWHVomQoCz\npuRij9SODj1iGUMGG07Pmz6FpXVSYvGHXnHSjPPntfgtLjQgAErU2ZcqZS3/0STv\n7Oz6libc3vlLYqZeD7gk8jyaRkK4J/XVDouKNEz2lHFmWEkFOm/lvm9O6wKBgHFr\nBSdCJJpySMI4+uQKi7LZRaJqiBoJsa40jTzvrKQP2l3Zd6KrpbXM33TyMAAK/yWe\nAQ+KDOiTxzB/Mpf3YbMMkN34Vefn3Es6D1zwUx6CFsPxkDVLY21cLVypXy0XOU9g\nT3EzCKyd1GEUF154U/OjrND44dp9ADlPh83ctFhVAoGBAMv3ly9loXruAqF2DC+8\nQkyrCI5hsNz9H2uuMhYRaCA9iWGPGr8ISrrlgYnu//mIDQ9MDJiwDBCYTQi081XU\nEM/eANKnpvGzdfQ2+9tesYM7gFH58joeZNQaXbSGSusQol7m/4CqG7VbUz7mAxqq\n0TfslpSbMgx3BmKNqwpJue3Y\n-----END PRIVATE KEY-----\n","client_email": "sheet-bot-api@sheets-connection-api.iam.gserviceaccount.com","client_id": "103080225992158614942","auth_uri": "https://accounts.google.com/o/oauth2/auth","token_uri": "https://oauth2.googleapis.com/token","auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs","client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/sheet-bot-api%40sheets-connection-api.iam.gserviceaccount.com","universe_domain": "googleapis.com"}

with open("credentials.json", "w") as file:
    json.dump(credentials, file, indent=2)

scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file(r"credentials.json", scopes=scopes)
client = gspread.authorize(creds)
# ESTA VARIÁVEL É SENSÍVEL E NA APLICAÇÃO REAL DEVE SER ADICIONADA AO ENV DO STREAMLIT E ACESSADA ATRAVÉS DE st.secrets["sheet_id"]
sheet_id = "1T3D_x6qr4OjXQ6qMXJR0ZCywifJaHP1ck-PbZ2vT_2I"
workbook = client.open_by_key(sheet_id)
worksheet = workbook.worksheet('user')

conn = st.connection("gsheets", type=GSheetsConnection, ttl=10)
data = conn.read(worksheet='user')
st.dataframe(data, use_container_width=True)

name = st.text_input("name")
id_ = st.text_input("id")
text = st.text_input("text")

col1, col2 = st.columns(2)
if col1.button("Adicionar linha nova", use_container_width=True):
    worksheet.append_row([name, id_, text])
if col2.button("Recarregar a página", use_container_width=True):
    st.rerun()
