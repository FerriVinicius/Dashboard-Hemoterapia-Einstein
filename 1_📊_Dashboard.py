import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Dashboard - Hemoterapia Einstein",
    page_icon="📊",
    layout="wide",
    )
st.header("Gestão de Tempos e Filas - Hemoterapia Einstein", divider='green')

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("https://raw.githubusercontent.com/FerriVinicius/Dashboard-Resistencia-Microbiana/main/151537457_l_normal_none.jpg");
background-size: cover;
background-position: center;
background-repeat: repeat;
background-attachment: local;
}}
[data-testid="stSidebar"] > div:first-child {{
background-image: url("https://minhabiblioteca.com.br/wp-content/uploads/2021/04/logo-einstein.png");
background-position: center; 
background-repeat: no-repeat;
background-attachment: fixed;
}}

[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}

[data-testid="stToolbar"] {{
right: 2rem;
}}
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

st.sidebar.header("Bem vindo!")
icon = "https://minhabiblioteca.com.br/wp-content/uploads/2021/04/logo-einstein.png"
st.sidebar.image(icon, use_column_width=True)

st.session_state.sbstate = 'expanded'

def rotina():
    st.write("Pedidos de rotina")
    
def reserva():
    st.write("Pedidos de reserva")
    
def urgencia():
    # Carregar o dataset
    df = pd.read_csv("https://raw.githubusercontent.com/FerriVinicius/Dashboard-Hemoterapia-Einstein/main/datasample.csv")
    
    # Converter as colunas de data para o formato desejado e lidar com valores vazios
    df["dh_solicitacao"] = pd.to_datetime(df["dh_solicitacao"], errors='coerce')
    df["dh_analise"] = pd.to_datetime(df["dh_analise"], errors='coerce')
    df["dh_coleta"] = pd.to_datetime(df["dh_coleta"], errors='coerce')
    df["dh_preparo"] = pd.to_datetime(df["dh_preparo"], errors='coerce')
    df["dh_liberado"] = pd.to_datetime(df["dh_liberado"], errors='coerce')

    # Função para determinar o status da solicitação
    def determinar_status(row):
        if pd.isnull(row["dh_analise"]):
            return "Em solicitação."
        elif pd.isnull(row["dh_coleta"]):
            return "Aguardando análise crítica."
        elif pd.isnull(row["dh_preparo"]):
            return "Aguardando amostra."
        elif pd.isnull(row["dh_liberado"]):
            return "Em preparo para liberação."
        else:
            return "Liberado"

    # Aplicar a função para determinar o status da solicitação
    df["status"] = df.apply(determinar_status, axis=1)

    # Filtrar pedidos com prioridade "Urgencia" e que não tenham o status "Liberado"
    pedidos_urgentes = df[(df["prioridade"] == "urgencia") & (df["status"] != "Liberado")]

    # Se não houver pedidos de urgência, exibir uma mensagem de sucesso
    if pedidos_urgentes.empty:
        st.success("Não há pedidos de urgência pendentes.")
    else:
        # Organizar pedidos urgentes por ordem crescente de horário de solicitação
        pedidos_urgentes.sort_values(by="dh_solicitacao", inplace=True)

        # Inverter a ordem dos pedidos urgentes
        pedidos_urgentes = pedidos_urgentes.iloc[::-1]

        # Separar os pedidos em duas colunas
        col1, col2 = st.columns(2)

        # Mostrar pedidos em andamento por padrão
        for idx, pedido in enumerate(pedidos_urgentes.itertuples()):
            if idx % 2 == 0:
                container = col1
            else:
                container = col2
                
            with container:
                with st.expander(pedido.paciente):
                    st.write("ID do paciente: ", pedido.id_paciente)
                    st.write("Horário de solicitação:", pedido.dh_solicitacao.strftime("%d/%m/%Y %H:%M"))
                    st.write("Solicitante:", pedido.responsavel_pedido)
                    st.write("ID Solicitante: ", pedido.CRM_responsavel_pedido)
                    st.write("Setor: ", pedido.setor)
                st.warning(pedido.status)
                
                # Calcular o tempo decorrido desde a solicitação
                tempo_decorrido_solicitacao = (pd.Timestamp.now() - pedido.dh_solicitacao).total_seconds() / 60
                
                # Verificar se os prazos estão dentro do limite e exibir o botão correspondente
                if pedido.status == "Em solicitação.":
                    if tempo_decorrido_solicitacao < 10:
                        st.success("Dentro do prazo definido para urgências.")
                    else:
                        st.error("Fora do prazo definido para urgências.")
                elif pedido.status == "Aguardando análise crítica.":
                    if tempo_decorrido_solicitacao < 50:
                        st.success("Dentro do prazo definido para urgências.")
                    else:
                        st.error("Fora do prazo definido para urgências.")
                elif pedido.status == "Aguardando amostra.":
                    if tempo_decorrido_solicitacao < 90:
                        st.success("Dentro do prazo definido para urgências.")
                    else:
                        st.error("Fora do prazo definido para urgências.")
                elif pedido.status == "Em preparo para liberação.":
                    if tempo_decorrido_solicitacao < 120:
                        st.success("Dentro do prazo definido para urgências.")
                    else:
                        st.error("Fora do prazo definido para urgências.")
                
                
                
                # Calcular o tempo decorrido
                horas = int(tempo_decorrido_solicitacao // 60)
                minutos = int(tempo_decorrido_solicitacao % 60)
                st.write("Tempo decorrido desde a solicitação:", f"{horas}h {minutos}min")
                
                

tab1, tab2, tab3, tab4 = st.tabs(["Urgência", "Rotina", "Reservas", "Liberados"])

def liberados():
    st.write("Pedidos liberados")

with tab1:
    urgencia()
with tab2:
    rotina()
with tab3:
    reserva()
with tab4:
    liberados()
