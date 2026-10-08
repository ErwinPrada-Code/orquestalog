import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { OrdenService } from '../../core/services/orden.service';
import { Orden } from '../../core/models/orden';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './dashboard.component.html'
})
export class DashboardComponent implements OnInit {
  ordenes: Orden[] = [];
  cargando = true;

  // KPIs
  totalOrdenes = 0;
  pendientes = 0;
  enCurso = 0;
  completadas = 0;

  private ordenService = inject(OrdenService);

  ngOnInit(): void {
    this.ordenService.getOrdenes().subscribe({
      next: (data) => {
        this.ordenes = data;
        this.calcularMetricas();
        this.cargando = false;
      },
      error: (err) => {
        console.error('Error cargando dashboard:', err);
        this.cargando = false;
      }
    });
  }

  calcularMetricas(): void {
    this.totalOrdenes = this.ordenes.length;
    this.pendientes = this.ordenes.filter(o => o.estado === 'pendiente').length;
    this.enCurso = this.ordenes.filter(o => o.estado === 'en_proceso').length;
    this.completadas = this.ordenes.filter(o => o.estado === 'completada').length;
  }

  // Calcula el ancho de las barras de progreso
  getPorcentaje(valor: number): string {
    if (this.totalOrdenes === 0) return '0%';
    return Math.round((valor / this.totalOrdenes) * 100) + '%';
  }
}