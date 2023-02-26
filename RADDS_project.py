

import streamlit as st

import pandas as pd
from io import StringIO
import openpyxl

import requests
from streamlit_lottie import st_lottie

from PIL import Image

#conexão com o lottie
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

#Uso de próprio CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)

## FUNÇÃO CHECK DE SENHA
def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Digite a senha para acessar", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True

#CHECANDO SE USUÁRIO POSSUI UMA SENHA

st.set_page_config(page_title="My webpage", page_icon=":factory:", layout="wide")
local_css("style/style.css")
if check_password():

    st.write("Here goes your normal Streamlit app...")
    st.button("Click me")

    #PROGRAM STARTS HERE AFTER RIGHT PASSWORD


    #LOAD ASSETS:
    supplychain_image = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_quxomsbr.json")

    #INTRODUCTION
    with st.container():

        st.subheader("Uma iniciativa Supply Chain Management Brazil")
        st.title("Risk Analysis and Demand Solicitation - RADDS")
        st.write("Este microserviço apresenta um framework que tem como função a devida comunicação sobre incrementos de demanda ao SCM, assim como garantem que sejam analisados, tratados e monitorados. Sua utilização também garante ao usuário uma resposta automática a respeito dos riscos envolvidos e posterior acompanhamento do sucesso desta solicitação")
        #st.write()
        #st.write("[Learn More Clicking Here >](https://medium.com/@baia-science)")


    #UPLOAD DO ARQUIVOS RADDS
    with st.container():
        st.write("---")
        left_column, right_column = st.columns ((1,2))
        with left_column:
            st.write('Passo-a-passo:')
            st.markdown('- 1. Baixar Template do RADDS:')

            with open('RADDS Standard  - Template.xlsx', 'rb') as file:
                btn = st.download_button(label = 'Baixar RADDS Template',
                                         data=file,
                                         file_name = 'RADDS Standard  - Template.xlsx',
                                         mime = 'application/octet-stream')
            st.markdown('- 2. Preencher Template do RADDS')
            st.markdown('- 3. Realizar Upload do arquivo:')
            uploaded_file = st.file_uploader("")
            st.markdown('- 4. Realizar download do resultado')
            st.markdown('- 5. Observar respostas automáticas')
            st.markdown('- 6. Caso haja interessante em dar sequência a uma solicitação de aumento de demanda, preencher formulário com a planilha resultado em anexada. Para isto, seguir link abaixo:')

            if uploaded_file is not None:
                # Can be used wherever a "file-like" object is accepted:
                RADDS = pd.read_excel(uploaded_file, skiprows=[0])



        with right_column:
            st_lottie(supplychain_image, height = 600, width=900, key="Supply chain")


    #SHOW DATASET UPLOADED
    with st.container():
        if uploaded_file is not None:
            st.write("---")
            st.header("RADDS a ser analisado:")
            st.write(RADDS.drop(columns=['Full Customer Name', 'Customer SAP Code']).reset_index(drop=True))

    #EXTRACT, CALCULATIONS AND MERGES
    with st.container():
        if uploaded_file is not None:
            st.write("---")
            st.header("Resultado")

            br = pd.read_excel("data/br.xlsx")
            bm96 = pd.read_excel("data/bm96.xlsx")
            bm9f = pd.read_excel("data/bm9f.xlsx")
            jk = pd.read_excel("data/JK.xlsx")


            RADDS['Increase'] = RADDS['Customer Future Annual Demand Quantity']-RADDS['Customer Actual Annual Demand Quantity']
            RADDS['Increase'] = RADDS['Increase']/12 #PASSANDO INCREMENTO PARA MENSAL


            analise_br = pd.merge(RADDS,br,on='SMN',how='left')
            analise_br_bm96 = pd.merge(analise_br,bm96,on='SMN',how='left')
            analise_br_bm9f = pd.merge(analise_br_bm96,bm9f,on='SMN',how='left')

            feedback = analise_br_bm9f.copy()

            feedback['Aumento BR'] = feedback['Increase']/feedback['demanda br']
            feedback['Aumento Estoque Geral'] = feedback['Increase']/feedback['demanda bm96']

            feedback.loc[feedback['Aumento Estoque Geral']<0.2, 'Análise de Risco SCM'] = 'Aumento NÃO traz risco ao estoque geral '
            feedback.loc[feedback['Aumento Estoque Geral']<0.2, 'Nível do aumento Estoque Geral'] = 'Nulo'

            feedback.loc[(feedback['Aumento Estoque Geral']>=0.2) & (feedback['Aumento Estoque Geral']<=0.4), 'Análise de Risco SCM'] = 'Aumento traz risco médio ao estoque geral '
            feedback.loc[(feedback['Aumento Estoque Geral']>=0.2) & (feedback['Aumento Estoque Geral']<=0.4), 'Nível do aumento Estoque Geral'] = 'Médio'

            feedback.loc[feedback['Aumento Estoque Geral']>0.4, 'Análise de Risco SCM'] = 'Aumento traz risco grave ao estoque geral '
            feedback.loc[feedback['Aumento Estoque Geral']>0.4, 'Nível do aumento Estoque Geral'] = 'Alto'



            feedback.loc[feedback['Aumento BR'] < 0.2, 'Análise de Risco SCM'] = feedback['Análise de Risco SCM'].astype('str') +   'e NÃO traz risco grave a Siemens Brasil'
            feedback.loc[feedback['Aumento BR'] < 0.2, 'Nível de Aumento Brasil'] = 'Nulo'

            feedback.loc[(feedback['Aumento BR'] >= 0.2) & (feedback['Aumento BR'] <= 0.4), 'Análise de Risco SCM'] = feedback['Análise de Risco SCM'].astype('str') + 'e Aumento traz risco médio a Siemens Brasil'''
            feedback.loc[(feedback['Aumento BR'] >= 0.2) & (feedback['Aumento BR'] <= 0.4), 'Nível de Aumento Brasil'] = 'Médio'

            feedback.loc[feedback['Aumento BR'] > 0.4, 'Análise de Risco SCM'] = feedback['Análise de Risco SCM'].astype('str') +   'e Aumento traz risco grave a Siemens Brasil'
            feedback.loc[feedback['Aumento BR'] > 0.4, 'Nível de Aumento Brasil'] = 'Alto'

            feedback2 = pd.merge(feedback,jk,on='SMN',how='left')

            st.write(feedback2)

            feedback2.to_excel('RADDS Result.xlsx',index=False)

            GH_BR = feedback2['Nível de Aumento Brasil'].value_counts().to_frame()
            #GH_BR.insert(1,'Total',feedback2.shape[0])
            #GH_BR = GH_BR.T
            #st.write(GH_BR)

            GH_geral = feedback2['Nível do aumento Estoque Geral'].value_counts().to_frame()
            #GH_geral.insert(1,'Total',feedback2.shape[0])
            #st.write(GH_geral)



            with open('RADDS Result.xlsx', 'rb') as file:
                col1, col2, col3 = st.columns(3)
                with col1:
                    pass
                with col3:
                    pass
                with col2:
                    btn = st.download_button(label = 'Clique aqui para realizar Download',
                                             data=file,
                                             file_name = 'Radds result.xlsx',
                                             mime = 'application/octet-stream')

    #CALCULATION FOR PLOTS


    with st.container():
        if uploaded_file is not None:
            st.write("---")
            st.header("Resultado Gráfico:")
            left_column, right_column = st.columns(2)
            with right_column:
                st.subheader("#Niveis de aumento por categoria - Relativo a Brasil")
                st.bar_chart(GH_BR, x=['Nulo','Médio','Alto'])
            with left_column:
                st.subheader("#Niveis de aumento por categoria - Relativo ao Estoque Geral")
                st.bar_chart(GH_geral, x=['Nulo','Médio','Alto'])






