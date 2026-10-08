import { Component, OnInit, inject, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { OrdenService } from '../../../core/services/orden.service';
import { AuthService } from '../../../core/services/auth.service';
import { ToastService } from '../../../core/services/toast.service';
import { Orden } from '../../../core/models/orden';

@Component({
  selector: 'app-listado-ordenes',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './listado-ordenes.component.html',
  styleUrls: ['./listado-ordenes.component.css']
})
export class ListadoOrdenesComponent implements OnInit {
  ordenes: Orden[] = [];
  cargando = true;
  error = '';
  busqueda = '';

  readonly auth = inject(AuthService);
  private ordenService = inject(OrdenService);
  private toast = inject(ToastService);
  private cdr = inject(ChangeDetectorRef);

  ngOnInit(): void {
    this.cargarOrdenes();
  }

  get ordenesFiltradas(): Orden[] {
    const termino = this.busqueda.trim().toLowerCase();
    if (!termino) return this.ordenes;
    return this.ordenes.filter(o =>
      String(o.id).includes(termino) ||
      o.descripcion.toLowerCase().includes(termino) ||
      o.estado.toLowerCase().includes(termino)
    );
  }

  cargarOrdenes(): void {
    this.ordenService.getOrdenes().subscribe({
      next: (data) => {
        this.ordenes = data;
        this.cargando = false;
        this.cdr.detectChanges();
      },
      error: (err) => {
        console.error('Error al cargar órdenes:', err);
        this.error = 'No se pudieron cargar las órdenes.';
        this.cargando = false;
        this.cdr.detectChanges();
      }
    });
  }

  eliminarOrden(id: number | undefined): void {
    if (!id) return;

    if (confirm('¿Estás seguro de que deseas eliminar esta orden?')) {
      this.ordenService.deleteOrden(id).subscribe({
        next: () => {
          this.ordenes = this.ordenes.filter(o => o.id !== id);
          this.toast.exito(`Orden #${id} eliminada correctamente.`);
          this.cdr.detectChanges();
        },
        error: (err) => this.toast.error(err.error?.detail ?? 'No se pudo eliminar la orden.')
      });
    }
  }
}
