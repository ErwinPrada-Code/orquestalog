import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, ActivatedRoute, RouterModule } from '@angular/router';
import { forkJoin } from 'rxjs';
import { OrdenService } from '../../../core/services/orden.service';
import { CatalogoService } from '../../../core/services/catalogo.service';
import { Orden, OrdenPayload } from '../../../core/models/orden';
import { Centro, Flota, Ruta } from '../../../core/models/catalogos';

@Component({
  selector: 'app-formulario-orden',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './formulario-orden.component.html'
})
export class FormularioOrdenComponent implements OnInit {
  orden: Orden = {
    descripcion: '',
    estado: 'pendiente',
    centro_distribucion_id: 0,
    flota_id: 0,
    ruta_id: 0
  };

  centros: Centro[] = [];
  flotas: Flota[] = [];
  rutas: Ruta[] = [];
  readonly estados = [
    { valor: 'pendiente', etiqueta: 'Pendiente' },
    { valor: 'en_proceso', etiqueta: 'En proceso' },
    { valor: 'completada', etiqueta: 'Completada' }
  ];

  isEdit = false;
  cargando = false;
  error = '';

  private ordenService = inject(OrdenService);
  private catalogoService = inject(CatalogoService);
  private router = inject(Router);
  private route = inject(ActivatedRoute);

  ngOnInit(): void {
    this.cargando = true;
    forkJoin({
      centros: this.catalogoService.getCentros(),
      flotas: this.catalogoService.getFlotas(),
      rutas: this.catalogoService.getRutas()
    }).subscribe({
      next: ({ centros, flotas, rutas }) => {
        this.centros = centros;
        this.flotas = flotas;
        this.rutas = rutas;

        const id = this.route.snapshot.paramMap.get('id');
        if (id) {
          this.isEdit = true;
          this.cargarOrden(Number(id));
        } else {
          this.orden.centro_distribucion_id = centros[0]?.id ?? 0;
          this.orden.flota_id = flotas[0]?.id ?? 0;
          this.orden.ruta_id = rutas[0]?.id ?? 0;
          this.cargando = false;
        }
      },
      error: () => {
        this.error = 'No se pudieron cargar los catálogos (centros, flotas y rutas).';
        this.cargando = false;
      }
    });
  }

  private cargarOrden(id: number): void {
    this.ordenService.getOrden(id).subscribe({
      next: (data) => {
        this.orden = data;
        this.cargando = false;
      },
      error: () => {
        this.error = 'No se pudo cargar la orden.';
        this.cargando = false;
      }
    });
  }

  guardarOrden(): void {
    this.cargando = true;
    this.error = '';

    const payload: OrdenPayload = {
      descripcion: this.orden.descripcion.trim(),
      estado: this.orden.estado,
      centro_distribucion_id: this.orden.centro_distribucion_id,
      flota_id: this.orden.flota_id,
      ruta_id: this.orden.ruta_id
    };

    const peticion = this.isEdit && this.orden.id
      ? this.ordenService.updateOrden(this.orden.id, payload)
      : this.ordenService.createOrden(payload);

    peticion.subscribe({
      next: () => this.router.navigate(['/ordenes']),
      error: (err) => {
        const detalle = err.error?.detail;
        this.error = typeof detalle === 'string'
          ? detalle
          : 'No se pudo guardar la orden. Revisa los datos ingresados.';
        this.cargando = false;
      }
    });
  }
}
