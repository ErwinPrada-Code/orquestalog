import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterModule } from '@angular/router';
import { OrdenService } from '../../../core/services/orden.service';
import { Orden } from '../../../core/models/orden';

@Component({
  selector: 'app-detalle-orden',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './detalle-orden.component.html'
})
export class DetalleOrdenComponent implements OnInit {
  orden: Orden | null = null;
  cargando = true;
  error = '';

  private route = inject(ActivatedRoute);
  private ordenService = inject(OrdenService);

  ngOnInit(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    if (!id) {
      this.error = 'Identificador de orden inválido.';
      this.cargando = false;
      return;
    }
    this.ordenService.getOrden(id).subscribe({
      next: (data) => {
        this.orden = data;
        this.cargando = false;
      },
      error: (err) => {
        this.error = err.status === 404 ? 'La orden no existe.' : 'No se pudo cargar la orden.';
        this.cargando = false;
      }
    });
  }
}
