import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title="Devs Brasileiros 2024",
    page_icon="🖥️",
    layout="wide"
)

st.markdown("""
<style>
    [data-testid="stMetricValue"] { font-size: 28px; font-weight: 700; }
    [data-testid="stMetricLabel"] { font-size: 13px; }
</style>
""", unsafe_allow_html=True)

USD_BRL = 5.70

@st.cache_data
def carregar_dados():
    df = pd.read_csv("survey_results_public.csv", low_memory=False)
    return df[df["Country"] == "Brazil"]

def plotly_bar(df, x, y, color_scale, height=350):
    fig = px.bar(df, x=x, y=y, orientation="h", color=x,
                 color_continuous_scale=color_scale)
    fig.update_layout(
        showlegend=False,
        coloraxis_showscale=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white", family="sans-serif"),
        height=height,
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)", title="Quantidade de Devs"),
        yaxis=dict(showgrid=False, title="")
    )
    fig.update_traces(marker_line_width=0)
    return fig

brasil = carregar_dados()
brasil_sal = brasil[
    brasil["ConvertedCompYearly"].notna() &
    (brasil["ConvertedCompYearly"] < 150000)
].copy()
brasil_sal["SalarioBRL"] = brasil_sal["ConvertedCompYearly"] * USD_BRL

# HEADER
st.title("🖥️ Mercado de Dev Brasileiro")
st.caption("Stack Overflow Developer Survey 2024 · Análise exclusiva do Brasil · Câmbio: R$ 5,70")
st.divider()

# MÉTRICAS
col1, col2, col3, col4 = st.columns(4)
mediana_brl = int(brasil_sal["SalarioBRL"].median())
media_brl = int(brasil_sal["SalarioBRL"].mean())

col1.metric("👥 Respondentes BR", f"{len(brasil):,}")
col2.metric("💰 Salário Mediano/ano", f"R$ {mediana_brl:,}")
col3.metric("📊 Salário Médio/ano", f"R$ {media_brl:,}")
col4.metric("💼 Com salário informado", f"{len(brasil_sal):,}")

st.divider()

# LINGUAGENS
col1, col2 = st.columns(2)

with col1:
    st.subheader("🔤 Top 10 Linguagens Usadas")
    linguagens = brasil["LanguageHaveWorkedWith"].dropna().str.split(";").explode()
    top_lang = linguagens.value_counts().head(10).reset_index()
    top_lang.columns = ["Linguagem", "Devs"]
    top_lang = top_lang.sort_values("Devs")
    st.plotly_chart(plotly_bar(top_lang, "Devs", "Linguagem", "Purples"), use_container_width=True)

with col2:
    st.subheader("🚀 Top 10 Linguagens Desejadas")
    lang_want = brasil["LanguageWantToWorkWith"].dropna().str.split(";").explode()
    top_want = lang_want.value_counts().head(10).reset_index()
    top_want.columns = ["Linguagem", "Devs"]
    top_want = top_want.sort_values("Devs")
    st.plotly_chart(plotly_bar(top_want, "Devs", "Linguagem", "RdPu"), use_container_width=True)

st.divider()

# SALÁRIO POR EXPERIÊNCIA
st.subheader("📈 Salário Mediano Anual por Anos de Experiência")
exp_sal = brasil_sal[brasil_sal["WorkExp"] <= 40].groupby("WorkExp")["SalarioBRL"].median().dropna().sort_index().reset_index()
exp_sal.columns = ["Anos de Experiência", "Salário Mediano (R$)"]

fig_exp = px.area(
    exp_sal,
    x="Anos de Experiência",
    y="Salário Mediano (R$)",
    color_discrete_sequence=["#7c6aff"]
)
fig_exp.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="white"),
    height=320,
    margin=dict(l=0, r=0, t=10, b=0),
    xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)", title="Anos de Experiência"),
    yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)", title="Salário Mediano (R$)", tickformat=",.0f")
)
fig_exp.update_traces(fill="tozeroy", fillcolor="rgba(124,106,255,0.15)", line=dict(width=2))
st.plotly_chart(fig_exp, use_container_width=True)

st.divider()

# REMOTE WORK E IA
REMOTE_MAP = {
    "Remote": "Remoto",
    "In-person": "Presencial",
    "Hybrid (some in-person, leans heavy to flexibility)": "Híbrido (mais flexível)",
    "Hybrid (some remote, leans heavy to in-person)": "Híbrido (mais presencial)",
    "Your choice (very flexible, you can come in when you want or just as needed)": "Escolha própria"
}

AI_MAP = {
    "Yes, I use AI tools daily": "Uso IA diariamente",
    "Yes, I use AI tools weekly": "Uso IA semanalmente",
    "Yes, I use AI tools monthly or infrequently": "Uso IA ocasionalmente",
    "No, and I don't plan to": "Não planejo usar IA",
    "No, but I plan to soon": "Planejo usar IA em breve"
}


col1, col2 = st.columns(2)

with col1:
    st.subheader("🏠 Modalidade de Trabalho")
    remote = brasil["RemoteWork"].map(REMOTE_MAP).value_counts().reset_index()
    remote.columns = ["Modalidade", "Devs"]
    fig_remote = px.pie(remote, values="Devs", names="Modalidade",
                        color_discrete_sequence=["#7c6aff", "#ff6a9e", "#6affb8", "#ffb86a"],
                        hole=0.4)
    fig_remote.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        height=320,
        margin=dict(l=0, r=0, t=0, b=0)
    )
    st.plotly_chart(fig_remote, use_container_width=True)

with col2:
    st.subheader("🤖 Uso de IA no Trabalho")
    ai = brasil["AISelect"].map(AI_MAP).value_counts().reset_index()
    ai.columns = ["Uso de IA", "Devs"]
    fig_ai = px.pie(ai, values="Devs", names="Uso de IA",
                    color_discrete_sequence=["#6affb8", "#7c6aff", "#ff6a9e", "#ffb86a"],
                    hole=0.4)
    fig_ai.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        height=320,
        margin=dict(l=0, r=0, t=0, b=0)
    )
    st.plotly_chart(fig_ai, use_container_width=True)

st.divider()

# INSIGHTS
st.subheader("💡 Principais Descobertas")
col1, col2, col3 = st.columns(3)

with col1:
    st.info("**JavaScript** lidera como linguagem mais usada, mas **Python** é a mais desejada — reflexo da demanda crescente em IA e dados.")

with col2:
    st.success("A diferença entre júnior e sênior pode chegar a **3x no salário**. Os primeiros 5 anos são os de maior crescimento proporcional.")

with col3:
    st.warning(f"A **mediana (R$ {mediana_brl:,}/ano)** é mais honesta que a média **(R$ {media_brl:,}/ano)** — poucos devs com salários altos distorcem a média.")

st.divider()
st.caption("Desenvolvido por Leonardo Duarte · github.com/leodevub · Dados: Stack Overflow Survey 2024")
