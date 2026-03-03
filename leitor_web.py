import streamlit as st # type: ignore
import pandas as pd
from io import BytesIO
import os
import plotly.express as px
import time

# 🎨 Configuração da página
st.set_page_config(
    page_title="Leitor de CNPJs",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ✅ CSS leve (mantém o visual padrão, remove menus e centraliza título)
st.markdown("""
<style>
    #MainMenu, footer, header {visibility: hidden;}
    div.block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    .stButton>button {
        border-radius: 8px;
        background: linear-gradient(90deg, #0072ff, #00c6ff);
        color: white;
        border: none;
    }
    h1 {
        text-align: center;
        color: #0072ff;
    }
</style>
""", unsafe_allow_html=True)

class LeitorCNPJ:
    def __init__(self):
        self.regioes = {
            'Norte': ['AC', 'AP', 'AM', 'PA', 'RO', 'RR', 'TO'],
            'Nordeste': ['AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE'],
            'Centro-Oeste': ['DF', 'GO', 'MT', 'MS'],
            'Sudeste': ['ES', 'MG', 'RJ', 'SP'],
            'Sul': ['PR', 'RS', 'SC']
        }

        self.capitais = {
            'AC': 'Rio Branco', 'AL': 'Maceió', 'AP': 'Macapá', 'AM': 'Manaus',
            'BA': 'Salvador', 'CE': 'Fortaleza', 'DF': 'Brasília', 'ES': 'Vitória',
            'GO': 'Goiânia', 'MA': 'São Luís', 'MT': 'Cuiabá', 'MS': 'Campo Grande',
            'MG': 'Belo Horizonte', 'PA': 'Belém', 'PB': 'João Pessoa', 'PR': 'Curitiba',
            'PE': 'Recife', 'PI': 'Teresina', 'RJ': 'Rio de Janeiro', 'RN': 'Natal',
            'RS': 'Porto Alegre', 'RO': 'Porto Velho', 'RR': 'Boa Vista', 'SC': 'Florianópolis',
            'SP': 'São Paulo', 'SE': 'Aracaju', 'TO': 'Palmas'
        }

        self.inicializar_sessao()
        self.carregar_arquivo_padrao()

    def inicializar_sessao(self):
        if 'tabela' not in st.session_state:
            st.session_state.tabela = None
        if 'dados_carregados' not in st.session_state:
            st.session_state.dados_carregados = False
        if 'arquivo_nome' not in st.session_state:
            st.session_state.arquivo_nome = ""

    def carregar_arquivo_padrao(self):
        if os.path.exists("202508_CNPJ.csv") and not st.session_state.dados_carregados:
            try:
                df = pd.read_csv("202508_CNPJ.csv", encoding='ISO-8859-1', sep=';', dtype=str)
                st.session_state.tabela = df
                st.session_state.dados_carregados = True
                st.session_state.arquivo_nome = "202508_CNPJ.csv"
                st.success("✅ Arquivo padrão carregado automaticamente!")
            except Exception as e:
                st.error(f"❌ Erro ao carregar arquivo padrão: {str(e)}")

    def carregar_arquivo_usuario(self):
        st.subheader("📂 Importar Arquivo CSV")
        uploaded = st.file_uploader(
            "Enviar CSV com CNPJs", type=['csv'], help="Use separador ';'"
        )
        if uploaded is not None:
            try:
                df = pd.read_csv(uploaded, encoding='ISO-8859-1', sep=';', dtype=str, low_memory=False)
                st.session_state.tabela = df
                st.session_state.dados_carregados = True
                st.session_state.arquivo_nome = uploaded.name
                st.success("✅ Arquivo carregado com sucesso!")
            except Exception as e:
                st.error(f"❌ Erro: {str(e)}")

        col1, col2 = st.columns([1, 1])

    def validar_arquivo(self):
        if st.session_state.tabela is None:
            return False
        if 'UF' not in st.session_state.tabela.columns:
            st.error("❌ O arquivo precisa conter uma coluna chamada **'UF'**.")
            return False
        return True

    def exibir_metricas(self):
        df = st.session_state.tabela
        total = len(df)
        estados = df['UF'].nunique()
        col1, col2, col3 = st.columns(3)
        col1.metric("📊 Total de CNPJs", f"{total:,}")
        col2.metric("🗺️ Estados únicos", estados)
        col3.metric("📁 Arquivo", st.session_state.arquivo_nome or "—")
        st.markdown("---")

    def filtro(self):
        st.subheader("🗺️ Filtros de Pesquisa")
        tab1, tab2, tab3 = st.tabs(["🏛️ Por Estado", "🌎 Por Região", "🏙️ Capitais"])
        resultado, tipo = None, None
        with tab1:
            estados = st.text_input("Digite as siglas dos estados (ex: SP, RJ, MG):")
            if st.button("🔍 Pesquisar por Estado"):
                resultado = estados
                tipo = "estados"
        with tab2:
            regiao = st.selectbox("Selecione uma região:", [""] + list(self.regioes.keys()))
            if st.button("🔍 Pesquisar por Região"):
                if regiao:
                    resultado = ",".join(self.regioes[regiao])
                    tipo = "regiao"
        with tab3:
            st.info("Filtra apenas CNPJs das 27 capitais brasileiras.")
            if st.button("🔍 Pesquisar Capitais"):
                resultado = ",".join(self.capitais.keys())
                tipo = "capitais"
        return resultado, tipo

    def processar(self, entrada, tipo):
        if not entrada:
            return None
        ufs = [uf.strip().upper() for uf in entrada.split(',') if uf.strip()]
        df = st.session_state.tabela
        with st.spinner("📊 Processando dados..."):
            time.sleep(0.05)
        filtro = df[df['UF'].isin(ufs)]
        if filtro.empty:
            st.warning("⚠️ Nenhum dado encontrado.")
            return None
        contagem = filtro['UF'].value_counts().sort_values(ascending=False)
        tabela = contagem.to_frame('Quantidade')
        tabela['Porcentagem'] = (tabela['Quantidade'] / tabela['Quantidade'].sum()) * 100
        tabela.loc['Total'] = [tabela['Quantidade'].sum(), 100.0]
        return tabela

    def exibir(self, tabela, tipo):
        st.subheader("📊 Resultados")
        df_display = tabela.copy()
        df_display['Quantidade'] = df_display['Quantidade'].apply(lambda x: f"{int(x):,}")
        df_display['Porcentagem'] = df_display['Porcentagem'].apply(lambda x: f"{x:.1f}%")
        st.data_editor(df_display, use_container_width=True, hide_index=False)
        fig = px.bar(
            tabela.iloc[:-1],
            x=tabela.iloc[:-1].index,
            y='Quantidade',
            title="Distribuição de CNPJs por Estado",
            text_auto=True,
            color='Quantidade',
        )
        st.plotly_chart(fig, use_container_width=True)
        total = int(tabela.loc['Total', 'Quantidade'])
        st.success(f"✅ Total encontrado: {total:,} CNPJs")

    def download(self, tabela):
        st.subheader("💾 Downloads")
        col1, col2 = st.columns(2)
        with col1:
            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                tabela.to_excel(writer, index=True)
            st.download_button("📊 Baixar Excel", buffer.getvalue(), "cnpjs.xlsx")
        with col2:
            csv = tabela.to_csv(index=True).encode('utf-8-sig')
            st.download_button("📄 Baixar CSV", csv, "cnpjs.csv")


# 🚀 Execução principal
def main():
    # Título centralizado
    st.markdown("<h1>📊 Leitor de CNPJs</h1>", unsafe_allow_html=True)

    app = LeitorCNPJ()
    app.carregar_arquivo_usuario()

    if not st.session_state.dados_carregados:
        st.markdown(
            "<div style='text-align: center;'>📂 Envie um arquivo CSV com dados de CNPJs ou use o arquivo padrão.</div>",
            unsafe_allow_html=True
        )
        return

    if not app.validar_arquivo():
        return

    app.exibir_metricas()
    entrada, tipo = app.filtro()

    if entrada:
        tabela = app.processar(entrada, tipo)
        if tabela is not None:
            app.exibir(tabela, tipo)
            app.download(tabela)


if __name__ == "__main__":
    main()
