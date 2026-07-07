from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List

from schemas.usuario import UsuarioCreate, UsuarioResponse, UsuarioUpdate
from models.usuario import UsuarioDB
from database import get_db

router = APIRouter(prefix="/api/v1/usuarios", tags=["Usuários"])

@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
async def criar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    """Cria um novo usuário e salva no banco de dados persistente."""
    db_usuario = UsuarioDB(**usuario.model_dump())
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

@router.get("/", response_model=List[UsuarioResponse])
async def listar_usuarios(db: Session = Depends(get_db)):
    """Retorna todos os usuários cadastrados."""
    return db.query(UsuarioDB).all()

@router.get("/{usuario_id}", response_model=UsuarioResponse)
async def buscar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """Busca um usuário específico pelo seu ID."""
    usuario = db.query(UsuarioDB).filter(UsuarioDB.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return usuario

@router.put("/{usuario_id}", response_model=UsuarioResponse)
async def atualizar_usuario(usuario_id: int, usuario_update: UsuarioUpdate, db: Session = Depends(get_db)):
    """Atualiza de forma parcial ou total os dados de um usuário existente."""
    usuario_db = db.query(UsuarioDB).filter(UsuarioDB.id == usuario_id).first()
    if not usuario_db:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    
    # Extrai apenas os dados que foram enviados na requisição (exclude_unset=True)
    dados_novos = usuario_update.model_dump(exclude_unset=True)
    
    for key, value in dados_novos.items():
        setattr(usuario_db, key, value)
        
    db.commit()
    db.refresh(usuario_db)
    return usuario_db

@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """Remove um usuário do sistema."""
    usuario_db = db.query(UsuarioDB).filter(UsuarioDB.id == usuario_id).first()
    if not usuario_db:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    
    db.delete(usuario_db)
    db.commit()
    return None