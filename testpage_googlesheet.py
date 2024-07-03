import streamlit as st
from streamlit_gsheets import GSheetsConnection
import gspread
from google.oauth2.service_account import Credentials

scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)
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