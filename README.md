#  🧠 **Quizz Interdisciplinar Educacional**

Um aplicativo interativo desenvolvido com Streamlit e Python que tem objetivo de promover o aprendizado interdisciplinar de forma interativa e personalizada para alunos do **Ensino Fundamental I e II**. O quiz é adaptável por matéria , dificuldade e número de perguntas,
ele fornece estatísticas detalhadas a respeito do desempenho de cada aluno ao finalizar o quiz.

Foi desenvolvido com base em Projeto de Extensão Oferecido pela **Faculdade Descomplica digital**

## **Funcionalidades**

📝 - Cadastro de aluno e turma

📚 - Seleção de matérias e dificuldade (Fácil, Médio, Difícil, Mista)

🔢 - Escolha do número de perguntas

✅ - Avaliação imediata com feedback e explicações

📊 - Geração de estatísticas e gráficos interativos

☁️ - Integração com Google Sheets (para salvar resultados)

📥 - Exportação dos resultados em Excel (.xlsx)


## **Tecnologias utilizadas:**

- Streamlit
- Pandas
- Plotly
- gspread + Google API ( Sheets e Drive) - opcional, caso não tenha a API, fornece a opção e baixar o relatório via excel.


## **Para Professores**

- Você pode usar este quiz em sala de aula para:

- Avaliar o desempenho dos alunos

- Trabalhar conteúdos de forma lúdica

- Acompanhar evolução por tema/matéria


## **Demostração do projeto**

### **Tela Inicial - principais elementos e funcionalidades:**

1. Menu do Quizz (Lateral Esquerda):
  - Nome do Aluno: Campo para que o aluno preencha seu nome
  - Turma: Colocar a turma do respctivo aluno

2. Configuração do Quizz:
   - Seleção de matérias: Permite escolher as matérias que serão incluidas no quiz ( Matemática, Português e Ciências)
   - Número de Perguntas: Controle deslizante que define a quantidade de perguntas ( mínimo no 5 e máximo no 10)
   - Nível de Dificuldade do Quiz: 
      - Fácil
      - Médio
      - Díficil
      - Mista (Combina as dificuldades acima)
      - Botão de iniciar o quiz.

3. Informações no Centro da Tela:
   - Resumo do Quiz:
       - Total de Matérias: Exibe o número de matérias selecionadas.
       - Total de Perguntas: Mostra o número total de perguntas disponíveis no banco de dados.
       - Níveis de Dificuldade: Indica a quantidade de níveis de dificuldade disponíveis no quiz.
       - Instruções para o usuário (Aluno)
       - Professores podem acessar as estatísticas de desempenho dos alunos após a conclusão do quiz.

![image](https://github.com/user-attachments/assets/f2eae889-b6ed-4fce-9e14-5e77c1565a0e)

### **Tela de Perguntas **

1. Apresenta a matéria selecionada pelo aluno, quantidade de perguntas, nível da pergunta.

![image](https://github.com/user-attachments/assets/11d3cb08-9939-43a9-8f38-5d0ea7c10da0)

###** Tela de Resultado**

1. É capaz de verificar quais foram os acertos do aluno.
2. No menu lateral tem duas funcionalidades:
     - Iniciar um novo quiz.
     - Ver o desempenho dos alunos - "Ver estatísticas"
       
![image](https://github.com/user-attachments/assets/2f6c67a3-be1a-4f5d-b408-54998b76cc72)

- **Tela de estatísticas:**
    - Capaz de exportar o relatório do Quiz.

![image](https://github.com/user-attachments/assets/8dea3d86-61db-4141-be7e-08c5c4c92f51)

