# Mitigação de Viés Musical via Redes Complexas

### Engine de Recomendação Topológica para a Discografia do BTS

Este projeto apresenta um Sistema de Recomendação (SR) focado na mitigação de preconceitos musicais estruturais através da Teoria dos Grafos e Ciência das Redes. O sistema modela a discografia do grupo sul-coreano BTS por meio de uma **Rede de Informação Heterogênea (HIN)**, conectando usuários não-fãs a atributos de gêneros neutros (Hip-Hop, Pop, R&B, EDM) e mapeando o catálogo de faixas de acordo com sua textura sonora. 

Para quebrar o problema de "partida fria" (Cold-Start) e furar as bolhas algorítmicas, o sistema implementa o algoritmo estocástico **Random Walk with Restart (RWR)** baseado em Cadeias de Markov.

---

## 🛠️ Tecnologias Utilizadas

### Backend
* **FastAPI:** Framework assíncrono em Python para construção de rotas REST.
* **NetworkX:** Biblioteca matemática para modelagem, manipulação e cálculo estocástico em grafos.
* **SQLAlchemy & SQLite:** Mapeamento Objeto-Relacional (ORM) para persistência transacional de perfis de usuários.

### Frontend
* **Angular 16:** Framework SPA utilizando controle reativo de estado através de *Signals*.
* **Angular Material:** Componentes de interface e experiência do usuário baseados no Design System do Google.
* **Cytoscape.js:** Motor gráfico de vanguarda para plotagem interativa de malhas topológicas.

---

## 📁 Estrutura do Repositório

```text
.
├── backend/          # API assíncrona em FastAPI e motor de grafos (NetworkX)
├── frontend/         # Interface SPA em Angular 16 e canvas em Cytoscape.js
└── docker-compose.yml # Orquestração do ecossistema unificado local

```

---

## 🚀 Como Executar o Projeto

O ecossistema foi totalmente conteinerizado utilizando o Docker, dispensando a necessidade de instalar dependências locais de Python ou Node de forma manual.

1. Certifique-se de ter o **Docker** e o **Docker Compose** instalados na sua máquina.
2. Clone este repositório e navegue até a pasta raiz do projeto:
```bash
git clone [https://github.com/MichellyCrys/Trabalho-Final-Grafos.git](https://github.com/MichellyCrys/Trabalho-Final-Grafos.git)
cd Trabalho-Final-Grafos

```


3. Execute a inicialização e compilação das imagens através do terminal:
```bash
docker compose up --build

```


4. Assim que os contêineres subirem, acesse os serviços no seu navegador:
* **Interface do Usuário (Frontend):** `http://localhost:4200`
* **Documentação Swagger da API (Backend):** `http://localhost:8000/docs`



---

## 🔬 Metodologia e Complexidade

* **Modelagem Semântica:** Usuário $\rightarrow$ Gênero Musical $\rightarrow$ Faixa do BTS.
* **Complexidade Temporal:** $O(N)$ linear, onde $N$ é o número limite fixado de passos de Monte Carlo.
* **Complexidade Espacial:** $O(|V| + |E|)$ restrito ao tamanho da malha heterogênea.
