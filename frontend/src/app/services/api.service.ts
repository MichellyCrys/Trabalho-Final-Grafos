import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Usuario {
  id?: number;
  nome: string;
  idade: number;
  genero_musical_preferivel: string;
}

export interface RecomendacaoPayload {
  usuario_alvo: string;
  generos_favoritos: string[];
  passos?: number;
  chance_restart?: number;
}

export interface TrackRecommendation {
  faixa: string;
  score_topologico: number;
}

export interface RecomendacaoResponse {
  usuario_analisado: string;
  total_recomendacoes: number;
  ranking: TrackRecommendation[];
}

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private readonly http = inject(HttpClient);
  private readonly baseUrl = 'http://localhost:8000/api/v1';

  // CRUD de Usuários
  getUsuarios(): Observable<Usuario[]> {
    return this.http.get<Usuario[]>(`${this.baseUrl}/usuarios/`);
  }

  criarUsuario(usuario: Usuario): Observable<Usuario> {
    return this.http.post<Usuario>(`${this.baseUrl}/usuarios/`, usuario);
  }

  deletarUsuario(id: number): Observable<void> {
    return this.http.delete<void>(`${this.baseUrl}/usuarios/${id}`);
  }

  // Motor de Recomendação HIN
  obterRecomendacao(payload: RecomendacaoPayload): Observable<RecomendacaoResponse> {
    return this.http.post<RecomendacaoResponse>(`${this.baseUrl}/recomendacao`, payload);
  }
}
