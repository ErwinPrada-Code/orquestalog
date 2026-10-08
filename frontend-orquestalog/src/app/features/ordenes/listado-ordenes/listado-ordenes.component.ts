import { Component, OnInit, inject, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { OrdenService } from '../../../core/services/orden.service';
import { Orden } from '../../../core/models/orden';

@Component({
  selector: 'app-listado-ordenes',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './listado-ordenes.component.html',
  styleUrls: ['./listado-ordenes.component.css']
})
export class ListadoOrdenesComponent implements OnInit {
  ordenes: Orden[] = [];
  cargando = true;
  private ordenService = inject(OrdenService);
  private cdr = inject(ChangeDetectorRef); // <-- Fuerza el redibujado de la pantalla

  ngOnInit(): void {
    this.cargarOrdenes();
  }

  cargarOrdenes(): void {
    this.ordenService.getOrdenes().subscribe({
      next: (data) => {
        this.ordenes = data;
        this.cargando = false;
        this.cdr.detectChanges(); // <-- Obliga a Angular a quitar el "Cargando..." y mostrar la tabla
      },
      error: (err) => {
        console.error('Error al cargar órdenes:', err);
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
          this.cdr.detectChanges(); // <-- Actualiza la vista inmediatamente al borrar
        },
        error: (err) => console.error('Error al eliminar:', err)
      });
    }
  }
}