import { Component, OnInit, inject, signal, ViewChild, ElementRef, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatButtonModule } from '@angular/material/button';
import { MatListModule } from '@angular/material/list';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import cytoscape from 'cytoscape';

import { ApiService, Usuario, TrackRecommendation } from '../../services/api.service';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [
    CommonModule, FormsModule, MatCardModule, MatFormFieldModule,
    MatInputModule, MatSelectModule, MatButtonModule, MatListModule,
    MatIconModule, MatProgressBarModule
  ],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {
  readonly apiService = inject(ApiService);
  readonly cdr = inject(ChangeDetectorRef);

  usuarios = signal<Usuario[]>([]);
  ranking = signal<TrackRecommendation[]>([]);
  usuarioSelecionado = signal<Usuario | null>(null);
  carregando = signal<boolean>(false);

  @ViewChild('cyGraph', { static: false }) cyGraphContainer!: ElementRef;

  // Tipagem restaurada para evitar erros silenciados
  private cy: cytoscape.Core | null = null;

  ngOnInit(): void {
    this.carregarControle();
  }

  carregarControle() {
    this.apiService.getUsuarios().subscribe(res => this.usuarios.set(res));
  }

  salvarUsuario(formValue: Usuario) {
    this.apiService.criarUsuario(formValue).subscribe(() => this.carregarControle());
  }

  deletarUsuario(id: number) {
    this.apiService.deletarUsuario(id).subscribe(() => this.carregarControle());
  }

  testarMitigacao(user: Usuario) {
    this.carregando.set(true);
    this.usuarioSelecionado.set(user);
    this.ranking.set([]);

    if (this.cy) {
      this.cy.destroy();
      this.cy = null;
    }
    if (this.cyGraphContainer?.nativeElement) {
      this.cyGraphContainer.nativeElement.style.width = '100%';
    }
    this.apiService.obterRecomendacao({
      usuario_alvo: user.nome,
      generos_favoritos: [user.genero_musical_preferivel]
    }).subscribe({
      next: (res) => {
        this.ranking.set(res.ranking);
        this.carregando.set(false);

        this.cdr.detectChanges();
        setTimeout(() => {
          this.renderizarGrafo(user, res.ranking);
        }, 150);
      },
      error: (err) => {
        this.carregando.set(false);
        console.error("Erro ao calcular Random Walk", err);
      }
    });
  }

  renderizarGrafo(user: Usuario, recomendacoes: TrackRecommendation[]) {
    if (!this.cyGraphContainer) {
      console.error("Canvas do grafo não encontrado!");
      return;
    }
    const cleanId = (str: string) => str.replace(/[^a-zA-Z0-9]/g, '_');

    const userId = cleanId(user.nome);
    const genreId = cleanId(user.genero_musical_preferivel);

    const elements: cytoscape.ElementDefinition[] = [];

    // 1. Instanciando o Nó do Usuário (Origem)
    elements.push({ data: { id: userId, label: user.nome, type: 'usuario' } });

    // 2. Instanciando o Nó de Gênero (A ponte topológica neutra)
    elements.push({ data: { id: genreId, label: user.genero_musical_preferivel, type: 'genero' } });
    elements.push({ data: { source: userId, target: genreId } });

    // 3. Instanciando os Nós das Músicas e Arestas
    const topRecomendacoes = recomendacoes.slice(0, 5);

    topRecomendacoes.forEach((rec) => {
      const trackId = cleanId(rec.faixa);
      elements.push({
        data: {
          id: trackId,
          label: `${rec.faixa}\n(${rec.score_topologico}v)`,
          type: 'musica'
        }
      });
      elements.push({ data: { source: genreId, target: trackId } });
    });

    // 4. Injetando a Topologia no Canvas
    this.cy = cytoscape({
      container: this.cyGraphContainer.nativeElement,
      elements: elements,

      style: [
        {
          selector: 'node',
          style: {
            'label': 'data(label)',
            'text-valign': 'bottom',
            'text-margin-y': 8,
            'color': '#212121',
            'text-wrap': 'wrap',
            'font-size': '11px',
            'font-family': 'Roboto',
            'font-weight': 'bold'
          }
        },
        {
          selector: 'node[type="usuario"]',
          style: { 'background-color': '#1976D2', 'width': 40, 'height': 40, 'shape': 'ellipse' }
        },
        {
          selector: 'node[type="genero"]',
          style: { 'background-color': '#8C52FF', 'width': 50, 'height': 50, 'shape': 'diamond' }
        },
        {
          selector: 'node[type="musica"]',
          style: { 'background-color': '#FFC107', 'width': 35, 'height': 35, 'shape': 'round-rectangle' }
        },
        {
          selector: 'edge',
          style: {
            'width': 2,
            'line-color': '#5E35B1',
            'target-arrow-color': '#5E35B1',
            'target-arrow-shape': 'triangle',
            'curve-style': 'bezier'
          }
        }
      ],
      layout: {
        name: 'breadthfirst',
        directed: true,
        padding: 30,
        spacingFactor: 1.5
      }
    });

    this.cy.ready(() => {
      this.cy!.fit();
      this.cy!.center();
    });
  }
}
