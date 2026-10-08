import { Component, inject } from '@angular/core';
import { ToastService } from '../../services/toast.service';

@Component({
  selector: 'app-toast',
  standalone: true,
  template: `
    <div class="toast-stack" aria-live="polite">
      @for (t of toast.toasts(); track t.id) {
        <div class="toast" [class.toast--exito]="t.tipo === 'exito'" [class.toast--error]="t.tipo === 'error'" role="status">
          <span>{{ t.mensaje }}</span>
          <button type="button" class="toast-close" (click)="toast.cerrar(t.id)" aria-label="Cerrar">×</button>
        </div>
      }
    </div>
  `,
})
export class ToastComponent {
  readonly toast = inject(ToastService);
}
