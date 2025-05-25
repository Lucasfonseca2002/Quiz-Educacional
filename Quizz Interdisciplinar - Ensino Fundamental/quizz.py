import streamlit as st
import pandas as pd
import plotly.express as px
import random
import datetime
import os
from io import BytesIO
import json

# Importando o banco de perguntas
from banco_de_perguntas import obter_perguntas

banco_de_perguntas = obter_perguntas()

# Configuração da página
st.set_page_config(
    page_title="Quiz Interdisciplinar 🚀",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar variáveis de sessão
if 'nome_aluno' not in st.session_state:
    st.session_state.nome_aluno = ""
if 'turma' not in st.session_state:
    st.session_state.turma = ""
if 'modo' not in st.session_state:
    st.session_state.modo = "inicial"
if 'pontuacao' not in st.session_state:
    st.session_state.pontuacao = 0
if 'tempo_inicio' not in st.session_state:
    st.session_state.tempo_inicio = None
if 'perguntas_selecionadas' not in st.session_state:
    st.session_state.perguntas_selecionadas = []
if 'respostas_aluno' not in st.session_state:
    st.session_state.respostas_aluno = {}
if 'historico' not in st.session_state:
    st.session_state.historico = []

# Função para salvar os resultados
def salvar_resultados(nome, turma, pontuacao, total, tempo, materias, dificuldade):
    data = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    percentual = round((pontuacao / total) * 100, 2)

    # Adicionar ao histórico local
    resultado = {
        "Data": data,
        "Nome": nome,
        "Turma": turma,
        "Pontuação": pontuacao,
        "Total": total,
        "Percentual": percentual,
        "Tempo": tempo,
        "Matérias": ", ".join(materias),
        "Dificuldade": dificuldade
    }
    st.session_state.historico.append(resultado)

    # Salvar no Google Sheetsp
    worksheet = conectar_google_sheets()
    if worksheet:
        try:
            worksheet.append_row([
                data, nome, turma, pontuacao, total, percentual,
                tempo, ", ".join(materias), dificuldade
            ])
        except Exception as e:
            st.error(f"Erro ao salvar no Google Sheets: {e}")


# Função para exportar resultados como Excel
def exportar_excel():
    if len(st.session_state.historico) > 0:
        df = pd.DataFrame(st.session_state.historico)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Resultados')

        return output.getvalue()
    else:
        return None


# Função para selecionar perguntas aleatórias
def selecionar_perguntas(materias, num_perguntas, dificuldade):
    perguntas_selecionadas = []

    # Verificar se há matérias selecionadas
    if not materias:
        st.warning("Nenhuma matéria selecionada. Por favor, selecione pelo menos uma matéria.")
        return []

    # Filtrar perguntas pela dificuldade
    perguntas_filtradas = {}
    total_perguntas_disponiveis = 0

    for materia in materias:
        if materia in banco_de_perguntas:
            if dificuldade == "Mista":
                perguntas_filtradas[materia] = banco_de_perguntas[materia]
            else:
                perguntas_filtradas[materia] = [p for p in banco_de_perguntas[materia] if
                                                p["dificuldade"] == dificuldade]

            total_perguntas_disponiveis += len(perguntas_filtradas[materia])

    # Verificar se há perguntas disponíveis
    if total_perguntas_disponiveis == 0:
        st.warning(
            f"Não há perguntas disponíveis para as matérias selecionadas com dificuldade '{dificuldade}'. Tente outras matérias ou outro nível de dificuldade.")
        return []

    # Calcular quantas perguntas por matéria
    perguntas_por_materia = num_perguntas // len(materias)
    extras = num_perguntas % len(materias)

    # Selecionar perguntas
    for materia in materias:
        if materia in perguntas_filtradas and perguntas_filtradas[materia]:
            qtd = perguntas_por_materia + (1 if extras > 0 else 0)
            extras -= 1 if extras > 0 else 0

            # Se não houver perguntas suficientes desta matéria, pegue todas disponíveis
            if len(perguntas_filtradas[materia]) <= qtd:
                for pergunta in perguntas_filtradas[materia]:
                    perguntas_selecionadas.append({
                        "materia": materia,
                        **pergunta
                    })
            else:
                # Selecionar aleatoriamente
                selecionadas = random.sample(perguntas_filtradas[materia], qtd)
                for pergunta in selecionadas:
                    perguntas_selecionadas.append({
                        "materia": materia,
                        **pergunta
                    })

    # Embaralhar as perguntas
    random.shuffle(perguntas_selecionadas)
    return perguntas_selecionadas


# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2641/2641409.png", width=100)
    st.title("Menu do Quiz")

    if st.session_state.modo == "inicial":
        st.session_state.nome_aluno = st.text_input("Nome do aluno:")
        st.session_state.turma = st.text_input("Turma:")

        st.subheader("Configurar Quiz")
        materias_disponiveis = list(banco_de_perguntas.keys())
        materias_selecionadas = st.multiselect(
            "Selecione as matérias:",
            options=materias_disponiveis,
            default=materias_disponiveis[:3] if len(materias_disponiveis) >= 3 else materias_disponiveis
        )

        num_perguntas = st.slider(
            "Número de perguntas:",
            min_value=5,
            max_value=10,
            value=10,
            step=5
        )

        dificuldade = st.radio(
            "Nível de dificuldade:",
            options=["Fácil", "Médio", "Difícil", "Mista"]
        )

        if st.button("🚀 Iniciar Quiz", type="primary"):
            if st.session_state.nome_aluno and st.session_state.turma:
                if not materias_selecionadas:
                    st.error("Por favor, selecione pelo menos uma matéria!")
                else:
                    st.session_state.modo = "quiz"
                    st.session_state.pontuacao = 0
                    st.session_state.tempo_inicio = datetime.datetime.now()
                    st.session_state.perguntas_selecionadas = selecionar_perguntas(
                        materias_selecionadas, num_perguntas, dificuldade
                    )

                    # Verificar se há perguntas selecionadas
                    if not st.session_state.perguntas_selecionadas:
                        st.error(
                            "Não foi possível encontrar perguntas com os critérios selecionados. Tente outras opções.")
                        st.session_state.modo = "inicial"
                    else:
                        st.session_state.respostas_aluno = {}
                        st.rerun()
            else:
                st.error("Por favor, preencha seu nome e turma!")

    elif st.session_state.modo == "quiz":
        st.info(f"Aluno: {st.session_state.nome_aluno}")
        st.info(f"Turma: {st.session_state.turma}")

        if st.button("❌ Cancelar Quiz"):
            st.session_state.modo = "inicial"
            st.rerun()

    elif st.session_state.modo == "resultado":
        st.success(f"Pontuação: {st.session_state.pontuacao}/{len(st.session_state.perguntas_selecionadas)}")

        if st.button("🔄 Novo Quiz"):
            st.session_state.modo = "inicial"
            st.rerun()

        if st.button("📊 Ver Estatísticas"):
            st.session_state.modo = "estatisticas"
            st.rerun()

    elif st.session_state.modo == "estatisticas":
        if st.button("⬅️ Voltar"):
            st.session_state.modo = "resultado"
            st.rerun()

        excel_data = exportar_excel()
        if excel_data:
            st.download_button(
                label="📥 Baixar Resultados (Excel)",
                data=excel_data,
                file_name=f"resultados_quiz_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

# Conteúdo principal
if st.session_state.modo == "inicial":
    st.title("🧠 Quiz Interdisciplinar - Ensino Fundamental")
    st.caption("Aprendizado divertido e conectado ao seu dia a dia!")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Matérias", len(banco_de_perguntas))
    with col2:
        total_perguntas = sum(len(perguntas) for perguntas in banco_de_perguntas.values())
        st.metric("Total de Perguntas", total_perguntas)
    with col3:
        st.metric("Níveis de Dificuldade", "3")

    st.markdown("---")
    st.subheader("📝 Como funciona?")
    st.markdown("""
    1. Preencha seu nome e turma no menu lateral
    2. Escolha as matérias que deseja praticar
    3. Defina o número de perguntas e o nível de dificuldade
    4. Clique em "Iniciar Quiz" e teste seus conhecimentos!
    """)

    st.info("👨‍🏫 Professores: Vocês podem acessar as estatísticas de desempenho dos alunos após a conclusão do quiz.")

elif st.session_state.modo == "quiz":
    st.title("🧠 Quiz Interdisciplinar")

    # Verificar se há perguntas selecionadas
    if not st.session_state.perguntas_selecionadas:
        st.error(
            "Não foi possível encontrar perguntas para as matérias selecionadas. Por favor, selecione outras matérias ou níveis de dificuldade.")
        if st.button("Voltar para configuração"):
            st.session_state.modo = "inicial"
            st.rerun()
    else:
        # Mostrar progresso
        progresso = st.progress(0)

        # Criar abas para as perguntas
        tabs = st.tabs([f"Pergunta {i + 1}" for i in range(len(st.session_state.perguntas_selecionadas))])

        # Exibir perguntas em abas
        for i, (tab, pergunta) in enumerate(zip(tabs, st.session_state.perguntas_selecionadas)):
            with tab:
                st.subheader(f"📚 {pergunta['materia']} - {pergunta['dificuldade']}")
                st.markdown(f"**{pergunta['pergunta']}**")

                # Usar session_state para manter as respostas entre reruns
                resposta_key = f"resposta_{i}"
                resposta = st.radio(
                    "Escolha uma opção:",
                    pergunta["opcoes"],
                    key=resposta_key,
                    horizontal=True
                )

                st.session_state.respostas_aluno[i] = resposta

                # Atualizar progresso
                progresso.progress((i + 1) / len(st.session_state.perguntas_selecionadas))

        # Botão para finalizar o quiz
        col1, col2 = st.columns([1, 5])
        with col1:
            if st.button("✅ Finalizar Quiz", type="primary"):
                # Calcular pontuação
                pontuacao = 0
                for i, pergunta in enumerate(st.session_state.perguntas_selecionadas):
                    if st.session_state.respostas_aluno.get(i) == pergunta["resposta"]:
                        pontuacao += 1

                # Calcular tempo gasto
                tempo_final = datetime.datetime.now()
                tempo_gasto = (tempo_final - st.session_state.tempo_inicio).total_seconds()

                # Atualizar estado
                st.session_state.pontuacao = pontuacao

                # Salvar resultados
                materias = list(set(p["materia"] for p in st.session_state.perguntas_selecionadas))
                dificuldade = list(set(p["dificuldade"] for p in st.session_state.perguntas_selecionadas))
                salvar_resultados(
                    st.session_state.nome_aluno,
                    st.session_state.turma,
                    pontuacao,
                    len(st.session_state.perguntas_selecionadas),
                    tempo_gasto,
                    materias,
                    "/".join(dificuldade)
                )

                # Mudar para modo de resultado
                st.session_state.modo = "resultado"
                st.rerun()

elif st.session_state.modo == "resultado":
    st.title("🏆 Resultado do Quiz")

    # Calcular percentual de acerto
    total_perguntas = len(st.session_state.perguntas_selecionadas)
    percentual = (st.session_state.pontuacao / total_perguntas) * 100

    # Exibir resultado com animação
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown(f"### Olá, {st.session_state.nome_aluno}!")
        st.markdown(f"### Turma: {st.session_state.turma}")
        st.markdown(f"### Pontuação: {st.session_state.pontuacao} de {total_perguntas}")

        # Mensagem baseada no desempenho
        if percentual == 100:
            st.success("🎉 Perfeito! Você acertou todas as perguntas!")
            st.balloons()
        elif percentual >= 70:
            st.success("👏 Muito bom! Você teve um ótimo desempenho!")
        elif percentual >= 50:
            st.info("👍 Bom trabalho! Continue estudando!")
        else:
            st.warning("📚 Continue praticando! Você consegue melhorar!")

    with col2:
        # Gráfico de pontuação
        fig = px.pie(
            values=[st.session_state.pontuacao, total_perguntas - st.session_state.pontuacao],
            names=["Acertos", "Erros"],
            color=["green", "red"],
            hole=0.4,
            title="Seu desempenho"
        )
        st.plotly_chart(fig)

    # Revisão das perguntas
    st.markdown("## 📝 Revisão das Perguntas")

    for i, pergunta in enumerate(st.session_state.perguntas_selecionadas):
        resposta_aluno = st.session_state.respostas_aluno.get(i)
        resposta_correta = pergunta["resposta"]

        with st.expander(f"Pergunta {i + 1}: {pergunta['materia']} - {pergunta['dificuldade']}"):
            st.markdown(f"**{pergunta['pergunta']}**")

            if resposta_aluno == resposta_correta:
                st.success(f"✅ Sua resposta: {resposta_aluno}")
            else:
                st.error(f"❌ Sua resposta: {resposta_aluno}")
                st.success(f"✅ Resposta correta: {resposta_correta}")

            st.info(f"📚 **Explicação:** {pergunta['explicacao']}")

elif st.session_state.modo == "estatisticas":
    st.title("📊 Estatísticas de Desempenho")

    if len(st.session_state.historico) > 0:
        # Converter histórico para DataFrame
        df = pd.DataFrame(st.session_state.historico)

        # Exibir tabela de resultados
        st.subheader("Histórico de Resultados")
        st.dataframe(df)

        # Gráficos
        st.subheader("Análise de Desempenho")

        col1, col2 = st.columns(2)

        with col1:
            # Gráfico de evolução por data
            if len(df) > 1:
                fig = px.line(
                    df,
                    x="Data",
                    y="Percentual",
                    title="Evolução de Desempenho",
                    markers=True
                )
                st.plotly_chart(fig)

        with col2:
            # Gráfico de desempenho por matéria
            if "Matérias" in df.columns:
                # Criar uma lista de todas as matérias
                todas_materias = []
                for materias_str in df["Matérias"]:
                    materias_lista = [m.strip() for m in materias_str.split(",")]
                    todas_materias.extend(materias_lista)

                # Contar ocorrências
                contagem_materias = pd.Series(todas_materias).value_counts()

                fig = px.bar(
                    x=contagem_materias.index,
                    y=contagem_materias.values,
                    title="Matérias mais praticadas",
                    labels={"x": "Matéria", "y": "Quantidade de quizzes"}
                )
                st.plotly_chart(fig)

        # Estatísticas gerais
        st.subheader("Estatísticas Gerais")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Média de Acertos", f"{df['Percentual'].mean():.1f}%")
        with col2:
            st.metric("Melhor Pontuação", f"{df['Percentual'].max():.1f}%")
        with col3:
            st.metric("Total de Quizzes", len(df))

    else:
        st.info("Ainda não há dados de desempenho disponíveis. Complete um quiz para ver estatísticas.")
