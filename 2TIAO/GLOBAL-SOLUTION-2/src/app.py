import pandas as pd
import streamlit as st

from src.recomendador import MATERIAIS, catalogo, cobertura, recomendar

st.set_page_config(page_title="ReciclaBairro", page_icon="♻️")
st.title("ReciclaBairro")
st.write("Encontre um ponto que aceite o material que você quer descartar.")
st.info("Demonstração com pontos e bairros fictícios. Consulte o serviço municipal para um descarte real.")

with catalogo() as db:
    bairros = [linha[0] for linha in db.execute(
        "SELECT DISTINCT bairro FROM ponto ORDER BY bairro"
    )]
    busca, panorama = st.tabs(["Buscar ponto", "Cobertura da base"])
    with busca:
        esquerda, direita = st.columns(2)
        bairro = esquerda.selectbox("Seu bairro", bairros)
        material = direita.selectbox("Material para descarte", MATERIAIS)
        sabado = st.checkbox("Mostrar apenas pontos com atendimento aos sábados")
        resultados = recomendar(db, bairro, material, sabado)
        if resultados:
            st.subheader(f"Pontos compatíveis ({len(resultados)})")
            if not resultados[0]["no_bairro"]:
                st.caption("As opções disponíveis ficam em outros bairros da base.")
            for ponto in resultados:
                with st.container(border=True):
                    st.markdown(f"**{ponto['nome']}** · {ponto['bairro']}")
                    local = "no bairro escolhido" if ponto["no_bairro"] else "em outro bairro"
                    horario = "atende aos sábados" if ponto["sabado"] else "sem atendimento aos sábados"
                    st.write(f"Aceita {material.lower()} · {local} · {horario}.")
        else:
            st.warning("Nenhum ponto da base atende a esta busca. Confira os filtros.")
    with panorama:
        totais = {linha["material"]: linha["total"] for linha in cobertura(db)}
        dados = pd.DataFrame({
            "Material": MATERIAIS,
            "Pontos compatíveis": [totais.get(item, 0) for item in MATERIAIS],
        })
        st.metric("Pontos simulados", db.execute("SELECT COUNT(*) FROM ponto").fetchone()[0])
        st.bar_chart(dados, x="Material", y="Pontos compatíveis", sort=False)
        st.dataframe(dados, hide_index=True)
        st.caption("Um mesmo ponto pode aparecer na contagem de vários materiais.")
