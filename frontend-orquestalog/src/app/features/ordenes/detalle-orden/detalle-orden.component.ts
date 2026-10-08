import { Component, OnInit, ChangeDetectorRef, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterModule } from '@angular/router';
import { forkJoin } from 'rxjs';
import { OrdenService } from '../../../core/services/orden.service';
import { CatalogoService } from '../../../core/services/catalogo.service';
import { Orden } from '../../../core/models/orden';
import { Centro, Flota, Ruta } from '../../../core/models/catalogos';

@Component({
  selector: 'app-detalle-orden',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './detalle-orden.component.html',
})
export class DetalleOrdenComponent implements OnInit {
  orden: Orden | null = null;
  centro: Centro | null = null;
  flota: Flota | null = null;
  ruta: Ruta | null = null;
  cargando = true;
  error = '';

  private route = inject(ActivatedRoute);
  private ordenService = inject(OrdenService);
  private catalogoService = inject(CatalogoService);
  private cdr = inject(ChangeDetectorRef);

  ngOnInit(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    if (!id) {
      this.error = 'Identificador de orden inválido.';
      this.cargando = false;
      return;
    }
    forkJoin({
      orden: this.ordenService.getOrden(id),
      centros: this.catalogoService.getCentros(),
      flotas: this.catalogoService.getFlotas(),
      rutas: this.catalogoService.getRutas(),
    }).subscribe({
      next: ({ orden, centros, flotas, rutas }) => {
        this.orden = orden;
        this.centro = centros.find((c) => c.id === orden.centro_distribucion_id) ?? null;
        this.flota = flotas.find((f) => f.id === orden.flota_id) ?? null;
        this.ruta = rutas.find((r) => r.id === orden.ruta_id) ?? null;
        this.cargando = false;
        this.cdr.detectChanges();
      },
      error: (err) => {
        this.error = err.status === 404 ? 'La orden no existe.' : 'No se pudo cargar la orden.';
        this.cargando = false;
        this.cdr.detectChanges();
      },
    });
  }
}
