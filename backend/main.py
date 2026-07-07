import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from core.graph_engine import load_graph_hin, run_random_walk
from routers import usuarios
from database import engine, Base

# 1. Cria as tabelas no banco de dados SQLite automaticamente na inicialização
Base.metadata.create_all(bind=engine)

# 2. INSTÂNCIA GLOBAL DO APP
app = FastAPI(
    title="BTS Graph Recommender API",
    description="Sistema de Recomendação em Redes Complexas: Mitigando Preconceitos Musicais através da Discografia do BTS",
    version="1.0.0"
)

# 3. Configuração de Segurança (CORS)
origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Registro do CRUD de Usuários
app.include_router(usuarios.router)

# 5. Configuração do Motor de Grafos
# Caminho absoluto para o banco de dados estático JSON que alimenta os nós do BTS
JSON_PATH = os.path.join(os.path.dirname(__file__), "data", "bts_discography.json")

# Schema estrito para a requisição de cálculo estocástico (Random Walk)
class RecomendacaoInput(BaseModel):
    usuario_alvo: str = Field(..., description="Nome do usuário (Ex: User_Carlos)")
    generos_favoritos: list[str] = Field(..., description="Array de gêneros. Ex: ['Hip-Hop/Rap']")
    passos: int = Field(default=25000, description="Iterações de Monte Carlo")
    chance_restart: float = Field(default=0.15, description="Fator Alfa limitador")

# 6. Endpoint de Recomendação Topológica
@app.post("/api/v1/recomendacao", tags=["Recomendação HIN"])
async def gerar_recomendacao(dados: RecomendacaoInput):
    """
    Endpoint principal para calcular a rota topológica e quebrar o Cold-Start,
    instanciando o componente gigante da Rede de Informação Heterogênea.
    """
    try:
        # Passo A: Instanciação da Topologia Matemática
        grafo_hin = load_graph_hin(
            filepath=JSON_PATH,
            user_name=dados.usuario_alvo,
            user_genres=dados.generos_favoritos
        )
        
        # Passo B: Execução do algoritmo de Random Walk with Restart (RWR)
        resultado_bruto = run_random_walk(
            G=grafo_hin, 
            target_node=dados.usuario_alvo, 
            steps=dados.passos, 
            alpha=dados.chance_restart
        )
        
        # Passo C: Formatação Top-K para a resposta JSON consumida pelo Angular
        recomendacoes = [{"faixa": item[0], "score_topologico": item[1]} for item in resultado_bruto]
        
        return {
            "usuario_analisado": dados.usuario_alvo,
            "total_recomendacoes": len(recomendacoes),
            "ranking": recomendacoes
        }
        
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Base de dados JSON não localizada no servidor.")
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=f"Erro de valor no grafo: {str(ve)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno ao processar o Random Walk: {str(e)}")