import { Component, OnInit, ChangeDetectorRef, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { CatalogoService } from '../../../core/services/catalogo.service';
import { ToastService } from '../../../core/services/toast.service';
import { Flota } from '../../../core/models/catalogos';

@Component({
  selector: 'app-listado-flotas',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './listado-flotas.component.html',
})
export class ListadoFlotasComponent implements OnInit {
  flotas: Flota[] = [];
  cargando = true;
  error = '';

  private catalogoService = inject(CatalogoService);
  private toast = inject(ToastService);
  private cdr = inject(ChangeDetectorRef);

  ngOnInit(): void {
    this.catalogoService.getFlotas().subscribe({
      next: (data) => {
        this.flotas = data;
        this.cargando = false;
        this.cdr.detectChanges();
      },
      error: () => {
        this.error = 'No se pudieron cargar las flotas.';
        this.cargando = false;
        this.cdr.detectChanges();
      },
    });
  }

  eliminar(flota: Flota): void {
    if (!confirm(`¿Eliminar la flota "${flota.nombre}"?`)) return;

    this.catalogoService.deleteFlota(flota.id).subscribe({
      next: () => {
        this.flotas = this.flotas.filter((f) => f.id !== flota.id);
        this.toast.exito('Flota eliminada correctamente.');
        this.cdr.detectChanges();
      },
      error: (err) => this.toast.error(err.error?.detail ?? 'No se pudo eliminar la flota.'),
    });
  }
}
