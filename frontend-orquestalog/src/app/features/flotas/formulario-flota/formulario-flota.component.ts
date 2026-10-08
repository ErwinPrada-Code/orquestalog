import { Component, OnInit, ChangeDetectorRef, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { CatalogoService } from '../../../core/services/catalogo.service';
import { ToastService } from '../../../core/services/toast.service';
import { FlotaPayload } from '../../../core/models/catalogos';

@Component({
  selector: 'app-formulario-flota',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './formulario-flota.component.html',
})
export class FormularioFlotaComponent implements OnInit {
  flota: FlotaPayload = { nombre: '', tipo: 'camion', capacidad: 1 };
  readonly tipos = [
    { valor: 'camion', etiqueta: 'Camión' },
    { valor: 'furgoneta', etiqueta: 'Furgoneta' },
    { valor: 'moto', etiqueta: 'Moto' },
  ];

  isEdit = false;
  cargando = false;
  error = '';
  private id: number | null = null;

  private catalogoService = inject(CatalogoService);
  private toast = inject(ToastService);
  private router = inject(Router);
  private route = inject(ActivatedRoute);
  private cdr = inject(ChangeDetectorRef);

  ngOnInit(): void {
    const idParam = this.route.snapshot.paramMap.get('id');
    if (!idParam) return;

    this.isEdit = true;
    this.id = Number(idParam);
    this.cargando = true;
    this.catalogoService.getFlota(this.id).subscribe({
      next: (f) => {
        this.flota = { nombre: f.nombre, tipo: f.tipo, capacidad: f.capacidad };
        this.cargando = false;
        this.cdr.detectChanges();
      },
      error: () => {
        this.error = 'No se pudo cargar la flota.';
        this.cargando = false;
        this.cdr.detectChanges();
      },
    });
  }

  guardar(): void {
    this.cargando = true;
    this.error = '';

    const payload: FlotaPayload = {
      nombre: this.flota.nombre.trim(),
      tipo: this.flota.tipo,
      capacidad: Number(this.flota.capacidad),
    };

    const peticion =
      this.isEdit && this.id
        ? this.catalogoService.updateFlota(this.id, payload)
        : this.catalogoService.createFlota(payload);

    peticion.subscribe({
      next: () => {
        this.toast.exito(this.isEdit ? 'Flota actualizada correctamente.' : 'Flota creada correctamente.');
        this.router.navigate(['/flotas']);
      },
      error: (err) => {
        const detalle = err.error?.detail;
        this.error =
          typeof detalle === 'string'
            ? detalle
            : 'No se pudo guardar la flota. Revisa los datos ingresados.';
        this.cargando = false;
        this.cdr.detectChanges();
      },
    });
  }
}
