import { Component, OnInit, ChangeDetectorRef, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { OrdenService } from '../../core/services/orden.service';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './dashboard.component.html',
})
export class DashboardComponent implements OnInit {
  cargando = true;
  error = '';

  totalOrdenes = 0;
  pendientes = 0;
  enCurso = 0;
  completadas = 0;

  private ordenService = inject(OrdenService);
  private cdr = inject(ChangeDetectorRef);

  ngOnInit(): void {
    this.ordenService.getResumen().subscribe({
      next: (r) => {
        this.totalOrdenes = r.total;
        this.pendientes = r.pendientes;
        this.enCurso = r.en_proceso;
        this.completadas = r.completadas;
        this.cargando = false;
        this.cdr.detectChanges();
      },
      error: (err) => {
        console.error('Error cargando dashboard:', err);
        this.error = 'No se pudieron cargar las métricas.';
        this.cargando = false;
        this.cdr.detectChanges();
      },
    });
  }

  getPorcentaje(valor: number): string {
    if (this.totalOrdenes === 0) return '0%';
    return Math.round((valor / this.totalOrdenes) * 100) + '%';
  }
}
