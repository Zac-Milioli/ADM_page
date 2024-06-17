from utils.config import *

initialize_page()


col1, col2, col3 = st.columns([1.3,1,1.3])
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
cep = col1.text_input(label="none", label_visibility="collapsed", placeholder="CEP")
endereco_c = form_edificio.container()
col1, col2, col3, col4 = endereco_c.columns([2,0.5,1.5,1])
# if cep:
#     headers = {'Authorization': 'Bearer your_token'}
#     response = requests.get(f"https://h-apigateway.conectagov.estaleiro.serpro.gov.br/api-cep/v1/consulta/cep/{cep}", headers=headers)
#     r_code = response.status_code
#     if r_code == 200:
#         response = json.loads(response.content)
#         endereco = f"{response['endereco']}, {response['bairro']}. {response['cidade']}/{response['uf']}"
#         col1.text_input(label="none", label_visibility="collapsed", value=endereco, disabled=True)
#     else:
#         endereco = col1.text_input(label="none", label_visibility="collapsed", placeholder="Endereço")
endereco = col1.text_input(label="none", label_visibility="collapsed", placeholder="Endereço")
numero = col2.text_input(label="none", label_visibility="collapsed", placeholder='Número')
complemento = col3.text_input(label="none", label_visibility="collapsed", placeholder='Complemento')
cidade = col4.text_input(label="none", label_visibility="collapsed", placeholder='Cidade')

