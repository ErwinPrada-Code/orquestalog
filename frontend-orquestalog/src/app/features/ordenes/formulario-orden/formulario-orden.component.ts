import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, ActivatedRoute, RouterModule } from '@angular/router';
import { OrdenService } from '../../../core/services/orden.service';
import { Orden } from '../../../core/models/orden';

@Component({
  selector: 'app-formulario-orden',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './formulario-orden.component.html'
})
export class FormularioOrdenComponent implements OnInit {
  // Datos iniciales por defecto
  orden: Orden = {
    descripcion: '',
    estado: 'pendiente',
    centro_distribucion_id: 1,
    flota_id: 1,
    ruta_id: 1,
    empresa_id: 1 // Por defecto para la prueba multiempresa
  };
  
  isEdit = false;
  cargando = false;
  
  private ordenService = inject(OrdenService);
  private router = inject(Router);
  private route = inject(ActivatedRoute);

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.isEdit = true;
      this.cargando = true;
      // Cargar la orden si estamos en modo edición
      this.ordenService.getOrden(Number(id)).subscribe({
        next: (data) => {
          this.orden = data;
          this.cargando = false;
        },
        error: (err) => {
          console.error(err);
          this.cargando = false;
        }
      });
    }
  }

  guardarOrden(): void {
    this.cargando = true;
    if (this.isEdit && this.orden.id) {
      this.ordenService.updateOrden(this.orden.id, this.orden).subscribe({
        next: () => this.router.navigate(['/ordenes']),
        error: (err) => { console.error(err); this.cargando = false; }
      });
    } else {
      this.ordenService.createOrden(this.orden).subscribe({
        next: () => this.router.navigate(['/ordenes']),
        error: (err) => {
          console.error(err);
          alert('Error: ' + (err.error?.detail || 'Verifica que la flota no exceda su capacidad.'));
          this.cargando = false;
        }
      });
    }
  }
}