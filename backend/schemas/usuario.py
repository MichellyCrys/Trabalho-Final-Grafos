from pydantic import BaseModel, Field
from typing import Optional

class UsuarioBase(BaseModel):
    nome: str = Field(..., description="Nome completo ou apelido do usuário")
    idade: int = Field(..., gt=0, description="Idade do usuário (deve ser maior que zero)")
    genero_musical_preferivel: str = Field(..., description="Gênero musical favorito (Ex: Hip-Hop/Rap, Pop, R&B/Soul)")

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    idade: Optional[int] = None
    genero_musical_preferivel: Optional[str] = None

class UsuarioResponse(UsuarioBase):
    id: int

    class Config:
        from_attributes = True